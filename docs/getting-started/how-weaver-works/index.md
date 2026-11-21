# How Weaver works

A Weaver project holds the definitions for a Fabric estate: Lakehouses, Warehouses, semantic models and Reports. Workspace configuration maps their logical names to physical items, and the catalogue records what is installed and what has run. Four operations connect those three things.

```text
project source
    ↓ Build
installed definitions and work
    ↓ Load
data + current load state
    ↓ Test
current validation state
    ↓ Health
estate assessment
```

The operations are separate because the things they act on are separate. Source is not installed state, installed work is not the data it produces, and a validation result is not the act of loading data. Each operation reads the state its predecessor left in the catalogue rather than reinterpreting project files.

## The project holds the source

Python and SQL define data work under `Lakehouse/` and `Warehouse/`. Native model and Report definitions live under `PowerBI/`. Models use standard TMDL; optional overlays and Weaver annotations add refinements and modelling rules, and play the same authoring role as the engineering declarations around SQL and Python. Tests and Assumptions live beside the items they check.

The project declares logical identities, not development or production item names. Workspace configuration selects the destination, so one copy of the source serves every environment.

[Projects and estates](../../estate/projects-and-estates.md) describes how a project is organised. [Logical and physical items](../../estate/environments/logical-and-physical-items.md) describes the binding to Fabric. [Weaver documents](../../reference/weaver-documents/overview.md) specifies what each file declares.

## Build installs definitions

Build is the operation that reads Weaver documents. It combines the selected source with workspace configuration, works out what has to change in the bound Fabric items, applies it and records the resulting installed generation in the catalogue. It also deploys native semantic models and their linked Reports. Build does not run the authored data loads or refresh models.

Each kind of document contributes something different:

- Tables and Folders contribute stored targets and loadable work.
- Views contribute query-defined relations that Build installs directly.
- Tests and Assumptions contribute validations for a later Test.
- Shortcuts contribute installed connections.
- Warehouse programmables and schema metadata contribute definitions with no separate Load step.

Editing a document changes the project, not the installed estate. The edit becomes part of the operating estate when Build installs it, and not before.

Build Lakehouse and Warehouse work first, then models and Reports in a separate call against the same project. The second call can read the metadata the first one installed. A workflow can sequence both.

## Load runs installed work

Load reads installed items and their recorded bindings. It runs Table and Folder work and refreshes registered semantic models through one dependency graph. With no item selection it covers the installed estate, and selected source work runs before the consumers and model refreshes that depend on it.

Because Load does not reopen project source, a Table edited after the last Build keeps running its previously installed work until another Build succeeds.

Each consumer keeps its own bookmark of successful processing, so a failed node does not discard the progress of independent work that finished. Views, Tests, Assumptions, Shortcuts, Warehouse programmables and schema metadata have no Load step of their own, though loadable work can read from them. A Report has no Load or Test either; it uses its model's data.

[Dependencies](../../estate/connected-items/dependencies.md) explains the graph, Incremental load via bookmarks in [Lakehouse](../../lakehouse/incremental.md) and [Warehouse](../../warehouse/incremental.md) shows bookmarks at work, [Incremental loading](../../reference/incremental-loading.md) specifies the contract, and [Fault tolerance](../../estate/recovery/fault-tolerance.md) covers what happens when a node fails.

## Test checks the data

Test reads the catalogue and runs the installed validations in its selection. A Test compares expected and actual rows. An Assumption returns the rows that contradict a condition and passes when there are none. Both can be authored for Lakehouse and Warehouse data, or as DAX against a semantic model. A model's DAX result can be compared with SQL calculated independently from its managed source.

Each validation's current outcome is recorded in the catalogue alongside its history. In catalogue mode an edited validation takes effect after Build installs it. File mode, selected with `--file` or by running without a catalogue, reads authored validations directly and records nothing. `--source` chooses the project folder; it does not by itself select file mode when a catalogue is configured.

[Testing Warehouse data](../../warehouse/tests.md) and [Testing Lakehouse data](../../lakehouse/tests.md) introduce validations in each item's own terms.

## Health reads the whole estate

Health brings Build, Load and Test state into one report, classified Green, Amber or Red. Without an item selector it covers the managed estate, including registered model refreshes and their DAX validations. It uses recorded state and, by default, the physical inventory of the selected targets. It runs no authored load or validation code and does not change the installed generation.

The shared view matters when something changes underneath earlier results. If a source is loaded after a downstream Table or model last ran, Health reports the downstream work as behind rather than presenting each successful run in isolation.

[State and Health](../../estate/catalogue-and-health/state-and-health.md) explains how the classifications are assigned.

## Each operation draws its own boundary

Build selects project items and resolves their configured physical targets. Load and Test select from the installed estate and use the bindings Build recorded. Operations that work without a catalogue, such as standalone Power BI deployment and file-mode validation, use configuration and source instead. Dependencies can widen the work inside a selected item and determine its order, but they do not add another item to the selection.

[Operation behaviour](../../reference/operation-behaviour/index.md) specifies the selection, ordering, state changes and failure boundary of each operation. [Sessions and execution contexts](../../estate/automation-and-deployment/sessions-and-hosts.md) covers running several operations together through a Session or a workflow.

## Develop against existing data

Mirror borrows unchanged data through Warehouse Views and OneLake Shortcuts, and Build materialises only the work you change. The project keeps the same logical names and operating flow throughout. [Borrowed and local data](../../estate/mirror/borrowed-and-local-data.md) explains the model, and [The development cycle](../../estate/development-cycle.md) shows it in use.

[Design principles](design-principles.md) gives the reasons for these boundaries.
