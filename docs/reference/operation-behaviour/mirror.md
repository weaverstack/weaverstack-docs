# Mirror behaviour

Mirror reconstructs a destination catalogue from another installed catalogue. It can also replace selected destination items with borrowed representations of their source installations.

## Source and destination

`mirror` / `--mirror` names the source catalogue. `catalogue` / `--catalogue` names the destination when a mirror source is configured or both values are supplied explicitly. Explicit values override the corresponding configuration values.

Without a configured `mirror`, configured `catalogue` is the source and a separate destination is required. With both configured, `mirror` is the source and `catalogue` is the destination.

The source is `Warehouse/Name` in the operation's workspace or `Workspace/Warehouse/Name` in another one. The destination is always in the operation's workspace; a destination qualified with another workspace is refused. Within one workspace, source and destination must be distinct Warehouses. A source in another workspace may share the destination's name.

The source must contain the catalogue tables required by this Weaver revision. A missing, unreadable or incompatible source fails before any destination is emptied. A source in another workspace must also record Fabric item IDs for its installations; a catalogue that records none is refused until a Build with this Weaver version has upgraded it.

Mirror reads the source catalogue and each selected source item in their own workspaces. While the destination still borrows objects, Load, Test and Health read their current state from the source catalogue there too, so `mirror` must stay configured and the identity running these operations needs read access to the source catalogue and items. See [Permissions](../permissions.md).

## Item selection

Repeatable `--item ITEM[=TARGET]` selects logical items. `ITEM` uses its configured destination; `ITEM=TARGET` supplies or overrides it. Naming no item selects every configured target. `--no-item` selects no item and copies only the catalogue; it is mutually exclusive with `--item`.

Each selected item must have a source installation. Selected logical items cannot repeat. Destination identities are type plus name: two selected outputs cannot share one physical target, collide with the destination catalogue, or overlap any source catalogue or item read by the same run. Only a source in the operation's workspace can overlap a destination; a source item in another workspace is bound by its Fabric IDs, so its destination may use the same name.

Each selected item is read in the workspace its source installation names. An installation that names no workspace is in the source catalogue's workspace. The installation is verified against Fabric there before any destination is emptied.

| Selected source item in another workspace | Result |
| --- | --- |
| Lakehouse | Mirrored. Its shortcuts and Spark wrapper Views read the source in its workspace, and its deployed Load and Test tree is copied from there. |
| Warehouse | Refused before any destination is emptied. A mirrored Warehouse borrows through Views, which read only their own workspace. Mirror it from within its own workspace, or select only Lakehouse items. |

A configuration that binds a Warehouse installed in another workspace therefore needs `--item` naming only its Lakehouses.

A source catalogue that holds `_.Mirror` has been a mirror itself. It may be copied in catalogue-only mode. Selected items cannot be rebound from it: borrowed state records one source hop, so a second hop is refused.

Recorded logical Shortcuts are resolved against the run's final bindings before mutation. A logical Shortcut to an item the run does not select keeps that item's recorded target, in the workspace its installation names. Physical Shortcuts retain their recorded workspace and item; one recorded without a workspace reads the source item's workspace. Selected producers precede selected consumers where a logical Shortcut requires that order; items in a cycle are ordered deterministically.

## Preflight and authorisation

The public operation has three boundaries:

1. `plan_mirror()` resolves workspace, catalogue roles and written item selection without reading Fabric.
2. `check_mirror()` proves the source, resolves source installations and final destinations, and checks borrowed relations, deployed work and recreatable Shortcuts without mutation.
3. `mirror()` executes the settled plan. An unresolved `MirrorPlan` is checked first; a `ResolvedMirror` is executed as supplied.

The CLI completes both planning and checking, displays the source, destination and selected mappings, then asks about that settled plan. Mirror has no dry-run mode.

An interactive CLI run requires confirmation unless `--yes` is present. JSON mode, a non-interactive run, or a run without a prompt requires `--yes`; otherwise nothing is changed. `--non-interactive` disables prompts and browser sign-in but does not authorise destruction.

Authorisation covers the destination catalogue and every displayed destination target. Existing contents in that scope are not preserved.

## Catalogue copy

Execution empties and rebuilds the destination catalogue against known-empty state and reconstructs selected targets. Only after every required reconstruction/readiness action succeeds are forked claims, borrowed records and final item bindings published in one final transaction. The copied state includes source item bindings, Registry certification, declaration dictionaries, dependencies, Shortcuts, bookmarks, and current Load and Test status. The destination keeps its own built-in catalogue installation.

Within one workspace, the transaction copies the rows server-side from the source Warehouse. A Warehouse names another Warehouse only within its own workspace, so for a source in another workspace Mirror reads the rows over TDS while checking the plan and the transaction writes them as literal values.

`_.Log` and `_.LoadStatistic` are rebuilt empty rather than copied. In catalogue-only mode, existing `_.Mirror` rows are copied.

Unselected logical items keep their copied source bindings, with one exception. When the source catalogue is in another workspace, an unselected item installed outside the destination's workspace is not claimed: the final transaction removes its copied claims, as [Unbind](unbind.md) would, and a later Build against the destination installs it there as a new item.

## Selected item state

Each selected destination target is emptied before its borrowed forms are created.

| Destination | Borrowed data | Local execution state |
| --- | --- | --- |
| Warehouse | Views over source Tables and Views; supported recorded Shortcuts become local Views | Required procedures and functions are copied into the destination |
| Lakehouse | OneLake shortcuts for Tables and Folders; source Views use local wrapper Views; recorded Shortcuts are recreated | The deployed Load and Test file tree is copied into the destination |

`_.Mirror` records each borrowed relation's source, including its workspace, and its physical form. All selected item bindings are published together after required borrowed forms, deployed work and readiness checks succeed. Copied code is local because execution is dispatched from the destination; it does not make borrowed data locally owned or loadable there.

A later Build compares project source with copied Registry certification and destination inventory. An unchanged borrowed object keeps its borrowed form and `_.Mirror` row. A changed or affected selected object has its recorded borrowed form removed and is installed locally. After the physical work, Build sets its `_.Mirror` row's `Row delete datetime`; the row stays as the record of the catalogue mirrored. Catalogue reads take only live rows, so the object is then local. The estate can therefore contain borrowed and local objects together. Edited protected borrowed Tables/Folders materialise with retained data/bookmarks; Warehouse CTAS, Folder copy and Delta shallow clone keep the source unchanged. A clone still depends initially on source files/retention. Failed materialisation cannot certify; ordinary unprotected replacement/reset rules differ.

## Failure, partial effects and re-mirroring

Planning and checking failures leave all destinations intact. Once execution starts, effects are not transactional:

1. the destination catalogue and selected targets are emptied/reconstructed under the action graph;
2. independent target branches may overlap, with endpoint/shortcut/readiness dependencies enforced; and
3. copied claims, Mirror records and all selected bindings publish together only after required reconstruction. Until that transaction commits the destination records no copied source installations.

A failure in catalogue rebuild or copy, target emptying, borrowed-form creation, deployed-work copy, Shortcut recreation, mirror recording or binding publication prevents successful final publication. Independent work may already have run or continue under the mutation failure policy. Earlier destructive/completed effects remain. No successful `MirrorResult` is returned for an incomplete run, and Weaver performs no operation-wide rollback.

Running Mirror again is a new reconstruction from the selected source. It empties the same settled destination scope again, so local materialisation inside that scope is replaced by a fresh borrowed baseline. This is a reset, not rollback or continuation of the earlier run.

A successful result reports `status: succeeded`, the workspace and catalogue pair, emptied destinations, copied and uncopied catalogue tables, selected logical items, and kind-specific work counts. See [JSON output](../ai-agents.md#json-output) for the current unversioned JSON shape.
