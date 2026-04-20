# session tracks the active login session
# Import this anywhere you need to check or update login state.

_active_employee: str = ""


def login(employee_name: str) -> None:
    """Call this when an employee successfully logs in."""
    global _active_employee
    _active_employee = employee_name


def logout() -> None:
    """Call this when an employee logs out."""
    global _active_employee
    _active_employee = ""


def is_logged_in() -> bool:
    """Returns True if someone is currently logged in."""
    return bool(_active_employee)


def current_user() -> str:
    """Returns the active employee's name, or empty string if nobody is logged in."""
    return _active_employee