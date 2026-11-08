# Using Weaver with AI agents

An AI coding agent can work on a Weaver project the way a developer does: edit the project's files, check them, preview a change, apply it in Fabric and read back what happened. Weaver gives it what that needs: plain source files, a local check, previews, one JSON document per command and no prompts when asked for none.

This page sets up that loop and the boundaries to give an agent. It applies to any agent that can run shell commands, such as Claude Code, GitHub Copilot or Codex.

## What an agent works with

- **Plain files.** A project is Python, SQL, TMDL and YAML in a folder. An agent reads and edits them with its ordinary tools; there is no generated code to keep in step.
- **A local check.** `weaver check` validates the project without contacting Fabric, so an agent can run it after every edit.
- **Previews.** `--dry-run` on `initialise`, `build`, `load`, `test`, `wipe`, `unbind` and `catalogue-dashboard` reports what would happen and changes nothing.
- **JSON results.** `--json` writes one JSON document to stdout and keeps progress off it. The [machine-readable output](../reference/machine-readable-output.md) reference lists each command's fields and exit codes.
- **No prompts.** `--non-interactive` makes a command fail with a message, instead of waiting, when it would need input or a confirmation.
- **Explicit authorisation.** `wipe`, `unbind` and `mirror` ask before they empty or unbind anything, and `workflow` asks before such a step. `--yes` answers that question and does nothing else; under `--non-interactive`, a missing `--yes` is an error, so an agent that is not given it cannot empty a target.
- **An acceptance check.** `weaver health --json` exits `0` only when the estate is Green, so an agent can tell whether its work left anything failed, stale or untested.
- **Inspection.** `weaver execute` runs a T-SQL, Spark SQL, Python or DAX query against one item and records nothing, so an agent can look at data without changing state.

## The loop

A change usually runs through the same commands. Give them to the agent in this order:

```bash
weaver check --json                                   # after every edit
weaver build --dry-run --json --non-interactive       # what Build would change
weaver build --json --non-interactive
weaver load --stale --json --non-interactive          # only what is now behind
weaver test --stale --json --non-interactive
weaver health --json --non-interactive                # exit 0 means Green
```

Select items with `--item` to keep each run to the part of the project the agent changed. When the result is not what it expected, it can query the data with `weaver execute` or read the catalogue tables directly.

## Give the agent its own workspace

Run an agent against a development workspace, never production:

- Give its identity Contributor in the development workspace, and in production only read access to the data it works from. [Permissions](../reference/permissions.md) lists what each command needs.
- Give it real data with [Mirror](../estate/mirror.md): the development workspace borrows production's Lakehouse data through shortcuts, and only what is built there changes. Reading through a shortcut uses the reader's own access, so the agent can read production data but not change it.
- Point every command at the development configuration with `--workspace-config`, so a missing flag cannot reach another workspace.
- Sign the agent in as yourself on a desktop, or as a service principal in automation. [Unattended execution](../estate/automation-and-deployment.md) covers service principals.

## Instructions for the agent

Agents read standing instructions from a file in the project, such as `AGENTS.md` or `CLAUDE.md`. A starting point for a Weaver project:

```markdown
This is a Weaver project for Microsoft Fabric. Weaver documentation: https://docs.weaverstack.dev/

- Use `--workspace-config workspace-config.dev.yml` on every command. Never use the production configuration.
- Pass `--json --non-interactive` to every command and read the JSON on stdout.
- Run `weaver check --json` after every edit.
- Preview with `--dry-run` before `build` or `load`, and report the planned changes.
- Never pass `--yes` to `wipe`, `unbind`, `mirror` or `workflow` without asking first.
- Finish with `weaver health --json --non-interactive`. Exit code 0 means Green; report anything else.
```

## Migrating a dbt project

For moving an existing dbt project to Weaver, weaverstack.dev has a [migration brief written for an agent](https://weaverstack.dev/vs-dbt/#migrating-from-dbt): what to read in the dbt project, which decisions to confirm with you, and how to validate the result.
