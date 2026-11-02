# `weaver execute`

Execute runs T-SQL, Spark SQL, Python or DAX against one item and prints what it returns. Use it to inspect or repair an estate without writing a Weaver document.

```bash
weaver execute tsql Warehouse/Curated --command "SELECT TOP 10 * FROM dbo.Example"
weaver execute spark-sql Lakehouse/Landing --file inspect.sql
weaver execute python Lakehouse/Landing --file investigate.py
weaver execute dax SemanticModel/Reporting --command 'EVALUATE ROW("Value", 1)'
```

Give exactly one of `--command` and `--file`. The item is a Weaver item. Its target in workspace configuration is used, or else the Fabric item of the same name; no catalogue is read or needed.

| Engine | Item | Runs | Returns |
| --- | --- | --- | --- |
| `tsql` | `Warehouse/Name` | the source as one batch, over TDS | every result set, in order |
| `spark-sql` | `Lakehouse/Name` | each statement in order, in Fabric Spark with that Lakehouse attached | the last statement's result |
| `python` | `Lakehouse/Name` | the source in Fabric, with `spark` attached to that Lakehouse | what it printed |
| `dax` | `SemanticModel/Name` | one query, through the Power BI `executeQueries` API | its rows |

Python always runs in Fabric, never in the local process. Unqualified Spark names resolve against the attached Lakehouse. From a desktop, a session whose Spark is already attached to another Lakehouse refuses the command; in a notebook, the notebook's own Lakehouse must be the one named.

Each result is read to `--limit` rows (default 100) where it runs, and the output says when a result had more. Python output is kept to its first 100,000 characters. Power BI returns a whole DAX result, subject to its own limits, and the limit applies to what is kept.

Execute records nothing in the catalogue. It moves no bookmark and leaves Load and Test state as it was, whatever the source changes. A request whose response is lost may have run; Execute reports that and does not send it again.

`--json` prints the result, or the error, as one JSON document and nothing else. The command exits `0` when the source ran and `1` when it failed or its outcome is unknown.

In `weaver session` and `weaver workflow`, Execute uses the open Session. In Python, call `weaver.execute(engine, item, command, file=..., limit=...)`; it returns an `ExecuteResult`, and raises `weaver.errors.ExecuteError` for a failure and `weaver.errors.OutcomeUnknown` for an unknown outcome, both `WeaverError`s.

<!-- BEGIN GENERATED CLI -->

## Synopsis

```text
weaver execute [-h] (--command SOURCE | --file PATH) [--limit N] [--json] [--non-interactive] [--workspace WORKSPACE] [--workspace-config WORKSPACE_CONFIG] [--environment ENVIRONMENT] {tsql,spark-sql,python,dax} ITEM
```

## Positional arguments

`{tsql,spark-sql,python,dax}`
: No description is provided by the parser.

`ITEM`
: Warehouse/Name for tsql, Lakehouse/Name for spark-sql and python, SemanticModel/Name for dax.

## Options

`-h, --help`
: show this help message and exit

`--command SOURCE`
: The source to run.

`--file PATH`
: A file holding the source.

`--limit N`
: Rows read from each result set. Defaults to 100.

`--json`
: Emit the result as JSON.

`--non-interactive`
: Do not read stdin, wait for a keypress or open browser sign-in. Missing authorisation or required input is an error.

`--workspace WORKSPACE`
: Fabric Workspace name.

`--workspace-config WORKSPACE_CONFIG`
: Workspace configuration file.

`--environment ENVIRONMENT`
: Fabric Environment name or Workspace/Environment reference.

<!-- END GENERATED CLI -->
