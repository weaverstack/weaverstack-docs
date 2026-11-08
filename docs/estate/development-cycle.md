# The development cycle

Edit a working definition, check it, inspect the Build preview, install the change, catch up data and validate the result. Use the same configuration throughout so each report describes the estate you changed.

```text
edit → check → Build preview → Build → Load → Test → Health → repeat
```

Continue the working [Landing → Operations project](connected-items.md) with `workspace-development.yml`, as selected on the mapping and Health pages. You will correct the depot on an earlier carrier event, install that change and check that the latest parcel statuses still agree with the expected rows. Use the connection task first if those items are not yet installed.

For another source-data estate, select its actual changed items in the same loop. A Warehouse-only reader can use `--item Warehouse/Operations` with the [StatusEvent project](../warehouse/tests.md). If you have added the native Parcel model and managed-source models to this project, use [the model-inclusive loop](#include-semantic-models-and-reports) below.

## Edit and iterate

Open `Lakehouse/Landing/Files/Parcel__Events.py`. In the `EVENTS` CSV constant, replace just this row:

```csv
P-1001,1,Accepted,North
```

with:

```csv
P-1001,1,Accepted,East
```

This corrects the first event's depot without changing its key or status. P-1001's later event is still `In transit` at `Central`, so its CurrentStatus should not change. Leave the logical names, imports and Operations connection intact.

Check the edited project and preview the installation:

```bash
weaver check
weaver build --item Lakehouse/Landing --item Warehouse/Operations --dry-run --workspace-config workspace-development.yml
```

Check catches declaration errors without contacting Fabric. Build preview reads existing targets and shows selected work and destructive consequences without changing the estate. Use ordinary Build for first deployment; previews require existing targets.

Look for the changed `Parcel.Events` Folder and its affected descendants in Landing. Operations is still selected so Build can reconcile its connected definitions too. A preview does not load the corrected CSV; if it shows unexpected removals or different targets, stop and correct the source or configuration. Otherwise, install and operate that selection:

```bash
weaver build --item Lakehouse/Landing --item Warehouse/Operations --workspace-config workspace-development.yml
weaver load --stale --workspace-config workspace-development.yml
weaver test --stale --workspace-config workspace-development.yml
weaver health --workspace-config workspace-development.yml
```

Inspect Landing's SQL analytics endpoint after Load:

```sql
select [Parcel ID], [Event sequence], [Status], [Depot]
from [Parcel].[Event]
where [Parcel ID] = 'P-1001'
order by [Event sequence];
```

Expect `Accepted / East` at sequence 1 and `In transit / Central` at sequence 2. Landing's `Parcel.CurrentStatus` and Operations' connected `Parcel.LakehouseCurrentStatus` should still show `In transit / Central` for P-1001. The correction reached the event history without changing which event is latest. The four Parcel validations should pass, and scoped Health should have no remaining findings if the estate was Green before the edit.

Build reconciles source against installed state, including changed definitions and affected descendants inside its selected items. Changed loadable work begins with non-Green current state. `load --stale` selects installed loadables needing work; it leaves omitted Green producers alone. `test --stale` then runs the installed validations that are new, failed, or read something the load just changed, and Health shows Load, Tests and Build together. Drop `--stale` to run every validation.

Load and catalogue-mode Test use installed definitions. After changing source data, run Load; after changing a project declaration, run Build first. Source/file Tests offer an authoring check against edited validations, returning results separately from installed Test history.

Use an item-wide run by default. Plain named Load does not add or order dependencies. [Run part of an estate](selective-runs.md) teaches deliberate seed expansion and a preview when item-wide work is too broad. Completed changes remain in place after a later failure; inspect failed steps for partial changes and follow [Recovery](recovery.md) against the state that remains.

## Include semantic models and Reports

For the [managed-source Parcel extension](../semantic-models/managed-sources.md), retain the working Landing/Operations pipelines, the native inline `Parcel` model and its linked Report, and the separate `ParcelWarehouse` model that reads Operations `Parcel.CurrentStatus`. Keep `workspace-development.yml` with the additional model and Report targets described in [workspace mappings](environments.md#a-model-and-report-variation). Source-backed Import refresh requires an existing supported SQL connection.

Build source-data definitions first, then changed model/Report definitions separately:

```bash
weaver check
weaver build --item Lakehouse/Landing --item Warehouse/Operations --dry-run --workspace-config workspace-development.yml
weaver build --item Lakehouse/Landing --item Warehouse/Operations --workspace-config workspace-development.yml
weaver build --item PowerBI/Parcel --dry-run --workspace-config workspace-development.yml
weaver build --item PowerBI/Parcel --bind-data-sources --workspace-config workspace-development.yml
weaver load --stale --workspace-config workspace-development.yml
weaver test --workspace-config workspace-development.yml
weaver health --workspace-config workspace-development.yml
```

Use this iteration loop after deploying the model and Report targets; Build preview requires those existing items. The `PowerBI/Parcel` selection covers the inline model and linked Report alongside the additional source-backed models. Preview each changed Build before applying it. `--bind-data-sources` requests binding to an existing connection; it does not create credentials. Estate Load coordinates selected source work and model refreshes; a source change can make the dependent model stale even if its definition is unchanged. DAX validations are part of Test. **Reports have only a Build/deployment lifecycle, not Load or Test.** Inspect their actual binding and rendering through the [Report task](../reports/deploy.md).

## Optional: establish a mirrored development baseline

Once the ordinary loop works, [develop using Mirror](mirror.md) if development should borrow existing source data rather than load every unchanged object locally. It requires existing destination items, reads a source in this workspace or another, and empties the destination catalogue plus selected targets. Re-mirror only for a fresh baseline, not for each edit.

[Run, test and inspect the estate](operate.md) is the installed-state path when no source change needs Build. [Build, Load and Test](../core-concepts/build-load-and-test.md) explains the operation boundaries behind both paths.
