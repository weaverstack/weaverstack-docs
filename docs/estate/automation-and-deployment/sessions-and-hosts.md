---
meta_title: Microsoft Fabric automation | Weaver docs
description: Automate Weaver build, load, test and health operations across Microsoft Fabric from desktop runners or Fabric-hosted processes.
social_title: Microsoft Fabric automation with Weaver
image_alt: Weaver logo.
schema_type: TechArticle
breadcrumbs:
  - name: Weaver documentation
    url: https://docs.weaverstack.dev/
  - name: Workflows and controlled deployment
    url: https://docs.weaverstack.dev/estate/automation-and-deployment/
  - name: Microsoft Fabric automation
    url: https://docs.weaverstack.dev/estate/automation-and-deployment/sessions-and-hosts/
---

# Sessions and execution contexts

Every Weaver operation reaches Fabric through a Session, and where Weaver runs decides which capabilities that Session can acquire. A command that works at your interactive desktop therefore does not by itself define an unattended job. For automation you settle three things: where Weaver runs, how that process authenticates without interaction, and which result your job reads as the machine interface. [Workflows and controlled deployment](index.md) shows the commands; this page explains the context they run in.

## The host supplies the execution context

Weaver exposes the same lifecycle operations from a desktop process and from Python running inside Fabric, but each host supplies different capabilities.

| Context | Workspace and identity | Spark and data access |
| --- | --- | --- |
| Desktop or external runner | Resolves the configured Fabric workspace and uses the desktop credential chain. | Uses Fabric APIs, OneLake and Warehouse SQL endpoints. Lakehouse Python or Spark SQL work acquires a remote Spark session in the target workspace. Hosted Lakehouse Build/Load/Test needs a published Weaver Environment, including generated Spark SQL work. Spark-backed Build checks matching runtime compatibility before mutation. |
| Fabric process addressing its attached workspace | Uses the notebook's current workspace and notebook identity. | Uses the active Spark session, notebook storage context and Fabric-hosted item resolution. Desktop credentials are not substituted. |
| Fabric process addressing another workspace | Uses the cross-workspace Session path and authenticates to the requested workspace independently. | Acquires capabilities for that target workspace; it does not reuse the notebook's attached Lakehouse or identity as though the workspaces were one host. |

A Session belongs to one physical workspace, and Weaver does not move it to another between commands. If the selected host cannot supply a required capability, the operation fails; Weaver does not fall back to local execution or silently change target. Livy is one mechanism Weaver uses when remote Spark execution is needed; it is not the definition of a Session.

Standalone Power BI deployment and refresh, and DAX file-mode validation, need their REST and query capabilities but not a catalogue or Spark runtime. They return operation reports without persisted Weaver history.

For hosted Spark work, publish the same Weaver release your runner uses into the Fabric Environment. [Running Python in Fabric](../../lakehouse/runtime.md) explains publication.

## A Session reuses acquired capabilities

A standalone operation creates a Session and closes it afterwards. An interactive session, a workflow or your Python code can instead supply one Session to several operations, and a Session that you supplied stays open after each operation completes. A Session closes only the resources it opened.

Weaver acquires capabilities from the host only when an operation needs them: authentication, workspace and item resolution, Warehouse connections, OneLake access, Spark execution context. A Warehouse-only operation does not start Spark because other operations support Lakehouses. Once Weaver has acquired a healthy capability, later commands in the same workspace reuse it, and concurrent requests for the same capability share one acquisition. Reuse avoids reacquiring remote resources for every command. It does not change what Build, Load, Test or Health means, and it does not merge their selections or state changes.

A failed authored statement does not by itself discard a healthy capability. A capability or remote-session failure can make it unavailable to the failed operation, and a later operation may reacquire it a bounded number of times. Closing the Session releases the capabilities it acquired; Weaver does not start unused ones in order to close them.

## A Workflow orders ordinary commands

A Workflow is a named, ordered list of Weaver commands that you list once; Weaver parses and runs each entry as the same command available outside the Workflow:

```text
Build → Load → Test → Health
```

Each entry keeps its normal selection, validation, state changes and failure behaviour, so a Workflow is not a second execution language. The sequence runs in one Session and one workspace configuration. A mixed project uses a source-item Build followed by a separate Power BI Build, and a Workflow can run both without combining their Build selection modes. Weaver can prepare the combined capabilities the commands need before the first entry. That changes startup timing, not command selection, authority or failure behaviour. Load and Test evidence produced during the sequence shares a workflow identifier, which makes related outcomes easier to correlate.

In Python, `with weaver.workflow():` is the same composition. Operations inside it use the workflow's Session and configuration without `session=`, and Load and Test record under its workflow identifier. Your Python code decides the order and what a finding means: Test returns its report inside a workflow as it does outside one. See [Workflows](../../reference/python/session.md#workflows).

### Composition does not create a transaction

Commands still complete one at a time. An execution error stops later commands, and changes made by earlier commands remain. Test and Health findings do not stop the sequence; the completed workflow then exits unsuccessfully. An exception from a query or command is not a finding. The failing command leaves whatever partial state its own behaviour defines, and a Workflow adds no operation-wide rollback around the sequence.

A Workflow records an accepted operating sequence; it does not hide the boundaries between its steps. After a failure, diagnose and recover the operation that failed, then rerun the appropriate sequence against the state that remains. [Fault tolerance](../recovery/fault-tolerance.md) explains partial state across commands. The [Workflow operation reference](../../reference/operation-behaviour/workflow.md) owns the file format and execution rules, and [Session and runtime behaviour](../../reference/operation-behaviour/session-runtime.md) owns capability and host behaviour.

## Make unattended policy explicit

Non-interactive policy and destructive authorisation are separate controls.

- Non-interactive execution forbids reading standard input, waiting for keypresses and opening browser sign-in. Missing input or authorisation becomes an error.
- Destructive authorisation approves the destinations or sequence the command has already settled. It does not configure credentials or make the process non-interactive.

An unattended job that may empty or reconstruct state needs both. Keep the workspace configuration, item selection and artifact identity under change control, so that the scope you authorised is the scope the job resolves.

For a workflow you authorise the whole sequence before it starts. Weaver passes that authorisation to the entries, while the non-interactive policy can only become stricter inside the sequence. The [CLI reference](../../reference/cli.md) identifies which commands expose each control and which operations are destructive.

## Supply credentials before the job starts

For desktop execution, the CLI credential chain tries a configured service principal and then an existing Azure CLI sign-in. Interactive execution can also use browser sign-in, which non-interactive execution omits.

Store service-principal secrets or certificate material in the runner's secret store, not in project files, workflow definitions, command arguments or bundles. The identity also needs the Fabric control-plane, SQL and OneLake permissions the selected operations require; authenticating successfully does not imply permission to every target capability.

Inside the attached Fabric workspace, the notebook identity is the host credential, and desktop credential environment variables do not replace it. A request from a Fabric process to another workspace authenticates independently through the cross-workspace context.

To tell credential and connectivity failures apart from lifecycle failures, run Doctor in the same runner and interaction mode. See [Session and runtime behaviour](../../reference/operation-behaviour/session-runtime.md) for credential selection and host boundaries.

## Treat machine-readable output as the automation interface

For a command that advertises machine-readable output, read that output together with the process status:

1. capture standard output as the command-specific result document;
2. keep standard error separate for authentication, configuration and host diagnostics;
3. fail the job on a non-zero process status; and
4. validate the fields the automation consumes rather than parsing the human renderer.

No single JSON schema covers every Weaver command, and not every command has JSON output. A workflow gives you ordered execution and a process status, not a universal envelope for nested results; to get one operation's structured report, run that operation directly through its machine interface. Unversioned result documents carry no long-term compatibility promise. [JSON output](../../reference/ai-agents.md#json-output) records the exact fields, stream behaviour and exit conditions for each command.
