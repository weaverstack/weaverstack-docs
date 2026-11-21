---
meta_title: Incremental loads in Microsoft Fabric | Weaver docs
description: How Weaver loads only what changed, including why a consumer bookmark is needed, what a Table or Folder returns and how a source supplies change evidence.
social_title: Incremental loads in Microsoft Fabric
image_alt: Weaver logo.
schema_type: TechArticle
---

# Incremental loading

An incremental Table or Folder applies only the changes since its own last clean Load. Three things make that work: a bookmark that records how far the consumer has processed, a return contract that turns source changes into target actions, and evidence in the source of what changed. This page specifies each. [Incremental load via bookmarks](../lakehouse/incremental.md) builds the pipeline step by step with a Lakehouse Folder source, and [the Warehouse task](../warehouse/incremental.md) does the same over a Warehouse source. [Load behaviour](operation-behaviour/load.md) owns selection, reload and failure outcomes.

Incremental loading and [incremental Build selection](../estate/selective-runs/build-selection.md) answer different questions. Build selection decides which definitions to install. Incremental loading decides which source changes an installed Table or Folder applies, and an ordinary data change needs no Build:

```text
initial Build + first Load
→ change source data only
→ Load again without Build
```

## Why `max(...)` is not enough

The obvious way to read only what changed is to ask the target how far it got and read the source from there. Suppose `Parcel.LiveStatus` kept a `[Source update datetime]` column copied from each source row:

```sql
select [Parcel ID], [Status], [Depot]
from [Source].[Parcel]
where [Row update datetime] > (
    select max([Source update datetime]) from [Parcel].[LiveStatus]
);
```

That holds until the target's data stops mirroring the source's changes, which it routinely does:

- **A change can leave no row behind.** A cancelled parcel becomes a delete key, not a target row. If the cancellation is the newest change, the target's maximum stays behind it and every later Load reads it again. A deleted file leaves no timestamp at all.
- **Several sources have several clocks.** A Table built from a join has an audit column per source, advancing at different rates. No single maximum says how far it has read each one.
- **A window with no changes writes nothing.** The target cannot show that a Load ran and found nothing.
- **A maximum cannot tell a clean boundary from a partial one.** It reflects whatever rows the target holds, including those from a Load that applied only part of its input.

A bookmark records progress rather than inferring it from the data. Weaver keeps one per consumer, sets it to the instant before a Load began, and advances it only when that Load completes cleanly, including a Load that found nothing. A change that lands while the Load is running is read again by the next one rather than missed. Weaver compares what it reads with the target and applies only genuine inserts and updates, so reading a change twice does not duplicate it.

## Worked example: files, a Delta Table and a Warehouse Table

The same idea runs through three consumers: a Folder that snapshots files in a Lakehouse, a Delta Table that reads that Folder's changes, and a Warehouse Table that reads a changing Warehouse source. Each stage below shows the declaration, one source change and what the next Load did, so the bookmark can be followed from the first Load to the empty window. Provisioning the external source, Build and the dry-run previews are in the two tasks, [Incremental load via bookmarks](../lakehouse/incremental.md) for the Lakehouse stages and [for the Warehouse stage](../warehouse/incremental.md); this section picks up from the installed definitions.

The data is the same in every stage: two parcels, `P-1001` in transit at Central and `P-1002` delivered at South. The source then changes so that `P-1001` is delivered and `P-1002` is gone. The change leaves the declarations untouched, so no stage runs Build between its two Loads.

### Lakehouse files: a snapshot Folder

Carrier status arrives as one CSV file per parcel in an external archive Lakehouse, `ParcelSourceArchive`, outside Weaver's targets. A physical Folder Shortcut presents that archive inside the managed `Landing` Lakehouse:

```python title="Lakehouse/Landing/shortcuts.py"
from weaver import Shortcut


Parcel__StatusSource = Shortcut(
    shortcut_type="folder",
    target_type="physical",
    target="Lakehouse/ParcelSourceArchive/Files/parcel-status",
)
```

The Folder copies that source into Weaver's staging area on every Load:

```python title="Lakehouse/Landing/Files/Parcel__StatusFiles.py"
"""
Folder ID: Parcel.StatusFiles

Description: Current parcel status snapshots, one CSV file per parcel.

Lineage: A carrier snapshot represented by this example.

File key: "*.csv"

Incremental: false
"""

import shutil

from shortcuts import Parcel__StatusSource
from weaver import Folder


class Parcel__StatusFiles(Folder):
    def read(self):
        source_root = Parcel__StatusSource(self).path()
        if not source_root.is_dir():
            raise FileNotFoundError(
                f"Parcel status source directory not found: {source_root}"
            )

        staging = self.staging_folder()
        for source in sorted(source_root.glob("*.csv")):
            shutil.copy2(source, staging.path / source.name)
        return staging
```

The Folder is not incremental, and it does not need to be. Each Load hands Weaver the complete current snapshot, and Weaver compares it with the managed Folder and records what changed: which paths were inserted, which were updated and which were deleted, each with the time of the event. A byte-identical file is not an update. That record is the change feed. The Folder produces it, and a consumer reads it with its own bookmark.

The source check runs before Weaver issues or populates staging, so an unavailable source raises `FileNotFoundError`, while an existing but empty directory is a valid empty snapshot.

The first Load publishes both files. The Folder reports two insertions.

### Lakehouse Delta Table: the consumer

`Parcel.LiveStatus` keeps one row per parcel. It asks the Folder for everything that changed after its own bookmark and turns removed files into explicit delete keys:

```python title="Lakehouse/Landing/Tables/Parcel__LiveStatus.py"
"""
Table ID: Parcel.LiveStatus

Description: The latest status supplied for each parcel.

Lineage: Parcel status snapshots managed by Parcel.StatusFiles.

Primary key: Parcel ID

Incremental: true

Schema:
  Parcel ID: string
  Status: string
  Depot: string
"""

from Files.Parcel__StatusFiles import Parcel__StatusFiles
from weaver import Table


class Parcel__LiveStatus(Table):
    def read(self):
        source = Parcel__StatusFiles(self)
        bookmark = self.bookmark()
        changed = source.files_since(bookmark)
        deleted = source.deleted_since(bookmark)

        staged = None
        if changed:
            root = source.spark_path()
            staged = (
                self.spark.read.option("header", True)
                .csv([f"{root}/{path.name}" for path in sorted(changed)])
                .select(*self.columns())
            )

        deletes = None
        if deleted:
            parcel_ids = [(path.stem,) for path in sorted(deleted)]
            deletes = self.spark.createDataFrame(parcel_ids, ["Parcel ID"])

        if staged is None and deletes is None:
            return None
        return staged, deletes
```

Three things in this code do the work:

- `self.bookmark()` is read once and passed to both calls. On the first Load it is `1900-01-01`, so `files_since()` returns both files.
- A removed file leaves no row behind, so the Table derives the delete key from its filename: `P-1002.csv` becomes the `Parcel ID` `P-1002`.
- When nothing changed, `read()` returns `None`. The Load succeeds without touching the target, and the bookmark still advances.

The Folder import establishes the managed dependency, so an item-wide Load runs `Parcel.StatusFiles` before `Parcel.LiveStatus`.

After the first Load, the Table holds both parcels. In a **SQL query connected to the catalogue Warehouse**, the Table's bookmark is the instant just before that read began. A Lakehouse Table is addressed in the catalogue by schema name `Tables/Parcel`:

```sql
select [Bookmark datetime]
from [_].[Bookmark]
where [Item type] = N'Lakehouse'
  and [Item name] = N'Landing'
  and [Schema name] = N'Tables/Parcel'
  and [Object name] = N'LiveStatus';
```

Now change the source and leave both declarations alone. In a notebook with `ParcelSourceArchive` attached as its default Lakehouse, replace one file and delete the other:

```python
from pathlib import Path

source_root = Path("/lakehouse/default/Files/parcel-status")
(source_root / "P-1001.csv").write_text(
    "Parcel ID,Status,Depot\nP-1001,Delivered,Central\n",
    encoding="utf-8",
)
(source_root / "P-1002.csv").unlink()
```

```bash
weaver load Lakehouse/Landing
```

The Folder snapshot now differs from the managed Folder by one updated path and one deleted path, and the Folder reports one update and one deletion. The Table's window, everything after its previous boundary, contains both events. `files_since()` returns `P-1001.csv`, which becomes an update, and `deleted_since()` returns `P-1002.csv`, which becomes a delete by primary key. The Table also reports one update and one deletion, and its only row is `P-1001`, now `Delivered`. The Folder's and the Table's counts are summed in the Load summary, so the summary shows two updates and two deletions for what is one business change.

Run the same Load again without changing the source. The Folder reports no changes, `read()` returns `None`, the Table's rows stay as they were and its bookmark advances to the new instant.

### Warehouse Table: a SQL consumer

A Warehouse has no Folder history, so the source carries its own change evidence: each row in `[Source].[Parcel]`, held in a separate `ParcelSource` Warehouse that Weaver does not manage, carries a `[Row update datetime]`. A physical Shortcut presents it inside `Warehouse/Operations` as the item-local View `[Source].[Parcel]`:

```yaml title="Warehouse/Operations/shortcuts.yml"
physical:
  "Warehouse/Operations/Source.Parcel": "Warehouse/ParcelSource/Source.Parcel"
```

The consumer is a T-SQL Table. The SQL reads its own bookmark from the catalogue and returns two result sets, the rows to upsert and the keys to delete:

```sql title="Warehouse/Operations/Parcel.LiveStatus.sql"
/*
Table ID: Parcel.LiveStatus

Description: Current state of active parcels.

Lineage: Parcel records supplied through the physical Source.Parcel Shortcut.

Primary key: Parcel ID

Incremental: true

Dependencies: []

Schema:
  Parcel ID: varchar(20)
  Status: varchar(30)
  Depot: varchar(30)
*/
declare @bookmark_datetime datetime2(6);
set @bookmark_datetime = coalesce(
    (
        select [Bookmark datetime]
        from [_].[Bookmark]
        where [Item type] = N'Warehouse'
          and [Item name] = N'Operations'
          and [Schema name] = N'Parcel'
          and [Object name] = N'LiveStatus'
    ),
    cast('1900-01-01' as datetime2(6))
);

-- Rows to insert or update
select [Parcel ID]
     , [Status]
     , [Depot]
from [Source].[Parcel]
where [Row update datetime] > @bookmark_datetime
  and [Status] <> 'Cancelled';

-- Keys to delete
select [Parcel ID]
from [Source].[Parcel]
where [Row update datetime] > @bookmark_datetime
  and [Status] = 'Cancelled';
```

Four details differ from the Lakehouse stage:

- **The Table reads the bookmark itself.** Every installed Warehouse sees the catalogue's `_.Bookmark` as a view, so the `select [Bookmark datetime] from [_].[Bookmark]` is an ordinary query on the four-part key. The `coalesce` supplies the initial boundary if no row exists yet.
- **The source's audit column does the work that `files_since()` did.** `[Row update datetime]` says when a source row changed and `@bookmark_datetime` says how far this Table has read, so comparing them selects the window.
- **A cancellation is a delete claim, not a row.** The first result set filters `Cancelled` out, and the second returns those parcels' keys. A parcel absent from the first result set is left alone, because absence is not a delete.
- **`Dependencies: []` is required.** T-SQL inference does not resolve `[Source].[Parcel]` to a physical Shortcut. The override removes a managed producer edge that does not exist; it does not remove the need to read the source.

The first Load reads both source rows, because the boundary is `1900-01-01`, and inserts them. The catalogue then holds this Table's bookmark, which can be read with the same query the Table itself uses.

Change the source. Each update sets the row's audit datetime, which is later than the bookmark:

```sql
update [Source].[Parcel]
set [Status] = 'Delivered',
    [Row update datetime] = sysutcdatetime()
where [Parcel ID] = 'P-1001';

update [Source].[Parcel]
set [Status] = 'Cancelled',
    [Row update datetime] = sysutcdatetime()
where [Parcel ID] = 'P-1002';
```

```bash
weaver load Warehouse/Operations
```

The window contains both rows. `P-1001` arrives in the first result set and updates the target to `Delivered`. `P-1002` arrives in the second, as a delete key, so a source update becomes a target deletion. The Load reports one update and one deletion, and the target holds one row:

| Parcel ID | Status | Depot |
| --- | --- | --- |
| P-1001 | Delivered | Central |

`ParcelSource` still holds `P-1002` as `Cancelled`; Weaver deletes from its own target, never from the source. A further Load with no source change reads an empty window, leaves the target unchanged and advances the bookmark again.

One limit applies to this query and to any audit-datetime predicate. A hard deletion in the source leaves no row for either result set, so it can never reach the target. Propagating it needs retained evidence: a tombstone, an audit table or CDC, kept until the consumer has read it.

### What differs between the consumers

| | Lakehouse Delta Table | Warehouse Table |
| --- | --- | --- |
| Change evidence | The Folder's record of inserted, updated and deleted paths | `[Row update datetime]` on each source row |
| Reads its bookmark with | `self.bookmark()` | `select … from [_].[Bookmark]` |
| Bookmark key in `_.Bookmark` | Schema name `Tables/Parcel` | Schema name `Parcel` |
| Delete claim from | The filename of a deleted path | A cancelled row |
| Empty window | `read()` returns `None` | Both result sets are empty |

In both, the declarations stayed as they were, the second Load saw only the window since the first one's boundary, and each consumer's bookmark moved independently of the source's own timestamps.

## Return contract

An incremental Table returns candidate rows to insert or update and, when needed, the keys of rows to delete. A row that is absent from the candidates stays in the target; absence is not a delete. A Python Table declared with `Incremental: true` has `read()` return one of four forms:

| Return value | Meaning |
| --- | --- |
| `staging` | Insert or update candidates, with no delete claim. |
| `(staging, deletes)` | Insert or update candidates and explicit delete keys. |
| `None` | No candidates and no deletes. The load succeeds as a no-op. |
| `(None, deletes)` | Deletion-only work. Weaver supplies an empty staging frame with the target shape. |

`staging` holds every declared business column. `deletes` holds the declared primary-key columns, so an incremental Table requires a primary key. A SQL-authored Table expresses the same contract as result sets: the first supplies the candidates and an optional second supplies delete keys. An incremental Folder may return `(staging_folder, files_to_delete)`. [Table](weaver-documents/table.md#body-and-return-contract), [Folder](weaver-documents/folder.md) and [Python authored objects](python/objects.md) own the accepted forms.

A source operation does not have to become the same target operation. After filters, joins or aggregation, a source update can produce a target delete, as the cancellation of `P-1002` does above. The target query decides which target keys to delete, from CDC tombstones, cancellations, deleted files, an API status or any other source it can read.

> **Design background:** [Responding to change](https://principlesofdataengineering.org/docs/efficient-stable-pipeline/responding-to-change/) covers translating source changes into target actions.

## Bookmark

A bookmark is the UTC instant immediately before a consumer's latest clean Load began. It is stored in `_.Bookmark`, keyed by item type, item name, schema name and object name, and holds `1900-01-01` until the object has had a clean Load.

- **One per consumer.** The Table or Folder owns it, not the source. Two Tables reading the same Folder keep separate boundaries, and loading one does not move the other's.
- **Advances only on a clean Load.** A clean no-op counts. Failed, rejected, blocked, pending and static-skip outcomes leave it where it was, and a dry run writes nothing. A fault-tolerant Load that publishes accepted rows alongside rejects does not advance it either, so the next Load starts from the last clean boundary.
- **Resets on rebuild.** Build resets the bookmark of every loadable object it rebuilds, because the new generation has not processed any history. `--reload` resets it for each reached Table. The next Load therefore asks the source for all available history. After a Build, `weaver load --stale` runs the objects whose state is no longer Green.

[Catalogue schema](catalogue-schema.md#_bookmark) lists the columns.

## Reading the bookmark

| Authored in | Read it with |
| --- | --- |
| Python Table or Folder | `self.bookmark()`, a timezone-aware UTC `datetime`. It requires a catalogue. |
| Python Folder source | `files_since(bookmark)` and `deleted_since(bookmark)` on the source Folder |
| T-SQL Table | A `select` from `[_].[Bookmark]` on the four-part key. Each installed Warehouse sees `_.Bookmark` as a view. |

`files_since()` returns the Folder's current managed files whose latest event is strictly after the bookmark. `deleted_since()` returns paths whose latest event is a deletion after it; those paths normally no longer exist, so the Table maps them to its own keys. `latest_files()` returns the current files from the newest change that left files in place.

## Source change evidence

The bookmark says where the consumer stopped. What counts as a change after that point is the source's business, so each source needs its own evidence:

| Source | Change evidence |
| --- | --- |
| Table with audit datetimes | A predicate such as `where [Row update datetime] > @bookmark_datetime`. |
| Database with CDC or a change table | The change rows after the boundary. |
| Weaver-managed Folder | `files_since()` and `deleted_since()`. |
| API | A cursor, usually with an overlap or polling window. |

One consumer owns one bookmark, but a query over several sources interprets that boundary once per source. The query combines the source-specific readings into candidates and delete keys.

Each approach has a condition. The source has to keep a row or other evidence of every change until the consumer has read it, and audit datetimes have to share the bookmark's UTC time basis. A hard source deletion leaves no row for either result set, so propagating it needs retained evidence such as a tombstone, an audit table or CDC.

> **Design background:** [Tracking changes](https://principlesofdataengineering.org/docs/efficient-stable-pipeline/tracking-changes/) covers how a source can record what changed. The contract on this page is self-contained.

## Declaration changes

An edit to a Table or Folder takes effect only after Check and Build. The rebuild resets that object's bookmark, so the next Load reads all available history rather than the changes since the old boundary. That combines a declaration change, Build impact and a bookmark reset with the data change being measured, which is why editing a constant in a Weaver document and rebuilding it does not demonstrate an incremental load. Keep the data-only sequence for that.

[Load behaviour](operation-behaviour/load.md) owns exact bookmark, reload and selection rules. [Row auditing and operational history](../estate/catalogue-and-health/row-auditing.md) explains where current state and Load activity are recorded.
