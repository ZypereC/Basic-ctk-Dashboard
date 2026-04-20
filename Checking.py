import json
import os

def check_credentials(employee_name, password):
    # File location
    folder = r"C:\Work Software"
    file_path = os.path.join(folder, "employee_data.json")

    # Check if the file exists
    if not os.path.exists(file_path):
        print("No employee data found. Please sign in first.")
        return False

    # Read existing data from JSON file
    with open(file_path, "r") as file:
        try:
            data_list = json.load(file)
        except json.JSONDecodeError:
            print("Employee data is corrupted. Please sign in again.")
            return False

    # Check credentials against stored data
    for employee_data in data_list:
        if (employee_data["employee_name"] == employee_name and
                employee_data["password"] == password):
            print("Credentials are correct. Access granted!") 
            return True

    print("Invalid credentials. Access denied.")
    return False

if __name__ == "__main__":
    employee_name = input("Please enter your employee name: ")
    password = input("Please enter your password: ")
    check_credentials(employee_name, password) 