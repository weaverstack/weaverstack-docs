# Work across teams' catalogues

When your tables depend on another team's data, give Health both teams' catalogues to assess the connected work. For Load or Test, also choose the items or workspaces to run. Each team keeps its own project and catalogue, while Weaver coordinates the selected work in dependency order.

Build stays within one catalogue. Each team builds its own items as usual; joining happens only when an operation reads several catalogues together.

## Before you start

You need two teams' projects, each built into its own workspace and catalogue. In this page the Operations team works in `Parcel Operations` and the Planning team in `Depot Planning`; each workspace has a catalogue Warehouse named `Catalogue`.

The Planning team's Lakehouse reads the Operations team's Warehouse Table through a physical Shortcut that names the other workspace. `Lakehouse/Inbound/shortcuts.py` in the Planning project:

```python
from weaver import Shortcut

Parcel__StatusEvent = Shortcut(
    shortcut_type="table",
    target_type="physical",
    target="Warehouse/Operations/Tables/Parcel.StatusEvent",
    workspace="Parcel Operations",
)
```

The Planning team's `Capacity` Warehouse then reads that Table through a logical Shortcut in `Warehouse/Capacity/shortcuts.yml`, as in [Connect items and dependencies](connected-items.md):

```yaml
logical:
  Warehouse/Capacity/Parcel.StatusEvent: Lakehouse/Inbound/Tables/Parcel.StatusEvent
```

Joining reads every catalogue you give, so you need read access to each one. Loading or testing another team's objects runs them in that team's workspace and records them in its catalogue, so it needs write access there. See [Permissions](../reference/permissions.md).

## How catalogues join

Give `--catalogue Workspace/Warehouse/Name` once for each catalogue:

```bash
weaver health \
  --catalogue "Parcel Operations/Warehouse/Catalogue" \
  --catalogue "Depot Planning/Warehouse/Catalogue"
```

In this example, Planning's Lakehouse Shortcut already identifies the Operations Table it reads. Give Weaver both catalogues and it matches that Shortcut to the Table recorded by Operations. Health can then follow Planning's dependency back to Operations and check the source Table's last Load result. You do not declare the relationship again in a separate configuration file. A Shortcut into an item that no supplied catalogue installs adds no managed producer to the joined graph.

The working workspace resolves as it does for one catalogue: `--workspace`, `--workspace-config`, or `workspace-config.yml` in the current directory. When nothing names one, the first catalogue's workspace is the working workspace. A catalogue given as `Warehouse/Name` is in the working workspace. Giving the same catalogue twice is an error.

Each catalogue is labelled by its workspace name, or by `Workspace/Name` when two catalogues given share a workspace. Reports qualify objects with that label, so two teams' `Warehouse/Mart` stay distinct.

## Read Health across catalogues

Run the command above from the Planning project. Health reports each catalogue in the order given, each as its own single-catalogue report, and assesses each one with ancestry through the others:

- the Planning team's `Capacity` Tables are behind when the Operations Table they read has failed, has not loaded, or has loaded since they last loaded;
- a catalogue that cannot be read keeps its place in the report with the error, and is not assessed;
- an object that reads into a catalogue that could not be read is Amber, and its finding says whether it is current is unverified.

The overall status is the worst catalogue's status; a catalogue that was not assessed counts as Amber at least. The CLI exits `0` only when every catalogue is Green.

To report on one team while reading the other for context, name its items. Here only `Depot Planning` is reported, and `Parcel Operations` supplies its load state:

```bash
weaver health --item "Depot Planning" \
  --catalogue "Parcel Operations/Warehouse/Catalogue" \
  --catalogue "Depot Planning/Warehouse/Catalogue"
```

A catalogue given only for context is not inventoried.

## Load or Test across catalogues

Suppose Operations has repaired and reloaded its source Table. As Planning, first catch up your own work using that upstream state:

```bash
weaver load "Depot Planning" --stale \
  --catalogue "Parcel Operations/Warehouse/Catalogue" \
  --catalogue "Depot Planning/Warehouse/Catalogue"
```

Only Planning's items run. Operations' catalogue supplies upstream state; including it does not reload Operations. `--stale` judges Planning's objects against their sources in both catalogues.

Then validate Planning's changed data. Each validation runs in Planning's workspace and is recorded in Planning's catalogue; `test --stale` counts source loads in either catalogue:

```bash
weaver test "Depot Planning" --stale \
  --catalogue "Parcel Operations/Warehouse/Catalogue" \
  --catalogue "Depot Planning/Warehouse/Catalogue"
```

Check scoped Health again to see whether Planning has caught up. An upstream failure still needs Operations' attention.

### Deliberately coordinate both teams

When you are responsible for both teams' run and have write access to both, select both workspaces. The catalogues supply dependency context; the workspace selectors choose execution:

```bash
weaver load "Parcel Operations" "Depot Planning" \
  --catalogue "Parcel Operations/Warehouse/Catalogue" \
  --catalogue "Depot Planning/Warehouse/Catalogue"
```

Items decide what runs. A bare workspace name selects every item in that workspace's catalogue, `Kind/Name` an item in the working workspace's catalogue, and `Workspace/Kind/Name` an item in another workspace's. The Operations Table loads first; Weaver then waits until OneLake publishes it, refreshes the `Inbound` SQL endpoint, and loads the `Capacity` Tables that read it.

- Each catalogue is read once before any work starts. If one cannot be read, the run is refused.
- Every object runs in its own workspace, with the working workspace's Environment. Cross-workspace Spark attachment requires Read access to that Environment and the same capacity and network security settings; see [shared runtime setup](../lakehouse/runtime.md#use-a-shared-environment).
- Every object is recorded in its own catalogue, and every record in the run carries one workflow ID.
- When a context catalogue supplies a Warehouse Table that your run reads without loading it, Weaver waits until OneLake has published that Table's last successful load.

With no items, the run covers the working workspace's catalogue: its configured catalogue if you gave it, otherwise the one catalogue you gave in the working workspace. Several catalogues in the working workspace, none of them configured, is an error; name the items instead.

`--file` runs against one catalogue and is refused with several. [Load behaviour](../reference/operation-behaviour/load.md#several-catalogues) and [Test behaviour](../reference/operation-behaviour/test.md#several-catalogues) give the exact selection forms and failure rules.

## Cycles

Teams that read one another's data can form a cycle: an object in one catalogue reads an object in another, which reads the first. A cycle is between objects, not items; two teams that read different objects of each other's form none.

Health and Load report each cycle once. Health lists cycles that span catalogues under **Cycles across catalogues**; a cycle within one catalogue is a Green finding in that catalogue's Build section. A Load report carries a `dag_cycle` message naming the members.

Load runs each selected member once per invocation in a deterministic order by target and name. It breaks the cyclic ordering constraints to form an executable plan; it does not iterate to convergence. Dependencies that close a cycle can therefore read results left by an earlier run.

Health does not compare load times between members of a cycle, because each reads what another last loaded and one is always newer. A member that failed, is Pending or is older than `--as-of` is still reported, and a failed member's state reaches the others.

## Next

The [Catalogue Dashboard](catalogue-dashboard.md) shows several catalogues in one Power BI report. [Health behaviour](../reference/operation-behaviour/health.md#several-catalogues) gives the exact report structure.
