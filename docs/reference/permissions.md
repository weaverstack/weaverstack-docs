# Permissions

Weaver uses the Fabric permissions of the identity that runs it: your own sign-in, a service principal, or the notebook user in Fabric. It needs no tenant administrator or capacity administrator role. A few tasks depend on tenant settings that an administrator controls, and the capacity commands need Azure permissions.

## Workspace roles

Fabric workspace roles are Admin, Member, Contributor and Viewer. Contributor is enough for everything Weaver changes in a workspace. Viewer is enough for some reads.

| Command | What it does in Fabric | Role in the workspace it changes | Elsewhere |
| --- | --- | --- | --- |
| `weaver check` | Nothing. It reads the project folder only. | None | None |
| `weaver doctor` | Lists workspaces and items, and probes OneLake, the SQL endpoint and Spark. | Contributor, for the Spark and OneLake probes | None |
| `weaver initialise` | Creates the catalogue Warehouse, the Environment, Lakehouses and Warehouses that are missing. | Contributor | The workspace must already exist. |
| `weaver fabric environment publish` | Publishes Weaver into a Fabric Environment. | Contributor | Only a workspace Admin can change the workspace's default Environment. |
| `weaver build` | Creates and replaces objects in Lakehouses and Warehouses, creates missing semantic models and Reports, and records them in the catalogue. | Contributor | Read access to the data a [shortcut](weaver-documents/shortcut.md) points at, in its own workspace. |
| `weaver load`, `weaver test` | Runs Spark through the Livy API, runs Warehouse procedures, refreshes semantic models and records results in the catalogue. | Contributor | Read access to source data. Across [several catalogues](../estate/catalogue-and-health.md), Contributor in each workspace whose objects run; a catalogue read only for context needs read access. |
| `weaver health` | Reads the catalogue over T-SQL and lists Lakehouse storage. | Viewer for the catalogue; Contributor to list Lakehouse storage | Read access to each further catalogue given. |
| `weaver execute` | Runs one T-SQL, Spark SQL, Python or DAX request against one item. | Viewer for a T-SQL `SELECT`; Contributor for anything that writes or runs Spark | DAX needs the Execute Queries setting below. |
| `weaver wipe`, `weaver unbind` | Empties named destinations, or removes the catalogue's claims. | Contributor | None |
| `weaver mirror` | Empties and rebuilds the destination, with shortcuts into the source. | Contributor in the destination | Read access to the source catalogue, and to the source items' data through OneLake. |
| `weaver catalogue-dashboard` | Creates or updates the Dashboard's semantic model and Report, and reads each catalogue. | Contributor in the Dashboard's workspace | Read access to each catalogue. The Report uses the HTML Content visual; see below. |
| `weaver catalogue-dashboard export` | Queries the deployed Dashboard model and writes static files. | Contributor, or any role that can query the model | The Execute Queries setting below, and write access to the destination folder. |
| `weaver fabric notebook push`, `run` | Creates or updates a notebook, or runs one. | Contributor | None |
| `weaver fabric capacity` | Reports, resumes or suspends a Fabric capacity through Azure. | None | Azure permissions; see below. |

**What Viewer allows.** Every workspace role, including Viewer, can read Warehouses and SQL analytics endpoints over T-SQL. Reading Lakehouse files or Delta tables through OneLake or Spark, and every write, need Contributor or higher, or an equivalent item permission.

**Power BI licences.** Semantic models and Reports in a workspace other than My workspace also need a Power BI licence; see [model and Report requirements](power-bi/requirements-and-compatibility.md).

**Shortcuts.** Creating a shortcut needs write access to the item that holds it and read access to the data it points at. Reading through a shortcut in the same tenant uses the caller's identity, so whoever reads it needs access to the target as well.

## Tenant settings

These settings are under **Tenant settings** in the Fabric admin portal. An administrator turns them on; you do not need an administrator role yourself.

| Setting | Section | Needed for |
| --- | --- | --- |
| Service principals can call Fabric public APIs | Developer settings | Running Weaver as a [service principal](../estate/automation-and-deployment.md). Weaver does not create workspaces or connections, so the separate setting for those is not needed. |
| Users can access data stored in OneLake with apps external to Fabric | OneLake settings | Running Weaver from a desktop or CI job, which reaches OneLake from outside Fabric. A Fabric notebook does not need it. |
| Semantic Model Execute Queries REST API | Integration settings | DAX: semantic model Tests and Assumptions, `weaver execute dax`, `weaver doctor --semantic-model` and `weaver catalogue-dashboard export`. |
| Allow visuals created using the Power BI SDK | Power BI visuals | The Catalogue Dashboard Report, which uses the HTML Content visual from AppSource. |

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

- Microsoft (2026). [Roles in workspaces in Microsoft Fabric](https://learn.microsoft.com/en-us/fabric/fundamentals/roles-workspaces).
- Microsoft (2025). [Workspace roles in Fabric Data Warehouse](https://learn.microsoft.com/en-us/fabric/data-warehouse/workspace-roles).
- Microsoft (2026). [Create and run Spark Session jobs using the Livy API](https://learn.microsoft.com/en-us/fabric/data-engineering/get-started-api-livy).
- Microsoft (2026). [Secure and manage OneLake shortcuts](https://learn.microsoft.com/en-us/fabric/onelake/onelake-shortcut-security).
- Microsoft (2026). [Tenant settings index](https://learn.microsoft.com/en-us/fabric/admin/tenant-settings-index).
- Microsoft (2026). [Organizational visuals](https://learn.microsoft.com/en-us/fabric/admin/organizational-visuals).
- Microsoft (2026). [Pause and resume your Fabric capacity](https://learn.microsoft.com/en-us/fabric/enterprise/pause-resume).
- Microsoft (2026). [Manage your Fabric capacity](https://learn.microsoft.com/en-us/fabric/admin/capacity-settings).
