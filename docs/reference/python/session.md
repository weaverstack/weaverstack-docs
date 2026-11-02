# Session and workspace helpers

A Session carries workspace resolution, credentials and acquired Fabric execution resources across operation calls. Constructing one resolves configuration but does not resolve Fabric items, start Livy or open a TDS connection. Capabilities are acquired when an operation asks for them.

Use it as a context manager:

```python
import weaver

with weaver.session(
    workspace="Parcel Operations",
    catalogue="Warehouse/Weaver",
    environment="Weaver",
) as opened:
    build_result = weaver.build(".", session=opened)
    load_report = weaver.load("Lakehouse/Parcels", session=opened)
    validation_report = weaver.test("Lakehouse/Parcels", session=opened)
    validation_report.report()
```

The Session closes on leaving the block. Each operation leaves a supplied Session open; an operation-created Session closes at the end of that call. A closed Session does not reopen.

`workspace_config` reads the same workspace configuration used by the CLI. Explicit `workspace`, `catalogue` and `environment` values override values read from that file. A resolved workspace object can be passed as `workspace`, but not together with `workspace_config`.

`current_workspace()` discovers `workspace-config.yml` from the current project first, then the current Fabric notebook workspace. Outside those contexts, pass a workspace name or configuration explicitly.

The [Sessions and workflows guide](../../estate/automation-and-deployment.md) covers interactive command composition. The [`weaver session` reference](../cli/session.md) documents the terminal prompt.

A catalogue-free Power BI Session needs no Spark Environment. Spark-backed Build execution checks the active or published Weaver runtime before dispatch. See [runtime qualification](../operation-behaviour/session-runtime.md#fabric-environment-qualification).

## Workflows

`weaver.workflow()` runs several operations in one Session under one workflow ID. An operation inside it that is given no `session=` uses the workflow's Session and configuration.

```python
import weaver

with weaver.workflow():
    weaver.load(stale=True)
    weaver.test(stale=True)
    weaver.health()
```

Without `session=`, the workflow opens a Session and closes it on exit. With `session=`, it borrows that Session and leaves it open:

```python
with weaver.session(workspace_config="workspace-development.yml") as opened:
    with weaver.workflow(session=opened):
        weaver.load(stale=True)
        weaver.test(stale=True)
```

Load and Test record under the workflow's ID, in their reports and in `_.Log`, `_.LoadStatus` and `_.TestStatus`, whether they run on the desktop or in Fabric. Each workflow gets its own ID. Outside a workflow, each run records under an ID of its own.

A workflow does not change what an operation returns. Test still returns its report when validations find something; inspect `succeeded`.

### Workflow configuration

The workflow resolves its configuration once, as an operation does; see [workspace resolution](../configuration-files/workspace-config.md#workspace-resolution-and-precedence). Arguments then change it for the workflow:

| Argument | Effect |
| --- | --- |
| `workspace`, `workspace_config` | Resolve that workspace or file instead of the Session's own configuration. |
| `catalogue`, `environment` | Replace the resolved value. |
| `mirror`, `execution`, `targets`, `data_sources`, `catalogue_dashboard` | Replace the resolved value whole. Values take workspace configuration shapes and are validated as configuration is. |
| `credential` | Applies to a Session the workflow opens; refused beside `session=`. |

Replacement is whole: `targets={"Lakehouse/Landing": "Landing_Test"}` leaves only that binding, and `execution={"run": {"spark_concurrency": 2}}` returns every other limit to its default. An empty mapping replaces too; `None` leaves the resolved value.

An argument given to an operation inside the workflow applies to that call only. It does not change the workflow, the Session or the next operation.

A workflow resolves no Fabric items and starts nothing. In a Fabric notebook with no `workspace-config.yml`, it takes the notebook's workspace and no catalogue, so catalogue-backed operations still need `catalogue=`.

### Workflow limits

- Workflows nest. An inner workflow with no `session=` borrows the outer one's Session; on exit, the outer workflow and its ID return.
- A Session runs one workflow at a time. Entering a workflow on a Session that another thread's workflow is using is refused. Open a Session for each concurrent workflow.
- A workflow applies to the thread that entered it. A thread started inside it is not in the workflow; give its operations `session=`.
- An authored object's own `load()` or `run()` records under an ID of its own.

`weaver workflow` runs its entries inside one workflow on its Session. See [Workflow](../operation-behaviour/workflow.md).

## Lakehouse locations

`Lakehouse` represents a resolved Lakehouse destination for authored code. It provides table and folder paths and qualifies object names against its Spark destination.

`default_lakehouse(spark)` resolves the Lakehouse attached to the supplied Fabric Spark session. It requires an attached Lakehouse and its workspace address.

`lakehouse_for(resolver, item)` resolves a named Lakehouse with the supplied resolver. Use the returned `Lakehouse` rather than retaining session-scoped mounted paths; `spark_root` is its durable OneLake identity.

<!-- BEGIN GENERATED PYTHON -->

## Public exports

### `weaver.Lakehouse`

Kind: class

### `weaver.Workflow`

Kind: class

### `weaver.current_workspace`

```python
weaver.current_workspace() -> Workspace
```

### `weaver.default_lakehouse`

```python
weaver.default_lakehouse(spark: Any) -> Lakehouse
```

### `weaver.lakehouse_for`

```python
weaver.lakehouse_for(resolver: Any, item: ItemRef | str) -> Lakehouse
```

### `weaver.session`

```python
weaver.session(*, workspace: Any=None, catalogue: str | None=None, environment: str | None=None, workspace_config: Any=None, credential: Any=None)
```

### `weaver.workflow`

```python
weaver.workflow(*, session: 'Session | None'=None, workspace: str | None=None, workspace_config: str | Path | None=None, catalogue: str | None=None, environment: str | None=None, mirror: str | None=None, execution: 'ExecutionSettings | Mapping[str, Any] | None'=None, targets: Mapping[Any, Any] | None=None, data_sources: Mapping[str, str] | None=None, catalogue_dashboard: str | None=None, credential: Any=None) -> Iterator[Workflow]
```

<!-- END GENERATED PYTHON -->
