from pathlib import Path
from datetime import datetime
from Checking import check_credentials

def logs(employee_name, password):
    # Verify credentials first
    if not check_credentials(employee_name, password):
        return False

    # Create logs folder if it doesn't exist
    log_folder = Path(r"C:\Work Software\Signing\logs")
    log_folder.mkdir(parents=True, exist_ok=True)

    # Create or append to log file
    log_file = log_folder / "employee_logs.txt"

    # Get current timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Create log entry
    log_entry = f"[{timestamp}] Employee: {employee_name} - Logged In\n"

    # Append to log file
    with open(log_file, "a") as file:
        file.write(log_entry)

    print(f"Login recorded for {employee_name}")
    return True

if __name__ == "__main__":
    employee_name = input("Please enter your employee name: ")
    password = input("Please enter your password: ")
    logs(employee_name, password) 