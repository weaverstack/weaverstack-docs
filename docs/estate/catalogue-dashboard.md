---
hide:
  - toc
---

# Catalogue Dashboard

After you build and load a project, use the Catalogue Dashboard to see what is installed, what has run and what needs attention. Run `weaver catalogue-dashboard` to deploy its Power BI semantic model and Report over one catalogue or several teams' catalogues.

Start with Workspaces or Items to see how the work connects. Use Health and Orchestration to investigate a failure or dependency. Performance, Gantt, Entity dictionary and Semantic model show timings, workflow timelines, table relationships and semantic models. The Dashboard reads the catalogue records Weaver already maintains; it needs no separate monitoring database.

The Dashboard reads the catalogues in their existing workspaces. Manage its semantic model and Report separately with `weaver catalogue-dashboard` and the Fabric interface.

It is an ordinary semantic model and Report. Change it to fit your needs, or build your own over the catalogue.

## The HTML Content visual

Each page is drawn by the HTML Content custom visual (the Regular edition, from AppSource). Where a tenant allows only certified visuals, a Fabric administrator must add HTML Content as an organisational visual before the pages render. The semantic model works without it, and [exported pages](#export-static-pages) do not use it.

See the command reference for the Report’s [support status](../reference/cli/catalogue-dashboard.md#support-and-compatibility).

## Deploy the Dashboard

Bring the source catalogues up to date by building their projects with the Weaver version used for Dashboard deployment. The deployment command checks the required catalogue tables and columns and identifies any that need updating before applying changes.

Give the deployment identity Contributor access to the Dashboard workspace and read access to each catalogue. Binding connections requires model ownership and access to those connections; see [permissions](../reference/permissions.md). Continuing the [Parcel estate](catalogue-and-health.md), name the Dashboard and deploy it:

```bash
weaver catalogue-dashboard --name "Catalogue Dashboard" --workspace-config workspace-development.yml
```

<!-- cli-capture: {"id": "152-catalogue-dashboard", "title": "Catalogue Dashboard · deploy over the Parcel catalogue"} -->
<p class="terminal-intro">The command returned:</p>
<figure class="weaver-terminal" aria-label="Catalogue Dashboard · deploy over the Parcel catalogue">
<figcaption>Terminal output <span class="terminal-exit">exit 0</span></figcaption>
<pre tabindex="0" aria-label="Terminal output"><code>Catalogue Dashboard

  Check the source catalogue                                                                               1.8s
  Resolve the Dashboard&#x27;s items                                                                           21.3s
Workspace  Parcel Development
Catalogue  none
Targets
  SemanticModel/Catalogue Dashboard
  Report/Catalogue Dashboard


Build

    Resolve semantic data sources                                                                          0.3s
      Resolve SemanticModel/Catalogue Dashboard                                                            0.0s
      Resolve Report/Catalogue Dashboard                                                                   0.0s
    Read target inventories                                                                                0.2s
    Read semantic sources                                                                                  5.1s
    Prepare bundle                                                                                         0.4s
Install selection
  SemanticModel/Catalogue Dashboard
    changed                 1
    selected for build      1
  Report/Catalogue Dashboard
    changed                 1
    selected for build      1

→     SemanticModel/Catalogue Dashboard · Deploy semantic definitions · 1 action
<span class="terminal-status-green">✓     SemanticModel/Catalogue Dashboard · Deploy semantic definitions · 1 action                          22.6s</span>
→     SemanticModel/Catalogue Dashboard, Report/Catalogue Dashboard · Verify deployed semantic definitions · 1 action
<span class="terminal-status-green">✓     SemanticModel/Catalogue Dashboard, Report/Catalogue Dashboard · Verify deployed semantic definitions · 1 action   20.6s</span>
→     Report/Catalogue Dashboard · Deploy Report definitions · 1 action
<span class="terminal-status-green">✓     Report/Catalogue Dashboard · Deploy Report definitions · 1 action                                   20.4s</span>
→     Report/Catalogue Dashboard · Verify deployed Report definitions · 1 action
<span class="terminal-status-green">✓     Report/Catalogue Dashboard · Verify deployed Report definitions · 1 action                          20.9s</span>
    Install                                                                                               1m24s
<span class="terminal-status-green">✓ Build                                                                                                   1m30s</span>

  Refresh the Dashboard model                                                                             13.6s
<span class="terminal-status-green">✓ Catalogue Dashboard                                                                                     2m08s</span>

Catalogue Dashboard  Catalogue Dashboard  in Parcel Development
  Reads  Parcel Development/Warehouse/Catalogue  (21 tables)
  SemanticModel Catalogue Dashboard  updated
  Report        Catalogue Dashboard  updated
</code></pre>
</figure>
<!-- /cli-capture -->

The command creates or updates a SemanticModel and a Report with that name in the workspace it runs against, then refreshes the model. It reads the catalogue named by `catalogue:` in the workspace configuration. To deploy without naming the Dashboard each time, add the name to the configuration:

```yaml
workspace: Parcel Development
catalogue: Warehouse/Catalogue
catalogue_dashboard: Catalogue Dashboard
```

- A name that `targets:` deploys a model or Report to is refused, and so is an existing model or Report of that name that is not a Catalogue Dashboard.
- `--dry-run` reads the catalogues and resolves the Dashboard's items, and changes nothing.
- Run the command again after upgrading Weaver. It replaces the model and Report definitions, so save your own changes under another name.
- To remove the Dashboard, delete its SemanticModel and Report in Fabric.

From Python, [`weaver.deploy_catalogue_dashboard`](../reference/python/operations.md) takes the same choices. The [command reference](../reference/cli/catalogue-dashboard.md) lists every option.

## Read several catalogues

Repeat `--catalogue` to read several catalogues in one Dashboard, for example one per team:

```bash
weaver catalogue-dashboard --name "Catalogue Dashboard" \
  --catalogue "Parcel Development/Warehouse/Catalogue" \
  --catalogue "Parcel Billing/Warehouse/Catalogue" \
  --workspace-config workspace-development.yml
```

A reference is `Workspace/Warehouse/Name`, or `Warehouse/Name` for a catalogue in the workspace the command runs against. The pages list the catalogues in the order given. A catalogue given twice is refused, and so is the whole set when any catalogue cannot be read, with each one named.

A physical shortcut recorded in one catalogue, onto an item another catalogue installs, joins their graphs: lineage, Orchestration and the Workspaces page follow it from one catalogue into the other. The page header names a single catalogue by its workspace, and several by their number and the first three. To load, test and assess several catalogues as one graph, see [work across teams' catalogues](across-catalogues.md).

### Direct Lake and Import

The model reads up to ten catalogues over Direct Lake on OneLake, one hidden table per catalogue table, so each page shows what the catalogues record as work is processed. More than ten requires `--ImportMode`, which imports them instead.

Import reads each catalogue through its Warehouse's SQL endpoint, and each endpoint needs a cloud or gateway connection the model can refresh with. After deploying, Weaver binds each endpoint to the one connection whose path is that endpoint's server and database. When no connection reaches an endpoint, deployment reports it as a warning and does not refresh the model: create a cloud connection to each SQL endpoint and deploy again, or set the model's credentials in Fabric and refresh it there. When several connections reach one endpoint, deployment stops and names them; keep one. See [permissions](../reference/permissions.md).

An imported Dashboard shows the catalogues as of the model's last refresh, and the page header shows when that was.

## What it reads

The model reads these catalogue tables: `Installation`, `Registry`, `LineageNode`, `LineageEdge`, `Dependency`, `Shortcut`, `LoadStatus`, `TestStatus`, `Log`, `LoadStatistic`, the dictionary tables, the `SemanticModel` tables, and `Mirror` in a catalogue that has been a mirror. The [catalogue schema](../reference/catalogue-schema.md) describes each one.

Each page sends the visual only what it shows. The Gantt and Items pages read workflows from the last 7 days, and Performance reads up to 30 days. The catalogue keeps the full history for your own queries.

Over Direct Lake, the first page view after a load, or after the model has been idle, can take several seconds while Direct Lake loads the columns it needs.

## Filter the pages

The Report's Filters pane narrows the data itself, before a page is built:

| Field | Selects |
| --- | --- |
| Workspace | items installed in that workspace |
| Item type | items of one type, such as Lakehouse or SemanticModel |
| Item name | individual items |
| Object type | objects of one kind, such as Table, View or Test |
| Object name | individual objects |

The Workspaces and Semantic model pages offer the first three fields. Without a selection every row stays. The catalogue's own item always stays, because the page header names the catalogue from it.

The lists in the Filters pane are written when the Dashboard is deployed, so an item or object installed since then is not in them and cannot be selected. A new item shows only while nothing is selected; a new object in a listed item shows while no Object type or Object name is selected. Deploy again to add them to the lists.

One Power BI measure returns a page, and a measure's text is limited to about 2 million characters. A page whose data exceeds that says so, with its size, and asks you to narrow the selection in the Filters pane. [Exported pages](#export-static-pages) carry no such limit.

## Export static pages

`weaver catalogue-dashboard export` writes the deployed Dashboard's pages as static HTML snapshots of the model's data at export. Downloaded local files open in a browser without a running Fabric capacity or the HTML Content visual:

```bash
weaver catalogue-dashboard export --path dashboard-pages --workspace-config workspace-development.yml
```

The folder receives one file per page, named by the page, and `index.html`, the Workspaces page. A bar of links at the top of each page opens the others. The data is the deployed model's as it is when you export, with no Filters pane selection. Each page is joined outside Power BI, so it is not limited to the 2 million characters one measure returns. `--name` defaults to `catalogue_dashboard:`.

`--path` is a writable local folder or a OneLake `abfss://` location where the running identity can write. A file retained only in a Lakehouse still requires access to that storage; exporting it does not make an unavailable Lakehouse accessible. The export runs from a desktop or in a Fabric notebook, so a scheduled notebook can keep a copy in a Lakehouse:

```python
import weaver

weaver.export_catalogue_dashboard(
    "abfss://<workspace-id>@onelake.dfs.fabric.microsoft.com/<lakehouse-id>/Files/dashboard",
    name="Catalogue Dashboard",
    workspace="Parcel Development",
)
```

The Dashboard must already be deployed in the workspace; an export names the missing Dashboard and asks you to deploy it. The export reads the model's measures through the Power BI `executeQueries` API, so the identity needs Read and Build permission on the model and the tenant's **Semantic Model Execute Queries REST API** setting must allow it. See [permissions](../reference/permissions.md).

## The pages

The demonstrations below are the Dashboard's own renderer over a generated estate of 133 objects, recorded at a fixed time. Search, select, drag and zoom as you would in Power BI.

Times show in the time zone of your browser, with the zone named, for example `AEDT`. The **Times** control in the page header switches the page to UTC and back. The catalogue holds UTC and the Dashboard converts it as it draws, so a time in the table is the same instant in either zone.

### Marks

Each object carries a mark for its kind, in lists, chips, the graph and the Gantt and Performance tables. Hover a mark for its name.

| Mark | Kind |
| --- | --- |
| Filled blue circle | Table |
| Blue ring with a dot | View |
| Green folder | Folder |
| Amber diamond | Shortcut |
| Filled violet triangle | Test |
| Outlined violet triangle | Assumption |
| Dark blue hexagon | Semantic model |
| Dark blue outlined square | Report |

A key above a page's first table or list shows the marks present. Where the Dashboard reads a mirror, the key adds how [the mirror left each object](#beside-a-mirror).

### Choose items

Every page except Workspaces starts with an **Items** chooser. Click an item to show it alone; hold Ctrl or ⌘, or tick its box, to add or remove it. Where the catalogues cover more than one workspace, each workspace is an entry of its own that brings in all of its items. Type to filter the list.

Items, Health, Performance and Gantt show every item until you choose. Orchestration and the Entity dictionary, which draw one Lakehouse or Warehouse in detail, and the Semantic model page show the first item they offer. Choosing nothing returns a page to its default.

The chooser picks what a page draws from the data it holds. To reduce the data itself, use the [Filters pane](#filter-the-pages).

### Workspaces

Which items depend on Operations? In the Parcel Dashboard, set **Show** to items and select **Operations**. Read the connected-item list to distinguish what supplies Operations from what reads it. Select a connected item's node, then choose that item on **Orchestration** to inspect the objects it reads and their last outcomes. If Operations has no downstream item yet, select Landing and follow its connection to Operations from the connected-items task.

Open **Health** for the selected item to see which recorded loads or validations need attention. If its source loaded after its last successful run, check the resulting stale finding before choosing what to rerun. Use `weaver health` when you also need physical inventory or borrowed-source state.

The network shows the workspaces and items the catalogues describe, with what each supplies to and receives from the others. **Show** switches between workspaces and items; with one workspace, the page starts with its items. A dependency is one object reading another directly, and a shortcut is the dependency rather than whatever reads through it. Dependencies inside one item are left out, and an item that two catalogues record counts once.

The tiles count workspaces, items and the dependencies between them. Select a workspace or item to list its items or the items it is connected to, with the dependencies in and out and each item's load state. Workspaces or items that read from one another, directly or through others, are listed as loops. Load state here is each item's last loads and validations, not a Health assessment.

<div class="dashboard-demo"><iframe src="../../assets/catalogue-dashboard/workspaces.html" title="Catalogue Dashboard demo: Workspaces" loading="lazy"></iframe></div>
<p class="dashboard-demo-open" markdown>[Open the Workspaces page full size](../assets/catalogue-dashboard/workspaces.html){ target="_blank" }</p>

### Items

Installed items by kind, with their object counts, a status bar and when work was last processed, grouped by workspace when there is more than one. The tiles summarise Load, Tests and Build health and the workflows of the last 7 days; significant findings and recent workflows are listed below.

<div class="dashboard-demo"><iframe src="../../assets/catalogue-dashboard/overview.html" title="Catalogue Dashboard demo: Items" loading="lazy"></iframe></div>
<p class="dashboard-demo-open" markdown>[Open the Items page full size](../assets/catalogue-dashboard/overview.html){ target="_blank" }</p>

### Health

The Load, Tests and Build findings, filtered by area and severity, including green rows. This page assesses what the catalogue records about itself. Physical inventory, unresolved references and a mirrored source's loads need [`weaver health`](catalogue-and-health.md).

<div class="dashboard-demo"><iframe src="../../assets/catalogue-dashboard/health.html" title="Catalogue Dashboard demo: Health" loading="lazy"></iframe></div>
<p class="dashboard-demo-open" markdown>[Open Health full size](../assets/catalogue-dashboard/health.html){ target="_blank" }</p>

### Orchestration

The installed dependency graph across Lakehouses, Warehouses and semantic models, coloured by each object's last outcome or by kind. The tiles count objects that are current, ready to load, waiting on a dependency or failed.

- Search for an object and press Enter to select it. Shift adds to the selection.
- A term containing `*` adds every match: `Parcel.*` selects every object in the `Parcel` schema. Terms combine.
- **Up** and **Down** set how many dependency levels to show either side of the selection. `‹‹ N` and `N ››` markers expand the neighbours not shown.
- Drag nodes, zoom, and use ⤢ to fill the page. The side panel shows the selected object's last load, readiness, findings, validations, and what it reads and is read by.

<div class="dashboard-demo"><iframe src="../../assets/catalogue-dashboard/orchestration.html" title="Catalogue Dashboard demo: Orchestration" loading="lazy"></iframe></div>
<p class="dashboard-demo-open" markdown>[Open Orchestration full size](../assets/catalogue-dashboard/orchestration.html){ target="_blank" }</p>

### Performance

Did the run finish in time. Each workflow is one vertical bar in a column for its day, from the time it started at the bottom to the time it finished at the top, with the time of day up the side in the page's time zone. The bar is drawn in blue for the Load part and violet for the Test part, and outlined in red when a record failed. Runs that overlap are never added together. Set a deadline, an hour of that zone, to see which runs ended after it.

Choose a window of 24 hours, 7 days or 30 days, a task and the items. Select a run, in the chart or its table, to list its longest object records, Loads first and then Tests. Select an object in that list to see that load's own row counts, read, inserted, updated, deleted and rejected, with the same object's loads in the runs around it, one row each. A Test shows its result and message with the executions around it. Counts are never added across loads.

The Loads and Tests tables give each object's number of loads or executions over the window. Select one to see its latest loads or executions one by one. The largest loads of the last 7 days are listed each by its own counts.

<div class="dashboard-demo"><iframe src="../../assets/catalogue-dashboard/performance.html" title="Catalogue Dashboard demo: Performance" loading="lazy"></iframe></div>
<p class="dashboard-demo-open" markdown>[Open Performance full size](../assets/catalogue-dashboard/performance.html){ target="_blank" }</p>

### Gantt

One workflow from the last 7 days, each record a bar on its timeline, with the object's mark, its item as `Type/Name` and its task, Load or Test. The tiles give elapsed time, summed task time, peak concurrency and failures. Click a row for the object and the record's outcome. Hold Ctrl or ⌘ and scroll to zoom time; drag to pan; double-click to reset. Records of the items not chosen are left out; the workflow's own records always show.

<div class="dashboard-demo"><iframe src="../../assets/catalogue-dashboard/gantt.html" title="Catalogue Dashboard demo: Gantt" loading="lazy"></iframe></div>
<p class="dashboard-demo-open" markdown>[Open the Gantt full size](../assets/catalogue-dashboard/gantt.html){ target="_blank" }</p>

### Entity dictionary

An ER diagram of Lakehouse and Warehouse tables, drawn from their declared `Primary key` and `Foreign keys`. Select a table and set how many levels of **Parents** (the primary key side) and **Children** (the foreign key side) to follow. Tables with no relationship are shown too. Boxes can be dragged.

Below it, the dictionary lists every item, Table, View, Folder, Shortcut, Test, Assumption and column, filtered by name, kind or description.

<div class="dashboard-demo"><iframe src="../../assets/catalogue-dashboard/entities.html" title="Catalogue Dashboard demo: Entity dictionary" loading="lazy"></iframe></div>
<p class="dashboard-demo-open" markdown>[Open the Entity dictionary full size](../assets/catalogue-dashboard/entities.html){ target="_blank" }</p>

### Semantic model

One deployed semantic model: its last refresh, DAX validations, and a bus matrix of fact tables against dimension tables showing each relationship's cardinality, filter direction and whether it is active. Its tables, columns, measures and the managed sources they read follow. Choose more models to show each in turn.

<div class="dashboard-demo"><iframe src="../../assets/catalogue-dashboard/semantic.html" title="Catalogue Dashboard demo: Semantic model" loading="lazy"></iframe></div>
<p class="dashboard-demo-open" markdown>[Open the Semantic model page full size](../assets/catalogue-dashboard/semantic.html){ target="_blank" }</p>

## Beside a mirror

Read a [mirror](mirror.md) together with the catalogue it mirrors, and the Dashboard compares them object by object. On the mirror's side, an object is:

- **borrowed**, drawn muted, while the mirror still borrows it from the source;
- **changed**, marked Δ, when it was built in the mirror and its signature differs from the source object's;
- **added**, marked +, when the catalogue mirrored holds no such object;
- otherwise rebuilt with the same code, and drawn as usual.

The source's copy of a borrowed or changed object is drawn the same way, and a borrowed object takes its source object's load state. The page key names both marks.

Read over the mirror alone, the Dashboard marks only borrowed objects, and their loads are not observed: Health counts them as unobserved. [`weaver health`](catalogue-and-health.md) reads the source's loads.
