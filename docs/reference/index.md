# Reference

Use Reference to look up current public interfaces, exact representations and operation behaviour. For a worked task, start with [Lakehouse](../lakehouse/index.md), [Warehouse](../warehouse/index.md), [Semantic models](../semantic-models/index.md), [Reports](../reports/index.md) or [Coordinate your estate](../estate/index.md).

## Changes for 0.11

This documentation previews 0.11 behaviour. The additions below require that release or a matching development build; installing from PyPI selects the published package, not unreleased source.

- Keep separate team projects and [assess, load or test across their catalogues](../estate/across-catalogues.md). Supply catalogue context and select the work independently.
- Use [Python workflows](python/session.md#workflows) to share a Session and configuration and correlate recorded Load/Test work. [Test stale validations](operation-behaviour/test.md#stale-selection) to rerun failed, invalid, Pending or stale results.
- [Execute](cli/execute.md) submits commands or files in T-SQL, Spark SQL, Python and DAX without authoring a Weaver document. SQL and Python can change data.
- [Mirror Lakehouse items across workspaces](../estate/mirror.md#mirror-from-another-workspace), retain local materialisation records, and [use a shared Environment](../lakehouse/runtime.md#use-a-shared-environment). Report-only initialisation supplies a catalogue without an Environment.
- Deploy the [multi-catalogue Dashboard](../estate/catalogue-dashboard.md), choose Direct Lake for up to ten catalogues or Import for more than ten, and export static HTML snapshots.
- Python-style names split at the first `__`; later separators remain in the object name. [Naming rules](operation-behaviour/shared-selection-and-identity.md) retain the schema restriction.

The release also corrects installation lookup for single-item work, publishes Folder files through the mount used by readers, excludes housekeeping columns from generated model source shapes, waits for shortcut columns to become available, and corrects Build/prune ordering. These are fixes to existing workflows, not new deployment modes. [Dependency cycles](../estate/across-catalogues.md#cycles) now use deterministic execution order without convergence iteration.

## Find the definition for your item

| Item | Authored definitions and relevant interfaces |
| --- | --- |
| Lakehouse | [Python and Spark SQL Tables](weaver-documents/table.md), [Folders](weaver-documents/folder.md), [Shortcuts](weaver-documents/shortcut.md), [Python authoring](python/objects.md) and [runtime requirements](operation-behaviour/session-runtime.md#fabric-environment-qualification). |
| Warehouse | [T-SQL Tables](weaver-documents/table.md#t-sql), [Views](weaver-documents/view.md), [schema metadata](weaver-documents/schema-metadata.md) and [programmables](weaver-documents/warehouse-programmable.md). |
| Semantic models | [Native layout](power-bi/project-layout.md#model-discovery-and-identity), [TMDL merging](power-bi/tmdl.md), [annotations](power-bi/annotations.md), [extension API](python/semantic-models.md) and [DAX validations](power-bi/validations.md). |
| Reports | [Discovery and local model association](power-bi/project-layout.md#report-discovery-and-association), [deployment binding](power-bi/requirements-and-compatibility.md#report-binding) and [target mappings](configuration-files/workspace-config.md#targets). |

For Lakehouse and Warehouse validation declarations, use [Test](weaver-documents/test.md), [Assumption](weaver-documents/assumption.md) and [Python validation objects](python/validation.md). [Test behaviour](operation-behaviour/test.md) distinguishes installed definitions and recorded results from source/file execution. Reports have no Load or Test; refresh and validate their semantic model.

## Look up a shared operation

[Selection and identity](operation-behaviour/shared-selection-and-identity.md) defines item and document names. [Load selection](operation-behaviour/load.md#selection) defines whole-name regular expressions and ancestor/descendant expansion; [reload](operation-behaviour/load.md#reload) defines the destructive scope. [Workspace execution settings](configuration-files/workspace-config.md#execution) defines resource ceilings alongside the invocation caps in [Build](cli/build.md), [Load](cli/load.md) and [Test](cli/test.md).

[Model source mappings and connections](power-bi/requirements-and-compatibility.md#source-mapping-and-connections) are distinct from destination names and credentials. [Build behaviour](operation-behaviour/build.md#inputs-and-selection) defines the separate source-item and model/Report Build calls. For recorded estate evidence, use [Health behaviour](operation-behaviour/health.md) and the [catalogue schema](catalogue-schema.md).

## Complete reference areas

| Area | Use it to look up |
| --- | --- |
| [Weaver documents](weaver-documents/overview.md) | Authored locations, forms and metadata. |
| [Semantic models and Reports](power-bi/index.md) | Native project layout, TMDL policy/composition, annotations, DAX validations and compatibility modes. |
| [Python API](python/index.md) | Public exports, call shapes and result types. |
| [CLI](cli.md) | Commands, options and shared CLI behaviour. |
| [Configuration files](configuration-files/index.md) | Workspace, workflow and Fabric Environment definitions. |
| [Operation behaviour](operation-behaviour/index.md) | Selection, state changes, outcomes and failure boundaries. |
| [Catalogue schema](catalogue-schema.md) | Public `_` tables, columns, types and keys. |
| [Build bundle format](build-bundle-format.md) | Manifest, payload and destination-bound installation handoff. |
| [Using Weaver with AI agents](ai-agents.md) | Running Weaver from an agent, and the JSON each command writes with its exit codes. |
| [Permissions](permissions.md) | Workspace roles, tenant settings and Azure permissions each command needs. |

For options in an installed CLI version, run:

```bash
weaver <command> --help
```

These pages record current formats where no separate compatibility policy exists. They do not make every machine shape or stored column a stable cross-version contract.
