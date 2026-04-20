# WorkPortal — Employee Login System

A modern desktop employee portal built with Python and CustomTkinter. WorkPortal provides secure employee registration, credential-based login, session management, activity logging, and a protected dashboard workspace — all wrapped in a dark-themed UI that scales fluidly with the window size.

---

## Features

- **Employee Registration** — New employees can create an account with a name and password. Duplicate names are rejected and all accounts are stored locally in a JSON file.
- **Credential Login** — Employees log in with their registered name and password. Invalid credentials are blocked with a clear error message.
- **Session Management** — A dedicated session module tracks who is logged in. Protected screens check the session state before rendering, and any unauthenticated access attempt shows a locked "Access Restricted" screen instead.
- **Activity Logging** — Every successful login is timestamped and appended to a plain-text log file. The Logs screen displays recent entries in a scrollable list, newest first.
- **Protected Dashboard** — After login, employees land on a personal dashboard showing their name and login time. The workspace area is ready to be built out with app-specific content.
- **Responsive Scaling** — All fonts and UI elements scale proportionally as the window is resized, with a debounced `<Configure>` binding that recalculates sizes without flickering.

---

## Project Structure

```
WorkPortal/
├── app.py          # Main application — UI, backend logic, all screens
├── session.py      # Session manager — tracks login state across the app
└── README.md
```

### `app.py`
Contains everything needed to run the app: backend functions for registration, credential checking, and login logging; the dynamic font scaling system; and the `WorkApp` class which manages all four screens (Login, Register, Logs, Dashboard).

### `session.py`
A small, self-contained module that holds the active login state. It exposes four functions used throughout the app:

| Function | Description |
|---|---|
| `session.login(name)` | Sets the active employee after a successful login |
| `session.logout()` | Clears the session on logout |
| `session.is_logged_in()` | Returns `True` if an employee is currently logged in |
| `session.current_user()` | Returns the logged-in employee's name |

---

## Data Storage

All data is saved locally under the user's home directory:

```
~/Work Software/
├── employee_data.json        # Registered employee accounts
└── Signing/logs/
    └── employee_logs.txt     # Timestamped login activity log
```

---

## Requirements

- Python 3.10+
- CustomTkinter

```bash
pip install customtkinter
```

---

## Running the App

```bash
python app.py
```

Both `app.py` and `session.py` must be in the same directory.

---

## Screens

| Screen | Access | Description |
|---|---|---|
| Login | Public | Enter employee name and password to sign in |
| Register | Public | Create a new employee account |
| Logs | Public | View recent login activity |
| Dashboard | **Authenticated only** | Personal workspace; blocked if not logged in |
