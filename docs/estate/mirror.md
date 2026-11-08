# Develop using Mirror

Development sometimes needs an estate's existing data without a separate load of every unchanged object. Mirror establishes a baseline that borrows that data, using the same project files with a separate configuration for development targets. Objects you change become local through Build, while unchanged objects can continue to borrow from the source.

Use Mirror only after the [ordinary development loop](development-cycle.md) is understood. **It empties and reconstructs the destination catalogue and every selected destination target**, including local materialisations there. Source items remain untouched. It is a baseline reset, not an iteration command.

## Prepare existing destinations in the same workspace

This first baseline keeps source and destination in one workspace; [mirror from another workspace](#mirror-from-another-workspace) covers a separate development workspace. The starting point is the [connected Landing/Operations project](connected-items.md) and its installed estate: the `Catalogue` Warehouse, the `Operations` Warehouse it records, and Landing supplying the connected `Parcel.LakehouseCurrentStatus` Table. Mirror needs existing empty destination Warehouses for the catalogue and Operations; it does not create Fabric items.

1. In the Fabric portal, create two Warehouses in `Parcel Development`: `CatalogueDev` and `OperationsDev`.
2. Add a separate configuration beside the project. Keep `workspace-development.yml` as it is; this file describes the mirrored copy:

```yaml title="workspace-mirror.yml"
workspace: Parcel Development
catalogue: Warehouse/CatalogueDev
mirror: Warehouse/Catalogue

targets:
  Warehouse/Operations: OperationsDev
```

`mirror` names the source catalogue; `catalogue` and `targets` name the destinations. The source physical item, `Operations`, comes from the source catalogue's recorded binding, not from this file. Only the items listed under `targets` are rebound to development copies.

In the Terminal, Weaver shows the source catalogue, destination catalogue and each target mapping, then asks once before emptying the destinations. Compare the plan with the names above; answer `y` only if they match. Declining changes nothing. In a Notebook, review the plan in the first cell before running the second. Mirror has no dry-run mode.

Run Mirror:

```bash
weaver mirror --workspace-config workspace-mirror.yml
```

<!-- cli-capture: {"id": "140-mirror", "title": "Mirror · fork the catalogue into development"} -->
<p class="terminal-intro">The command returned:</p>
<figure class="weaver-terminal" aria-label="Mirror · fork the catalogue into development">
<figcaption>Terminal output <span class="terminal-exit">exit 0</span></figcaption>
<pre tabindex="0" aria-label="Terminal output"><code>Mirror

Workspace              Parcel Development
Source catalogue       Warehouse/Catalogue
Destination catalogue  Warehouse/CatalogueDev
Targets
  Warehouse/Operations → Warehouse/OperationsDev

Empty these targets? This cannot be undone. [y/N] y

Mirror

  Planning the mirror                                                                                      1.8s
→   Wipe Warehouse/CatalogueDev · 1 action
→   Wipe Warehouse/OperationsDev · 1 action
<span class="terminal-status-green">✓   Wipe Warehouse/CatalogueDev · 1 action                                                                 0.7s</span>
→   Warehouse/CatalogueDev · Catalogue: creating schemas · 1 action
<span class="terminal-status-green">✓   Wipe Warehouse/OperationsDev · 1 action                                                                0.7s</span>
<span class="terminal-status-green">✓   Warehouse/CatalogueDev · Catalogue: creating schemas · 1 action                                        0.0s</span>
→   Warehouse/CatalogueDev · Catalogue: building objects · 24 actions
→   Reconstruct Warehouse/OperationsDev · 2 actions
→   Recreate views over other items in Warehouse/OperationsDev · 1 action
<span class="terminal-status-green">✓   Reconstruct Warehouse/OperationsDev · 2 actions                                                        0.2s</span>
<span class="terminal-status-green">✓   Recreate views over other items in Warehouse/OperationsDev · 1 action                                  0.4s</span>
<span class="terminal-status-green">✓   Warehouse/CatalogueDev · Catalogue: building objects · 24 actions                                      6.9s</span>
→   Warehouse/CatalogueDev · Catalogue: updating catalogue definitions · 1 action
<span class="terminal-status-green">✓   Warehouse/CatalogueDev · Catalogue: updating catalogue definitions · 1 action                          4.4s</span>
→   Warehouse/CatalogueDev · Catalogue: finalising catalogue · 1 action
<span class="terminal-status-green">✓   Warehouse/CatalogueDev · Catalogue: finalising catalogue · 1 action                                    0.7s</span>
→   Recreate catalogue views in Warehouse/OperationsDev · 1 action
<span class="terminal-status-green">✓   Recreate catalogue views in Warehouse/OperationsDev · 1 action                                         0.1s</span>
→   Copy procedures and functions into Warehouse/OperationsDev · 1 action
<span class="terminal-status-green">✓   Copy procedures and functions into Warehouse/OperationsDev · 1 action                                  0.3s</span>
→   Warehouse/CatalogueDev · Forking the catalogue and binding items · 1 action
<span class="terminal-status-green">✓   Warehouse/CatalogueDev · Forking the catalogue and binding items · 1 action                            7.8s</span>
  Mirroring                                                                                               20.9s
<span class="terminal-status-green">✓ Mirror                                                                                                  24.4s</span>

Mirror complete
  Catalogue  Warehouse/Catalogue → Warehouse/CatalogueDev
  1 item mirrored
  2 destinations emptied
</code></pre>
</figure>
<!-- /cli-capture -->

Mirror emptied CatalogueDev and OperationsDev and rebuilt them from the source estate. Unchanged objects start as borrowed source data: OperationsDev presents Operations' Tables through local Views, and `_.Mirror` in CatalogueDev lists every borrowed object. The project's logical items and Weaver documents are unchanged.

Inspect the baseline:

```bash
weaver health --workspace-config workspace-mirror.yml
```

<!-- cli-capture: {"id": "141-mirror-health", "title": "Health · the mirrored development estate"} -->
<p class="terminal-intro">The command returned:</p>
<figure class="weaver-terminal" aria-label="Health · the mirrored development estate">
<figcaption>Terminal output <span class="terminal-exit">exit 1</span></figcaption>
<pre tabindex="0" aria-label="Terminal output"><code>Health

  Read catalogue                                                                                           3.4s
  Read the mirrored catalogue                                                                              1.9s
  Check installed items                                                                                    0.2s
  Read installed objects                                                                                  17.1s
<span class="terminal-status-green">✓ Health                                                                                                  22.6s</span>

<span class="terminal-status-amber">Weaver Health  Amber</span>

<span class="terminal-status-green">Load    Green</span>
  Last load activity   0h 1m ago
<span class="terminal-status-green">  15 succeeded</span>

<span class="terminal-status-amber">Tests   Amber</span>
<span class="terminal-status-green">  4 succeeded</span>
<span class="terminal-status-amber">  Amber  Warehouse/Operations/Parcel.CurrentStatusMatches</span>
<span class="terminal-status-green">          Warehouse/Operations/Parcel.StatusEvent has been loaded since this validation passed</span>
<span class="terminal-status-amber">  Amber  Warehouse/Operations/Parcel.StatusIsKnown</span>
<span class="terminal-status-green">          Warehouse/Operations/Parcel.StatusEvent has been loaded since this validation passed</span>

<span class="terminal-status-green">Build   Green</span>
  Installed estate consistent (67 objects)

Slowest loads
  Warehouse/Operations/Parcel.LakehouseCurrentStatus  6.6s
  Warehouse/Operations/Parcel.Daily                   4.9s
  Warehouse/Operations/Parcel.LiveStatus              2.5s
  Warehouse/Operations/Parcel.StatusEvent             2.5s
  Warehouse/Operations/Reference.Depot                2.2s

Largest changes
  Warehouse/Operations/Parcel.StatusEvent     read 3  +3 ~0 -0 !0
  Warehouse/Operations/Parcel.Daily           read 1  +1 ~0 -1 !0
  Warehouse/Operations/Parcel.Events          read 1  +1 ~0 -1 !0
  Warehouse/Operations/Parcel.RawEvents       read 1  +1 ~0 -1 !0
  Warehouse/Operations/Parcel.Summary         read 1  +1 ~0 -1 !0
</code></pre>
</figure>
<!-- /cli-capture -->

Health reads borrowed objects' Load state from the source catalogue, so the mirrored estate starts with the source's history and findings.

See [Mirrors](../core-concepts/mirrors.md) for borrowed and local data. Exact Mirror selection, authorisation and failure boundaries are in [Mirror operation behaviour](../reference/operation-behaviour/mirror.md).

## Change only the work that needs to become local

After a successful Mirror, the same project source and [development cycle](development-cycle.md#edit-and-iterate) apply. The difference is the destination: Build, Load, Test and Health use `--workspace-config workspace-mirror.yml` to operate the mirrored estate.

Correct an earlier event's depot in the required `Warehouse/Operations/Parcel.StatusEvent.sql`. Replace this row:

```sql
    ('P-1001', 1, 'Accepted', 'North'),
```

with:

```sql
    ('P-1001', 1, 'Accepted', 'East'),
```

Keep the key, remaining rows and metadata intact. This changes event history, not P-1001's latest status. Check, preview and install it against the mirrored destinations:

```bash
weaver check
weaver build --item Warehouse/Operations --dry-run --workspace-config workspace-mirror.yml
weaver build --item Warehouse/Operations --workspace-config workspace-mirror.yml
weaver load Warehouse/Operations --stale --workspace-config workspace-mirror.yml
weaver test Warehouse/Operations --workspace-config workspace-mirror.yml
```

Review the preview before applying Build. In Fabric, query `Parcel.StatusEvent` in **OperationsDev** and **Operations**. P-1001's sequence 1 should now read `Accepted / East` in development and still `Accepted / North` at the source. Sequence 2 remains `In transit / Central` in both, so the generated current-status Test and known-status Assumption should still pass.

Compare the connected `Parcel.LakehouseCurrentStatus` Table too: it stays borrowed, presented as a View in OperationsDev over the unchanged source data. You corrected one branch without copying or reloading that independent Table. Keep the [connected Landing/Operations project](connected-items.md) for this comparison.

Build compares source with copied installed declarations. The changed StatusEvent and its affected selected CurrentStatus View become local after successful installation; unchanged borrowed objects stay borrowed. For each object made local, its `_.Mirror` row is marked deleted and remains as a record of the catalogue mirrored. Items outside the Build selection do not materialise just because another item changed. Load operates local materialisations; borrowed data continues to be loaded and owned at its source.

Warehouse borrowed Tables/Views are presented through local Views. Lakehouse stored Tables/Folders use shortcuts, with local wrapper Views for source Views. Health reads borrowed current Load state from the source catalogue and local state from development. Development can therefore combine borrowed and locally materialised objects.

Selected changed or impacted protected Tables/Folders use preserving materialisation rather than empty reconstruction: Warehouse CTAS, Delta shallow clone or native recursive Folder copy. That path retains the established bookmark but is not an atomic estate snapshot; shallow clones require source file retention. Protection does not protect against Wipe or deliberate re-mirroring. Keep irreplaceable source data outside ordinary managed target ownership. See [Protecting data](../advanced/protecting-data.md).

## Mirror from another workspace

A separate development workspace can borrow production Lakehouse data directly. Mirror reads a source catalogue in another workspace and borrows its Lakehouses across the boundary. A Warehouse borrows through Views, which read only their own workspace, so the Warehouse is built in development instead.

Suppose `Parcel Production` holds the estate from [workspace mappings](environments.md#keep-development-and-production-bindings-separate): the `ParcelCatalogue` catalogue, the `ParcelLanding` Lakehouse and the `ParcelOperations` Warehouse. In a separate workspace, `Parcel Sandbox`, create three empty items with the same names: Warehouses `ParcelCatalogue` and `ParcelOperations`, and Lakehouse `ParcelLanding`. Then describe the sandbox beside the project:

```yaml title="workspace-sandbox.yml"
workspace: Parcel Sandbox
catalogue: Warehouse/ParcelCatalogue
environment: Parcel Development/Weaver
mirror: Parcel Production/Warehouse/ParcelCatalogue

targets:
  Lakehouse/Landing: ParcelLanding
  Warehouse/Operations: ParcelOperations
```

`mirror` names the source catalogue with its workspace. `catalogue` and `targets` are always in `workspace`. Mirror binds each source item by its Fabric IDs, so the sandbox can reuse production's names. Mirroring a Lakehouse runs Spark work, so `environment` names a published Weaver Environment; this one reuses the Environment in `Parcel Development`.

Mirror, and later Load, Test and Health, read `Parcel Production`. The identity running them needs read access to the production catalogue and `ParcelLanding`; see [Permissions](../reference/permissions.md).

Mirror only the Lakehouse:

```bash
weaver mirror --item Lakehouse/Landing --workspace-config workspace-sandbox.yml
```

Without `--item`, Mirror selects every configured target, and `Warehouse/Operations` is refused before anything is emptied. Mirror asks once before emptying the sandbox's `ParcelCatalogue` and `ParcelLanding`.

The sandbox's `ParcelLanding` now presents production's Tables and Folders through shortcuts into `Parcel Production`, with local wrapper Views over its Views. Mirror read production's catalogue rows over T-SQL and wrote them into the sandbox's `ParcelCatalogue`. The sandbox catalogue claims only items in `Parcel Sandbox`: `Warehouse/Operations`, left in production, is not claimed.

Build and load the Warehouse in the sandbox:

```bash
weaver build --item Warehouse/Operations --workspace-config workspace-sandbox.yml
weaver load Warehouse/Operations --workspace-config workspace-sandbox.yml
weaver health --workspace-config workspace-sandbox.yml
```

Build installs Operations into the sandbox's `ParcelOperations` as a new item. Its logical Shortcut to `Lakehouse/Landing` resolves to the sandbox's `ParcelLanding`, so Operations reads production's Landing data through the borrowed Tables. Load runs Operations' work in the sandbox; Landing stays borrowed and is loaded in production. Health reads the borrowed Landing objects' state from `ParcelCatalogue` in `Parcel Production`. Nothing in `Parcel Production` changes.

The shared Environment needs Read permission, and both workspaces must have the same capacity and network security settings. The sandbox supplies its own pool and compute settings; see [Running Python in Fabric](../lakehouse/runtime.md#use-a-shared-environment).

From here the development cycle is the one above: a changed Landing object becomes local in the sandbox when Build selects it.

## Reset only when a new source baseline is intended

Run Mirror again only when the displayed destination catalogue and selected targets should be replaced. Local work inside that boundary is not preserved as a fallback. Preflight failures leave destinations unchanged; a failure after mutation begins does not restore the old catalogue or targets and does not undo already completed destinations. Inspect remaining state before retrying.

Selective mirroring still copies the destination catalogue, but only selected items are rebound to development targets. Within one workspace, unselected copied installations remain source-bound; from another workspace, an unselected item there is left unclaimed for Build to install. A catalogue-only Mirror copies installed/current state without emptying an item target, and destination Log/LoadStatistic history starts empty. It is not an isolated writable copy of every source binding. Rebinding from an already mirrored source is refused rather than chaining borrowing hops.

[Mirror and materialisation strategies](../advanced/mirror-and-materialisation-strategies.md) explains these narrower estate shapes. [Mirror behaviour](../reference/operation-behaviour/mirror.md) owns exact selection, binding and failure rules. Once the baseline is in place, return to [ordinary development](development-cycle.md), not another reset.
