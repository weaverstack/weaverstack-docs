# Warehouse

A Warehouse Table begins with a T-SQL SELECT and a small metadata comment. Weaver installs the physical Table and its load machinery, then records the work it runs.

[Build a first Table and View](first-project.md), then [test their data](tests.md). You keep SQL for the transformation and its independent checks.

When the source changes, [Incremental load via bookmarks](incremental.md) shows how candidate rows and explicit delete keys become target updates around a consumer bookmark. [Protecting data](../lakehouse/protecting-data.md) covers which acquired data must stay outside a managed target, and [Schemas, keys and managed columns](../reference/weaver-documents/schemas-keys-and-columns.md) specifies row identity and the managed columns.

For shared deployment and operation, [Coordinate your estate](../estate/index.md).
