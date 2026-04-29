# Global interface

Every page shares the same top bar:

| Element | What it does |
|---|---|
| **Logo** | Returns to the Dashboard. |
| **Main navigation** | Dashboard, Workspaces, Findings, Runners, Reports, (Features for owners). |
| **Search** | Global search across workspaces and runners. Type at least 2 characters; results refresh after 500 ms (debounced); matches are prefix-based and case-insensitive. Each result shows the entity type and a short context line. |
| **Organization switcher** | Switch between organizations you belong to. Shows the current org's name and description. |
| **Theme toggle** | Light, Dark, or System (follows OS preference). The choice is remembered across sessions. |
| **Notifications bell** | Shows the unread count, refreshing every 30 seconds. Click to read recent notifications, mark them as read, or jump to the related runner / finding / workspace. Notification subscriptions are configured per workspace under *Workspace settings → Notifications*. |
| **User menu** | Profile, Organization, API Keys, run-hours indicator, Logout. |

### Mobile usage

The interface is fully responsive:

- **Hamburger menu** replaces the top navigation; tap to open a drawer with the main links.
- **Sheets** (full-height side panels) replace popovers for forms and detail views, making editing comfortable on small screens.
- **Tables** become single-column cards on narrow viewports; sort/filter controls move into a bottom sheet.
- **Touch targets** are sized for thumbs.
- The **organization switcher** and **user menu** open as bottom sheets.
