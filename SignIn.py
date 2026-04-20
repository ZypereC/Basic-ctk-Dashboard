import json
import os

def sign_in():
    # Get user input
    employee_name = input("Please enter your employee name: ")
    password = input("Please enter your password: ")

    # Store input in a dictionary
    employee_data = {
        "employee_name": employee_name,
        "password": password
    }

    # File location
    folder = r"C:\Work Software"
    file_path = os.path.join(folder, "employee_data.json")

    # Make sure the folder exists
    os.makedirs(folder, exist_ok=True)

    # Read existing data if file exists, otherwise start with empty list
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            try:
                data_list = json.load(file)
            except json.JSONDecodeError:
                data_list = []
    else:
        data_list = []

    # Append new data
    data_list.append(employee_data)

    # Write updated list back to JSON file
    with open(file_path, "w") as file:
        json.dump(data_list, file, indent=4)

    print("Data saved to JSON file successfully!")

if __name__ == "__main__":
    sign_in() 