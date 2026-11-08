# The development cycle

A typical development cycle involves editing a query or transformation, trying the change against development data and checking the result before releasing it. In Fabric, you may also need to update dependent tables, refresh a model and check whether earlier test results still apply to the changed data.

Weaver gives you a consistent set of commands for that work. You can check your files locally, review the deployment before applying it, then load and test the installed change. Health brings the results together so you can see what still needs attention. This guide takes one small correction through the loop and shows you how to check both the changed data and the results that should stay the same.

```text
edit → check → Build preview → Build → Load → Test → Health → repeat
```

The example starts with the working [Landing → Operations project](connected-items.md) and `workspace-development.yml` from the mapping and Health pages. It corrects the depot on an earlier carrier event, then checks both the correction and the latest parcel statuses that should remain unchanged. The connection task sets up these items if they are not yet installed.

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

Load and catalogue-mode Test use installed definitions. A source-data change needs another Load, while a changed project declaration needs Build before the installed work can use it. Source/file Tests offer an authoring check against edited validations, returning results separately from installed Test history.

An item-wide run is usually the simplest starting point because it follows the installed item's dependency graph. Plain named Load has a narrower purpose: it selects matching objects without automatically adding or ordering dependencies. [Run part of an estate](selective-runs.md) explains deliberate seed expansion and its preview when item-wide work is too broad. Completed changes remain in place after a later failure; [Recovery](recovery.md) explains how to inspect partial changes and work from the state that remains.

## Include semantic models and Reports

The [managed-source Parcel extension](../semantic-models/managed-sources.md) adds model work to the same loop. Its starting state includes the working Landing/Operations pipelines, the native inline `Parcel` model and linked Report, and the separate `ParcelWarehouse` model over Operations `Parcel.CurrentStatus`. The model and Report targets are already in `workspace-development.yml`, as described in [workspace mappings](environments.md#a-model-and-report-variation). Source-backed Import refresh requires an existing supported SQL connection.

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

[Mirror](mirror.md) provides an optional baseline for the ordinary development loop: development borrows existing source data rather than loading every unchanged object locally. It requires existing destination items, reads a source in this workspace or another, and empties the destination catalogue plus selected targets. Re-mirroring is a reset to a fresh baseline, not part of each edit.

[Run, test and inspect the estate](operate.md) is the installed-state path when no source change needs Build. [Build, Load and Test](../core-concepts/build-load-and-test.md) explains the operation boundaries behind both paths.
