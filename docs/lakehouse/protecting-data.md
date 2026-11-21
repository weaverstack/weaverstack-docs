# Protecting data

Weaver treats the Tables and Folders it manages as reproducible. When a declaration changes, Build normally drops and recreates the affected object, and a later Load rebuilds its contents from source. That is the right behaviour for a derived Table. It is the wrong one for data that was costly to acquire and cannot be fetched again: an API history the provider no longer serves, a manually supplied workbook, an archive another team owns. Acquired source files usually land in a Lakehouse, but the choices below are the same for Warehouse Tables.

**Ownership should match recoverability.** Before you bring data under Weaver management, ask whether you can reconstruct the physical contents. For truly irreplaceable data, keep the contents in an external physical item and expose them through a physical Shortcut. If Weaver should own the object but Build must preserve its existing contents, declare `Prohibit rebuild: true`.

## Choose the ownership boundary

Choose the strongest boundary that fits the source:

| Situation | Pattern |
| --- | --- |
| Manually supplied Excel dump | External data + physical Shortcut |
| One-time historical source archive | External data + physical Shortcut |
| Another team owns the source | Physical Shortcut |
| Weaver Table accumulated through costly API calls | `Prohibit rebuild: true` |
| Weaver-managed Folder containing unrecoverable API responses | `Prohibit rebuild: true` |
| Ordinary reproducible derived Table | Normal Weaver management |

The distinction matters. A Shortcut keeps the data beyond Weaver's ownership boundary. `Prohibit rebuild` keeps the data inside that boundary and changes how Build reconciles an existing object.

## Keep irreplaceable sources outside Weaver ownership

A physical Shortcut fits a source that no repeatable process can reconstruct. Typical examples include:

- manually supplied Excel workbooks;
- one-off historical extracts;
- files supplied by another organisation;
- manually curated reference data;
- external archives; and
- any source without repeatable extraction.

Weaver manages the Shortcut destination in the local item: it may create, replace or remove that pointer as you change its declaration. Weaver does **not** manage the underlying physical source named by the Shortcut. This is the strongest ownership boundary because Build and Load do not treat the source contents as a Weaver-owned Table or Folder.

For example, a Lakehouse physical Folder Shortcut can expose an archive held in another workspace without making that archive part of the local estate's managed data. Follow [Connect data with Shortcuts](shortcuts.md) for the authoring workflow, and use the [Shortcut reference](../reference/weaver-documents/shortcut.md) for exact physical target forms and workspace rules.

## Retain an existing Weaver-owned object

Declare `Prohibit rebuild: true` on a Table, Folder or View when Weaver should own the object, but Build must not satisfy a change by dropping and recreating the existing physical object. Add the field to the document's metadata header:

```yaml
Prohibit rebuild: true
```

This is appropriate for Weaver-owned data such as:

- costly API history accumulated over many Loads;
- API history that the provider no longer makes available;
- a Folder containing retained external responses;
- an object whose reconstruction is expensive;
- history built from an upstream that exposes only current state; or
- data whose reconstruction would breach rate limits or operational constraints.

When planning finds an existing protected object that would otherwise be rebuilt, it records that object as prohibited and omits its physical drop and build actions. The existing object is retained; Build does not fail merely because the changed object is protected. Other work in the plan can continue, including installation of new objects. Catalogue metadata, certification and separately generated load work can still reconcile when the change does not require replacing the protected physical object.

A source change that requires a different physical shape does not update that shape in place. The old object remains. Review the plan and the resulting physical shape; the edited declaration is not necessarily materialised. [Build behaviour](../reference/operation-behaviour/build.md) owns the exact planning, certification and installation semantics; [Common metadata](../reference/weaver-documents/common-metadata.md) owns the accepted field and default.

## A protected borrowed object can become local without resetting its contents

For selected changed/impacted protected Tables and Folders in a Mirror, Build uses a preserving materialisation path rather than dropping the borrowed data and starting empty. Warehouse Tables use native CTAS after removing the destination wrapper View. Lakehouse Tables use a Delta shallow clone after removing the shortcut; Folders use native recursive copy. The retained bookmark is not reset for that materialisation. Ordinary unprotected reconstruction has a different boundary.

Inspect the Build preview, because removing the destination pointer is still a destructive destination change. The source is retained, but a failed copy/clone can leave incomplete destination state; there is no whole-operation rollback. A Delta shallow clone still depends on retained source files, so this is not independent backup storage. A Folder copy is not a guaranteed atomic snapshot while its source changes. If you need that stronger guarantee, preserve or migrate the data deliberately.

## Know what `Prohibit rebuild` does not do

**Warning:** `Prohibit rebuild` guards destructive replacement during Build only. It is not consulted as a general data-retention policy by Load, reload, Wipe, or Mirror.

`Prohibit rebuild` is a Build replacement guard, not a general freeze:

- A normal Load can insert, update, or delete data according to the installed Table or Folder contract.
- `weaver load --reload` empties each reached selected Table before reconstructing it from the initial bookmark boundary.
- Wipe removes managed contents within its confirmed destructive scope.
- Re-mirroring empties and reconstructs the selected destination catalogue and targets.
- The flag does not prevent first installation when no existing physical object is present.
- It does not put the physical object outside Weaver ownership.
- It does not protect an external target behind a Shortcut; that target is already outside Weaver ownership.

A non-destructive metadata or load-logic change may therefore be installed while the physical object remains in place. A change requiring destructive recreation does not replace the existing object. If the physical shape must change, preserve or migrate the data deliberately before you remove the protection or the existing object.

## Revisit the choice when recovery changes

Recoverability can change independently of your code. A repeatable upstream may stop retaining history, a manual archive may gain a governed extraction process, or an API may impose new limits. When that happens, reassess both questions:

1. Should Weaver own the physical data at all?
2. If it should, can Build recreate the object without unacceptable loss or cost?

If the answer to the first question is no, a physical Shortcut fits. If the first answer is yes and the second is no, `Prohibit rebuild` fits. If both answers are yes, ordinary Weaver ownership fits.
