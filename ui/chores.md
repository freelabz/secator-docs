# Chores & owner features

### Chores

Chores are scheduled background jobs (recurring scans, attack-surface monitoring, cleanup tasks). They are created automatically whenever you launch a runner with anything other than *Once* in the [Scheduling tab](runners.md#scheduling-a-run) — that turns the runner into a chore.

The **Chores** page lists all chores with their schedule (next-run time, frequency) and last-run status. Clicking a chore opens a detail view similar to a runner: status, next run, full execution history, logs.

From a chore detail page you can:

- **Pause / Resume** the schedule without losing its history.
- **Edit** the schedule (switch from daily to weekly, change the natural-language expression).
- **Delete** the chore — past runs stay archived in the Runners list.
- **Run now** — trigger an out-of-band execution without affecting the next scheduled tick.

> [!note]
> Chores must be enabled for the workspace by an **owner** on the [Features](chores.md) page first. Without that toggle, the *Scheduling* tab on the Run form will let you pick a schedule but the chore won't actually start firing.

### Features (owner only)

The **Features** page is visible only to users with the *owner* role. Non-owners are redirected to the Dashboard.

From here an owner can:

- **Pick a workspace** to configure (if more than one exists).
- **Toggle optional features** for that workspace, including chore-based automation (attack-surface monitoring, AI suggestions, scheduled scans).
- **Open the Chores page** directly to inspect what is currently scheduled.

A warning is shown if you try to toggle features on the *system* workspace.
