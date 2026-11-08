# Permissions

You do not need to be a Fabric tenant administrator for ordinary Weaver development. Run Weaver with your own Fabric sign-in or a service principal, from your computer or a Fabric notebook. Weaver uses the permissions of that running identity. Tenant settings and Azure capacity permissions are separate from workspace access.

## Workspace roles

For most Build and Load tasks, give the running identity Contributor access to the workspace where the work runs, plus read access to source data and catalogues elsewhere. Fabric workspace roles are Admin, Member, Contributor and Viewer; the table lists additional requirements for individual tasks.

| Command | What it does in Fabric | Role in the workspace it changes | Elsewhere |
| --- | --- | --- | --- |
| `weaver check` | Nothing. It reads the project folder only. | None | None |
| `weaver doctor` | Lists workspaces and items, and probes OneLake, the SQL endpoint and Spark. | Contributor, for the Spark and OneLake probes | None |
| `weaver initialise` | Creates the catalogue Warehouse, the Environment, Lakehouses and Warehouses that are missing. | Contributor | The workspace must already exist. |
| `weaver fabric environment publish` | Publishes Weaver into a Fabric Environment. | Contributor | Updating the contents of an Environment selected as the workspace default requires workspace Admin, as does changing that default. Using the published Environment does not require Admin. |
| `weaver build` | Creates and replaces objects in Lakehouses and Warehouses, creates missing semantic models and Reports, and records them in the catalogue. | Contributor | Read access to the data a [shortcut](weaver-documents/shortcut.md) points at. Binding semantic-model connections requires model ownership and access to the existing connection; Contributor alone is not ownership. |
| `weaver load`, `weaver test` | Runs Spark through the Livy API, runs Warehouse procedures, refreshes semantic models and records results in the catalogue. | Contributor | Read access to source data. Across [several catalogues](../estate/catalogue-and-health.md), Contributor in each workspace whose objects run; a catalogue read only for context needs read access. |
| `weaver health` | Reads the catalogue over T-SQL and lists Lakehouse storage. | Viewer for the catalogue; Contributor to list Lakehouse storage | Read access to each further catalogue given. |
| `weaver execute` | Runs one T-SQL, Spark SQL, Python or DAX request against one item. | Viewer for a T-SQL `SELECT`; Contributor for anything that writes or runs Spark | DAX needs model Read and Build permissions and the Execute Queries setting below. |
| `weaver wipe`, `weaver unbind` | Empties named destinations, or removes the catalogue's claims. | Contributor | None |
| `weaver mirror` | Empties and rebuilds the destination, with shortcuts into the source. | Contributor in the destination | Read access to the source catalogue, and to the source items' data through OneLake. |
| `weaver catalogue-dashboard` | Creates or updates the Dashboard's semantic model and Report, and reads each catalogue. | Contributor in the Dashboard's workspace | Read access to each catalogue. Connection binding requires model ownership and access to the connection. The Report uses the HTML Content visual; see below. |
| `weaver catalogue-dashboard export` | Queries the deployed Dashboard model and writes static files. | Model Read and Build permissions | The Execute Queries setting below, and write access to the destination folder. |
| `weaver fabric notebook push`, `run` | Creates or updates a notebook, or runs one. | Contributor | None |
| `weaver fabric capacity` | Reports, resumes or suspends a Fabric capacity through Azure. | None | Azure permissions; see below. |

**What Viewer allows.** Every workspace role, including Viewer, can read Warehouses and SQL analytics endpoints over T-SQL. Reading Lakehouse files or Delta tables through OneLake or Spark, and every write, need Contributor or higher, or an equivalent item permission.

**Power BI licences.** Semantic models and Reports in a workspace other than My workspace also need a Power BI licence; see [model and Report requirements](power-bi/requirements-and-compatibility.md).

**Shortcuts.** Creating a shortcut needs write access to the item that holds it and read access to its target. Access when reading depends on the engine and authentication path. Same-tenant OneLake passthrough uses the caller, but Direct Lake over SQL and T-SQL delegated identity paths can use the item owner. Check the effective identity and source permissions for the path you use.

**Shared Environments.** Attaching an Environment from another workspace needs Read permission on it. Both workspaces must have the same capacity and network security settings; otherwise the Spark session fails to start. The current workspace supplies the pool and compute configuration.

## Tenant settings

These settings are under **Tenant settings** in the Fabric admin portal. An administrator turns them on; you do not need an administrator role yourself.

| Setting | Section | Needed for |
| --- | --- | --- |
| Service principals can call Fabric public APIs | Developer settings | Running Weaver as a [service principal](../estate/automation-and-deployment.md). Weaver does not create workspaces or connections, so the separate setting for those is not needed. |
| Users can access data stored in OneLake with apps external to Fabric | OneLake settings | Running Weaver from a desktop or CI job, which reaches OneLake from outside Fabric. A Fabric notebook does not need it. |
| Semantic Model Execute Queries REST API | Integration settings | DAX: semantic model Tests and Assumptions, `weaver execute dax`, `weaver doctor --semantic-model` and `weaver catalogue-dashboard export`. |
| Allow visuals created using the Power BI SDK | Power BI visuals | The Catalogue Dashboard Report, which uses the HTML Content visual from AppSource. |

Execute Queries also requires model Read and Build permissions. Service principals need the Power BI API tenant setting and cannot use Execute Queries with RLS- or SSO-enabled models. These requirements apply to DAX validations and Dashboard export, not just `execute dax`. Microsoft's API documentation calls the Execute Queries tenant setting **Dataset Execute Queries REST API**; the admin portal also uses semantic-model terminology.

The Livy API that runs Spark from a desktop must also be enabled for the tenant.

**The HTML Content visual in restricted tenants.** Where SDK visuals are off, or **Add and use certified visuals only (block uncertified)** is on, an administrator can add HTML Content as an organisational visual instead. Organisational visuals are available to Reports regardless of those two settings.

## Capacity commands

`weaver fabric capacity` calls Azure Resource Manager, not Fabric, so it needs Azure permissions on the capacity resource rather than a workspace role:

| Command | Azure actions |
| --- | --- |
| `status` | `Microsoft.Fabric/capacities/read` |
| `resume` | `Microsoft.Fabric/capacities/read`, `Microsoft.Fabric/capacities/resume/action` |
| `suspend` | `Microsoft.Fabric/capacities/read`, `Microsoft.Fabric/capacities/suspend/action` |

The built-in Contributor role on the capacity includes them. Microsoft recommends a custom role limited to these actions.

Weaver never assigns a workspace to a capacity. Doing that yourself needs Admin on the workspace and contributor permissions on the capacity.

## Sources

- Microsoft. [Bind semantic model connection](https://learn.microsoft.com/en-us/rest/api/fabric/semanticmodel/items/bind-semantic-model-connection).
- Microsoft. [Create, configure, and use an Environment](https://learn.microsoft.com/en-us/fabric/data-engineering/create-and-use-environment).
- Microsoft. [Execute Queries](https://learn.microsoft.com/en-us/rest/api/power-bi/datasets/execute-queries).

- Microsoft (2026). [Roles in workspaces in Microsoft Fabric](https://learn.microsoft.com/en-us/fabric/fundamentals/roles-workspaces).
- Microsoft (2025). [Workspace roles in Fabric Data Warehouse](https://learn.microsoft.com/en-us/fabric/data-warehouse/workspace-roles).
- Microsoft (2026). [Create and run Spark Session jobs using the Livy API](https://learn.microsoft.com/en-us/fabric/data-engineering/get-started-api-livy).
- Microsoft (2026). [Secure and manage OneLake shortcuts](https://learn.microsoft.com/en-us/fabric/onelake/onelake-shortcut-security).
- Microsoft (2026). [Tenant settings index](https://learn.microsoft.com/en-us/fabric/admin/tenant-settings-index).
- Microsoft (2026). [Organizational visuals](https://learn.microsoft.com/en-us/fabric/admin/organizational-visuals).
- Microsoft (2026). [Pause and resume your Fabric capacity](https://learn.microsoft.com/en-us/fabric/enterprise/pause-resume).
- Microsoft (2026). [Manage your Fabric capacity](https://learn.microsoft.com/en-us/fabric/admin/capacity-settings).
