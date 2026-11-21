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

## One consumer across three Loads

The Warehouse task loads two parcels, changes the source so that `P-1001` is delivered and `P-1002` is cancelled, then loads again without changing anything. The bookmark moves like this:

| Load | Source changes after the bookmark | Target action | Bookmark afterwards |
| --- | --- | --- | --- |
| First | Everything: the bookmark is `1900-01-01`. `P-1001` is In transit and `P-1002` is Delivered. | Insert both rows. | t₁, the instant before this Load began. |
| Second | `P-1001` is now Delivered and `P-1002` is Cancelled. | Update `P-1001`. Delete `P-1002` by key. | t₂, a later instant. |
| Third | None after t₂. | None. | t₃, advanced by the empty window. |

The source's `[Row update datetime]` says when a source row changed. The bookmark says how far this consumer has processed. They are different quantities, and a query compares one with the other.

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
| T-SQL Table | a `select` from `[_].[Bookmark]` on the four-part key |

In Python, a Table that consumes a managed Folder passes its own bookmark to the Folder:

```python
changed = source.files_since(self.bookmark())
deleted = source.deleted_since(self.bookmark())
```

`files_since()` returns the Folder's current managed files whose latest event is strictly after the bookmark. `deleted_since()` returns paths whose latest event is a deletion after it; those paths normally no longer exist, so the Table maps them to its own keys, usually from the filename. `latest_files()` returns the current files from the newest change that left files in place.

In a Warehouse, the catalogue's `_.Bookmark` is projected as a view in each installed Warehouse, so the Table's own query can read its boundary. The `coalesce` supplies the initial boundary when no row exists yet:

```sql
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
```

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

## Folders

A Folder that is not incremental takes a complete snapshot of its source on every successful Load, so a source file that disappears is retired from the managed Folder. Weaver records the inserted, updated and deleted managed paths, and a byte-identical file is not an update.

The source check runs before Weaver issues or populates staging. An unavailable source raises `FileNotFoundError`. An existing but empty source directory passes and is a valid empty snapshot.

A Table that reads such a Folder gets a managed dependency from the Folder import, so an item-wide Load runs the Folder first. A physical Shortcut import inside the Folder records an external boundary, not a managed producer.

## Declaration changes

An edit to a Table or Folder takes effect only after Check and Build. The rebuild resets that object's bookmark, so the next Load reads all available history rather than the changes since the old boundary. That combines a declaration change, Build impact and a bookmark reset with the data change being measured, which is why editing a constant in a Weaver document and rebuilding it does not demonstrate an incremental load. Keep the data-only sequence for that.

[Load behaviour](operation-behaviour/load.md) owns exact bookmark, reload and selection rules. [Row auditing and operational history](../estate/catalogue-and-health/row-auditing.md) explains where current state and Load activity are recorded.
