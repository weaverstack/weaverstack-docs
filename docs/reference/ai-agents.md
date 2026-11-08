# Using Weaver with AI agents

An AI coding agent can edit your Weaver project and run the same commands you use. Give it a development workspace, have it preview changes before applying them, and use the returned results to decide what to do next. This guide shows the commands and permissions for that workflow.

It applies to any agent that can run shell commands, such as Claude Code, GitHub Copilot or Codex.

## What an agent works with

- **Edit plain files.** A project is Python, SQL, TMDL and YAML in a folder. An agent reads and edits them with its ordinary tools; there is no generated code to keep in step.
- **Check source locally.** `weaver check` validates the project without contacting Fabric, so an agent can run it after every edit.
- **Preview changes.** `--dry-run` on `initialise`, `build`, `load`, `test`, `wipe`, `unbind` and `catalogue-dashboard` reports what would happen and changes nothing.
- **Read JSON results.** `--json` writes one JSON document to stdout and keeps progress off it. [JSON output](#json-output) below lists each command's fields and exit codes.
- **Configure non-interactive execution.** `--non-interactive` makes a command fail with a message, instead of waiting, when it would need input or a confirmation.
- **Check operational Health.** `weaver health --json` returns the Build, Load and validation findings for the assessed scope. Exit code `0` means that scope is Green.
- **Investigate data.** `weaver execute` submits T-SQL, Spark SQL, Python or DAX against one item. SQL and Python can change data. See [Execute reference](cli/execute.md) for results and catalogue bookkeeping.

## The loop

A change usually runs through the same commands. Give them to the agent in this order:

```bash
weaver check --json
weaver build --dry-run --json --non-interactive --workspace-config workspace-config.dev.yml
weaver build --json --non-interactive --workspace-config workspace-config.dev.yml
weaver load --stale --json --non-interactive --workspace-config workspace-config.dev.yml
weaver test --stale --json --non-interactive --workspace-config workspace-config.dev.yml
weaver health --json --non-interactive --workspace-config workspace-config.dev.yml
```

Run these commands from the project folder. Check validates files in that folder. The workspace commands use `workspace-config.dev.yml` to select the development targets. The examples request JSON results and non-interactive execution for commands that support those options. See [workspace configuration](configuration-files/workspace-config.md) for default discovery.

Run `check` after every edit. The dry run reports what Build would change. `--stale` reruns loads and validations that need attention.

Select items with `--item` to keep each run to the part of the project the agent changed. When the result is not what it expected, it can query the data with `weaver execute` or read the catalogue tables directly.

## Give the agent its own workspace

Use an identity with write access to the development workspace and only the required read access to production sources. Pass the development configuration to workspace operations. The identity's Fabric permissions determine what the agent can change; the configuration chooses its destinations. [Permissions](permissions.md) lists what each command needs.

Review destructive plans before authorising them. `--yes` accepts the confirmation prompts for `wipe`, `unbind`, `mirror` and `workflow`. Build, Load and submitted SQL or Python can also change data, so apply the same permission and review policy to that work. Keep the agent's operations in development.

With a desktop sign-in, the agent uses that sign-in's existing permissions. Use a service principal where appropriate for automation; see [Unattended execution](../estate/automation-and-deployment.md).

For development against real data, [Mirror](../estate/mirror.md) lets the development workspace borrow production's Lakehouse data through shortcuts. **Mirror empties and reconstructs the destination catalogue and selected targets**; review that reset scope before creating a baseline. Unchanged data stays borrowed while edited objects can become local. Give the effective source-reading identity read access only. Shortcut identity depends on the access path; see [shortcut permissions](permissions.md#workspace-roles).

## Instructions for the agent

Agents read standing instructions from a file in the project, such as `AGENTS.md` or `CLAUDE.md`. A starting point for a Weaver project:

```markdown
This is a Weaver project for Microsoft Fabric. Weaver documentation: https://docs.weaverstack.dev/

- Work from this project folder. For workspace operations that accept it, pass `--workspace-config workspace-config.dev.yml`. Never use the production configuration.
- Use `--json --non-interactive` where supported and read the command-specific result. `check` accepts `--json` but not `--workspace-config`; `workflow` has no `--json` result mode.
- Run `weaver check --json` after every edit.
- Preview with `--dry-run` before `build` or `load`, and report the planned changes.
- When investigating an unexpected result, start with a read-only Execute query against the intended development item. For example: `weaver execute tsql Warehouse/Operations --command "SELECT TOP 10 [Parcel ID], [Status], [Depot] FROM [Parcel].[CurrentStatus] ORDER BY [Parcel ID]" --workspace-config workspace-config.dev.yml --json --non-interactive`. Choose the engine and item for the actual task; do not query production by substituting its physical name.
- Ask for approval before submitting SQL or Python that mutates data, as well as before `wipe`, `unbind`, `mirror` or confirming a workflow. Execute has no read-only or dry-run flag: review the submitted code and use identity permissions to enforce access. Keep only required read access to production sources; never write Weaver-owned catalogue rows.
- If Execute reports an unknown outcome or loses its response, stop and inspect the resulting state before any retry. The request may already have run.
- Finish by checking Health for the intended development scope with `weaver health --json --non-interactive --workspace-config workspace-config.dev.yml`. Report the status, any findings, and whether the full requested scope was assessed. Run the project’s Tests and Assumptions to check the declared data and business rules.
```

## Migrating a dbt project

For moving an existing dbt project to Weaver, weaverstack.dev has a [migration brief written for an agent](https://weaverstack.dev/vs-dbt/#migrating-from-dbt): what to read in the dbt project, which decisions to confirm with you, and how to validate the result.

## JSON output

Each command with `--json` writes one JSON result document. Use the command-specific fields listed below. A `format_version` field identifies a versioned output format; treat unversioned shapes as specific to the Weaver version in use.

`check` has local-source options and accepts `--json`; workspace configuration options belong to the workspace commands. `workflow` uses text output. Use each command’s documented options rather than attaching the same flags to every command.

### Stream and process behaviour

Commands with `--json` write the result document to stdout and do not prompt. Their Session enters machine-output mode, suppressing its ordinary reports and progress; representation tests require stderr to remain empty for normal JSON Load, Test, and Health output. Parser help and parser usage errors happen before command JSON handling and retain `argparse`'s text streams. `fabric environment publish` follows the same output choice: human-readable output by default, JSON with `--json`.

A handled Weaver error under `--json` has this current shape:

```json
{
  "status": "failed",
  "error": {
    "executor": "TDS",
    "message": "..."
  }
}
```

`executor` is omitted when no executor reported the error. Load may also add `report`, containing its partial load report. A Test or Assumption failure that produced a validation report emits that report directly instead of the generic error envelope.

Successful command outcomes normally exit `0`. A report that does not satisfy the command's success condition, a handled Weaver error, a refused confirmation, or a failed waited-for notebook run exits `1`. `argparse` usage errors write diagnostics to stderr and exit `2`. Do not treat this as a universal exit-code protocol for unhandled Python or host failures.

### Commands with `--json`

| Command | Current top-level fields | Current exit condition |
| --- | --- | --- |
| `initialise` / `initialize` | `project_folder`, `workspace`, `resources`, `files`, `example`, `example_added`, `environment_publication`, `environment_definition`, `dry_run`, `next_commands` | `0` for a produced report; handled setup errors return `1` through the error envelope. |
| `doctor` | `workspace`, `authentication`, `workspaces`, `succeeded`, `checks` | `0` only when the report succeeds; otherwise `1`. |
| `check` | `status`, `project_folder` | `0` for valid source; `1` with the error envelope for a Weaver error. |
| `build` | `source`, `items`, `bundle_id`, `installation`, `bundle_path`, `status`, `errors` | `0` when `status` is `succeeded`; otherwise `1`. |
| `install` | `bundle_id`, `status`, `started_at`, `finished_at`, `sequences` | `0` when the installation report succeeds; otherwise `1`. |
| `load` | `requested`, `status`, `dry_run`, `fault_tolerant`, `reload`, `ignore_stability_threshold`, `workspace`, `workflow_id`, `started_at`, `finished_at`, `order`, `edges`, `nodes`, `messages` | `0` for `succeeded` or `succeeded_with_rejects`; otherwise `1`. |
| `test` | `status`, `nodes`, `totals`, `workflow_id`, `started_at`, `finished_at` | `0` for a completed passing or planned report; failed or invalid validation returns `1` while still emitting the report. |
| `health` | `format_version`, `generated_at`, `as_of`, `status`, `targets`, `sections`, `current_load`, `load_activity` | `0` only for Green; Amber or Red returns `1`. |
| `execute` | `status`, `engine`, `item`, `target`, `limit`, `seconds`, `result_sets`, and `output` where Python printed any | `0` after the request returns; a handled error returns `1` through the error envelope. |
| `catalogue-dashboard` | `workspace`, `catalogue`, `catalogues`, `mode`, `name`, `items`, `sources`, `dry_run`, `status`, `errors`, `warnings` | `0` when `status` is `succeeded`; otherwise `1`. |
| `catalogue-dashboard export` | `workspace`, `name`, `path`, `pages` | `0` after the pages are written; a handled error returns `1`. |
| `wipe --dry-run` | `workspace`, `targets`, `catalogue`, `catalogue_action`, `unbound` | `0` after reporting the settled plan. |
| `wipe` | `workspace`, `plan`, `items`, `unbound`, `dry_run` | `0` after the operation returns; refusal or a handled operation error returns `1`. |
| `unbind --dry-run` | `workspace`, `catalogue`, `targets` | `0` for a settled plan, `1` for refusal/error. |
| `unbind` | `workspace`, `catalogue`, `targets`, `unbound`, `dry_run` | `0` for a completed plan/deletion, `1` for refusal/error. |
| `mirror` | `workspace`, `source_catalogue`, `destination_catalogue`, `wiped`, `copied`, `uncopied`, `items`, `mirrored`, `status` | `0` after the operation returns; refusal or a handled operation error returns `1`. |
| `fabric environment publish` | `workspace_id`, `workspace_name`, `environment_id`, `environment_name`, `weaver_requirement`, `mode`, `action`, `published`, `publish_status`, `timings` and mode-specific publication details | `0` for successful publication or an already matching definition; errors return non-zero. |
| `fabric notebook push` | `workspace`, `notebook`, `notebook_id`, `source`, `action` | `0` after create or update; handled errors return `1`. |
| `fabric notebook run` | `workspace`, `notebook`, `notebook_id`, `job_url`, `status`, `exit_value` | Waited runs return `0` when completed or deduped. `--no-wait` returns `0` for the accepted job. A handled failure returns `1`. |

Only Health currently includes a top-level JSON `format_version`; its current value is `2`. A Build result's `bundle_id` identifies the bundle contents, but the Build result is not the bundle manifest and has no result format version.

### Commands without JSON result mode

`session`, `workflow`, and `fabric capacity` have no `--json` option. A bare invocation, `--help`, and `--version` also use text output. Their terminal presentation is not a stable machine format; do not parse it as a substitute JSON schema.

### Nested field shapes

#### Initialise

`resources[]` has `role`, `name`, `status`, and nullable `action`. `example` has `generated`; `example_added` repeats that Boolean for the current representation. `files` and `next_commands` are arrays of strings. `dry_run` is Boolean.

#### Doctor

`checks[]` has `name`, `status`, nullable `detail`, nullable `remedy`, and nullable `via`. Current check statuses are `ok`, `not tested`, `missing`, `failed`, and `error`. `authentication` is a provider mapping and `workspaces[]` contains Fabric workspace mappings; their provider-owned nested fields are not normalized by Weaver.

#### Build

`items[]` contains logical item references. `installation` is Boolean and `bundle_path` is a string or null. `errors[]` has `id`, nullable `type`, nullable `message`, nullable `artefact`, and nullable `source`. An installation result additionally has `actions` (total/succeeded/skipped/failed counts) and `report_path`. A dry-run result adds `dry_run: true` and `preview`, containing `plan`, `objects`, `actions`, `no_op`, `destructive`, `uncertain`, certification/validation/runtime-state decisions, omissions and `execution_runtime_checked: false`. Preview is not a retained bundle or proof that the runtime can execute it.

#### Install

`sequences[]` has `number`, `description`, `status`, and `actions`. Each action has `action_id`, nullable `resource_node_id`, `target_id`, `executor`, `status`, nullable `started_at`, nullable `finished_at`, and nullable `duration_seconds`. `source_path`, `error_type` plus `error_message`, and `details` appear only when present.

#### Load

`order[]` contains node IDs and `edges[]` contains two-element node-ID arrays. `nodes[]` has:

- `node_id`, nullable `logical_id`, `physical_target`, `primitive_kind`, and nullable `dispatch_location`;
- `status`, `executed`, nullable `started_at`, and nullable `finished_at`;
- nullable `rows`; and
- `messages[]`.

When present, `rows` is primitive result evidence. Data loads carry row counts; semantic refresh carries refresh evidence without invented row counts. Message objects currently carry `code`, `severity`, and `message`, with optional context fields supplied by the run representation. Status vocabulary differs between execution and dry run; do not infer another command's status set from it.

#### Test

`totals` has `planned`, `executed`, `passed`, `failed`, `invalid`, `missing_count`, `unexpected_count`, and `violation_count`. `nodes[]` has `logical_id`, `kind`, `physical_target`, `primitive_kind`, nullable `dispatch_location`, `status`, `executed`, `messages`, nullable timestamps, and result-specific count/error fields.

A Test result adds `missing_count`, `unexpected_count`, and nullable `error_message`. An Assumption result adds `violation_count` and nullable `error_message`. When name/file filtering requests diagnostics and rows are available, that node also has `diagnostics`; values such as datetimes and bytes are converted to ISO strings and hexadecimal strings by the CLI JSON renderer.

#### Health

`sections` is an object with `load`, `tests`, and `build`. Each section has `status`, `subjects`, `counts`, and `findings`. A finding has `area`, `code`, `severity`, nullable `status`, `message`, nullable `object_id`, nullable `target`, nullable `workflow_id`, nullable timestamps, and nullable `failure_count`.

`current_load` is null or has `workflow_ids`, nullable timestamps, and `counts`. `load_activity[]` has object and target identity, workflow and timing fields, row counts, `is_reload`, and `is_static_skip`. Health timestamps are ISO 8601 strings. `format_version: 2` versions this report only; it says nothing about the other command documents.

Given more than one `--catalogue`, Health writes a joined document instead: `format_version` `1`, `generated_at`, `as_of`, `status`, `complete`, `catalogues` and `cycles`. Each `catalogues[]` entry has `label`, `catalogue`, `status`, nullable `error`, and nullable `report`, which is that catalogue's ordinary Health document above. `complete` is false when a catalogue could not be read or assessed. `cycles[]` lists each dependency cycle once, as its member node IDs. The exit code follows the joined `status`.

#### Wipe

A dry-run `targets[]` entry has `target` and Boolean `catalogue`; entries can add recorded logical `items`. The plan always emits `preserve_data_source` and `left` (retained targets such as Reports). A completed result embeds that same shape as `plan`. Its `items[]` entries have `target`, `outcome`, Boolean `catalogue`, Boolean `unbound`, and a `counts` mapping. Top-level `unbound` is null or the catalogue-unbind result mapping.

#### Unbind

`targets[]` entries have `target`, `items` (logical claims) and `in_fabric`. The result adds `unbound` logical items and `dry_run`; no physical-delete count is emitted because no physical item changes.

#### Mirror

`copied` maps catalogue table names to copied row counts. `uncopied[]` names historical catalogue tables rebuilt without copied rows. `items[]` names mirrored logical items. `mirrored` maps each item to the operation-specific result: all item results include `source` and `target`, while Lakehouse and Warehouse entries expose different count fields for the physical work performed.

#### Fabric notebooks

Notebook push `action` is currently `created` or `updated`. Notebook run preserves Fabric's status spelling. With `--no-wait`, the current status is `Accepted` and `exit_value` is null.

### Environment publication JSON

`weaver fabric environment publish --json` emits the following fields. Without the flag, it prints a human-readable publication summary:

```text
workspace_name, workspace_id,
environment_name, environment_id,
source_path, mode, weaver_requirement, wheel_filename,
removed_wheels, action, published, publish_status, timings
```

`source_path`, `weaver_requirement`, and `wheel_filename` are nullable. `removed_wheels` is an array. `mode` is `released` or `dev`; `action` is `created`, `updated`, or `unchanged`; `published` records whether this invocation asked Fabric to publish. `timings` is a mapping of measured phase names to seconds and the CLI adds `total`.

This document has no `format_version`. A handled publication error exits `1` and uses the selected human or JSON error rendering. Parser errors remain text output and exit `2`.

### Compatibility boundary

Validate the command-specific fields your scripts need and reject unexpected shapes. Where `format_version` is absent, the document is unversioned; do not treat it as an implicit version 1.
