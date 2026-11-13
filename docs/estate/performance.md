# Investigate performance and scale

A slow run can spend its time processing rows, waiting for a service or repeating setup. Those causes need different remedies: more concurrency may help independent work, but it will not shorten a serial dependency chain or fix a slow source query. The reports and timings below help distinguish these cases before a setting changes.

## 1. Keep the comparison fixed

A useful comparison holds the workload and conditions fixed: Weaver revision/package, capacity, selected items, source and target state, run mode and resource limits. Changing one setting at a time makes its effect distinguishable. A first Load, an unchanged Load and an incremental change answer different questions, so their timings are not interchangeable.

Use normal operation reports to identify attempted, succeeded, failed and blocked work. A short run that omitted necessary work is not a performance improvement.

## 2. Separate work, waits and overhead

Use a Session or workflow's Fabric access timings:

```bash
weaver session --workspace-config workspace-development.yml --timings
```

Inside the Session, run the operation you are investigating, then exit to see its access timings. The accepted `verify` sequence from [workflows](automation-and-deployment.md#turn-the-accepted-sequence-into-a-workflow) can report timings with:

```bash
weaver workflow verify --workspace-config workspace-development.yml --timings
```

Review the workflow's commands and confirmation before running it. `--timings` belongs to Session and Workflow, not an invented Load flag. For catalogue-backed work, inspect the per-node report, `_.Log` and `_.LoadStatistic` alongside current status. History is not the same as current health.

Ask where time went:

| Observation | Check next |
| --- | --- |
| Long row-processing nodes | Change volume, incremental query shape, source access and target reconciliation |
| Ready work waiting for a lane | Dependency shape and resource/total concurrency ceilings |
| Long endpoint/readiness waits | The tables actually read through that endpoint and current service readiness |
| Many tiny nodes with little row movement | Repeated session, metadata, storage and scheduling overhead |
| A node failed or was blocked | Correct that condition before treating its short runtime as evidence |

## 3. Adjust the work, not just the lane count

Independent work can run concurrently, but its source dependencies and service limits still govern admission. More lanes do not shorten a serial chain or repair a slow source query. Use [Control concurrency](concurrency.md) to set a total invocation cap or resource limits for the item that is constrained.

Weaver shares repeated setup, batches supported access and coordinates endpoint readiness with the Tables actually needed downstream. For a model refresh, check both the upstream source load and the model’s service refresh: the run report puts them in the same graph.

## A measured estate

An observed synthetic workload of around 3,000 objects on F64, with one Lakehouse and two Warehouses, completed its first Load in about an hour. The later measured incremental Loads completed in under 15 minutes. The workload inserted about 4 billion rows across its layers; those are estate insertions, not distinct source records. These observations are not a service SLA or a duration promised for another workload.

Those measurements describe that workload, not the duration of another project. Your project's data shape, source access and capacity determine its own timings; first-load and incremental results remain separate comparisons.

## Related tasks

- [Limit simultaneous work](concurrency.md).
- [Run only the relevant part](selective-runs.md).
- [Inspect row auditing and operational history](../advanced/row-auditing-and-operational-history.md).
