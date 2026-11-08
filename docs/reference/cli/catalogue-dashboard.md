# `weaver catalogue-dashboard`

Catalogue Dashboard creates or updates the Catalogue Dashboard's SemanticModel and Report, both under one name, in the workspace the command runs against, and refreshes the model. Each catalogue given is read in its own workspace and never written, and nothing about the Dashboard is recorded in a catalogue.

```bash
weaver catalogue-dashboard --name "Catalogue Dashboard" --workspace-config workspace-development.yml
```

`--catalogue` defaults to `catalogue:` and `--name` to `catalogue_dashboard:` in workspace configuration. Repeat `--catalogue` to read several catalogues, in the order the pages list them. Up to ten are read over Direct Lake; more require `--ImportMode`, which imports them through each catalogue's SQL endpoint. Import binds each endpoint to the one connection that reaches it; when none does, the command reports a warning and does not refresh the model, and when several do, it fails naming them.

Refused before any change: a catalogue given twice, a catalogue that cannot be read or lacks a table or column the Dashboard reads, a name that `targets:` deploys a model or Report to, and an existing model or Report of that name that is not a Catalogue Dashboard. A dry run reads the catalogues, resolves the items and changes nothing.

`export` writes the deployed Dashboard's pages as static HTML to `--path`, a local folder or a OneLake `abfss://` location: `index.html` and one file per page. It reads the model through the Power BI `executeQueries` API, so it needs the deployed Dashboard and the tenant's Semantic Model Execute Queries REST API setting. See [permissions](../permissions.md).

See [Catalogue Dashboard](../../estate/catalogue-dashboard.md) for what the pages show, the Filters pane and the HTML Content requirement.

<!-- BEGIN GENERATED CLI -->

## `weaver catalogue-dashboard`

### Synopsis

```text
weaver catalogue-dashboard [-h] [--workspace WORKSPACE] [--workspace-config WORKSPACE_CONFIG] [--catalogue REFERENCE] [--ImportMode] [--name NAME] [--dry-run] [--json] [--non-interactive] {export} ...
```

### Positional arguments

`{export}`
: No description is provided by the parser.

### Options

`-h, --help`
: show this help message and exit

`--workspace WORKSPACE`
: Fabric Workspace name.

`--workspace-config WORKSPACE_CONFIG`
: Workspace configuration file.

`--catalogue REFERENCE`
: A catalogue Warehouse to read, as Workspace/Warehouse/Name or Warehouse/Name. Repeat for each catalogue, in the order the Dashboard lists them. Defaults to catalogue: in workspace configuration.

`--ImportMode`
: Import the catalogues instead of reading them over Direct Lake. Required for more than ten. Each SQL endpoint needs a connection the model can refresh with.

`--name NAME`
: The SemanticModel and Report to deploy to. Defaults to catalogue_dashboard: in workspace configuration.

`--dry-run`
: Resolve the catalogues and the Dashboard's items without changing them.

`--json`
: Emit the result as JSON.

`--non-interactive`
: Do not read stdin, wait for a keypress or open browser sign-in. Missing authorisation or required input is an error.

## `weaver catalogue-dashboard export`

### Synopsis

```text
weaver catalogue-dashboard export [-h] [--workspace WORKSPACE] [--workspace-config WORKSPACE_CONFIG] --path PATH [--name NAME] [--json] [--non-interactive]
```

### Options

`-h, --help`
: show this help message and exit

`--workspace WORKSPACE`
: Fabric Workspace name.

`--workspace-config WORKSPACE_CONFIG`
: Workspace configuration file.

`--path PATH`
: Folder to write, local or a OneLake abfss:// location.

`--name NAME`
: The Dashboard to export. Defaults to catalogue_dashboard: in workspace configuration.

`--json`
: Emit the result as JSON.

`--non-interactive`
: Do not read stdin, wait for a keypress or open browser sign-in. Missing authorisation or required input is an error.

<!-- END GENERATED CLI -->
