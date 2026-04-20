from SignIn import *
import json
from Checking import *
import logs

def logging_in():
    # Get user input
    employee_name = input("Please enter your employee name: ")
    password = input("Please enter your password: ")

    # Check credentials and log if successful
    if logs.logs(employee_name, password):
        print("Welcome to the software")
    else:
        print("Login failed. Please try again.")
if __name__ == "__main__":
    logging_in() 