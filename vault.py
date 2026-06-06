# Password Vault: Project 4
import json
import random
import string
import pyperclip
import stdiomask
from argon2 import PasswordHasher

password_hasher = PasswordHasher()

class Credential:
    def __init__(self, application_name, username, password):
        self.application_name = application_name
        self.username = username
        self.password = password
    
    def display_hidden_password(self):
        return "*" * len(self.password)

        
def main():
    # Verifies if user has master access to the password vault
    has_access = master_access()

    if has_access:
        credentials = load_credentials("credentials.json")

        while True:
            menu()

            try:
                user_choice = int(input("Please select an option (1-5): "))
            except ValueError:
                print("Please enter a valid number (1-5)\n")
                continue
            
            if user_choice >= 1 and user_choice <= 5:
                user_action(user_choice, credentials)
                if user_choice == 5:
                    break
            else:
                print("Please enter a valid number (1-5)\n")
                continue

# Determining user action and calling appropriate function
def user_action(user_choice, credentials):
    if user_choice == 1:
        add_credential(credentials)
    elif user_choice == 2:
        view_credentials(credentials)
    elif user_choice == 3:
        search_credentials(credentials)
    elif user_choice == 4:
        generate_password()
    elif user_choice == 5:
        quit_program(credentials)
    else:
        print("Must be a number that is 1-5\n")

def add_credential(credentials):
    app_name = input("\nEnter the name of the application/website: ")
    username = input("Enter the username/email for the account: ")
    password = stdiomask.getpass(prompt="Enter the password for the account: ", mask="*")

    new_credential = Credential(app_name, username, password)
    credentials.append(new_credential)
    print("\nCredential added successfully!\n")
    

def view_credentials(credentials):
    print("\n===STORED CREDENTIALS===\n")

    if not credentials:
        print("No credentials stored yet, please add some first.\n")
        return
    
    for i, credential in enumerate(credentials, start=1):
        print(f"{i}.\nApplication: {credential.application_name}")
        print(f"Username: {credential.username}")
        print(f"Password: {credential.display_hidden_password()}\n")

def search_credentials(credentials):
    has_access = master_access()
    
    if has_access:
        user_search = input("\nSearch for an account by application name: ").strip().lower()
        found_credentials = [cred for cred in credentials if user_search in cred.application_name.lower()]

        if found_credentials:
            print(f"\nFound {len(found_credentials)} credential(s) matching '{user_search}': \n")

            for credential in found_credentials:
                print(f"Application: {credential.application_name}")
                print(f"Username: {credential.username}")
                print(f"Password: {credential.password}\n")

def generate_password():
    while True:
        try:
            length = int(input("\nEnter the length of the random password (minimum 8 characters): "))
            if length < 8:
                print("Please enter a length of at least 8 characters.\n")
                continue
            else:
                break
        except ValueError:
            print("Please enter a valid number for the password length.\n")
            continue
    
    # Setting up a character pool that includes uppercase, lowercase, digits, and punctuation for a strong password
    characters = string.ascii_letters + string.digits + string.punctuation
    
    random_password = "".join(random.choices(characters, k = length))
    print(f"\nGenerated random password: {random_password}\n")
    
    pyperclip.copy(random_password)
    print("We've automatically copied the generated password to your clipboard!\n")
    

def quit_program(credentials):
    save_credentials("credentials.json", credentials)
    print("\nSaving credentials and exiting program...\n")
    return

def load_credentials(file_name):
    try:
        with open(file_name, "r") as file:
            credentials_data = json.load(file)
            credentials = [Credential(**credential) for credential in credentials_data]
            return credentials
    except(json.JSONDecodeError, FileNotFoundError):
        return []

def save_credentials(file_name, credentials):
    try:
        with open(file_name, "w") as file:
            credentials_data = [credential.__dict__ for credential in credentials]
            json.dump(credentials_data, file, indent=4)
    except IOError:
        print("Error saving credentials to file.\n")


def master_access():
    print("\n===PERSONAL PASSWORD VAULT===\n")

    # Attempting to load master password hash from file
    master_password_hash = load_master("master_password.json")

    # If it doesn't exist, prompt user to create one
    if not master_password_hash:
        print("Please create a master password to secure your vault.\n")
        while True:
            new_master_password = input("Enter your new master password: ")
            confirm_password = input("Confirm your new master password: ")

            if new_master_password == confirm_password:
                hashed_password = password_hasher.hash(new_master_password)

                with open("master_password.json", "w") as file:
                    json.dump(hashed_password, file)
                    print("Master password set successfully.\n")
                    return True
            else:
                print("Passwords do not match. Please try again.\n")

    # If it does exist, prompt user to enter master password and verify
    attempts = 3
    print("**You have 3 attempts to enter the correct master password**\n")
    for attempt in range(attempts):
        master_password = input("Enter the master password: ")
        valid = check_valid(master_password)

        if valid:
            print("\nAccess granted.\n")
            return True
        else:
            print(f"Incorrect password. {attempts - attempt - 1} attempt(s) remaining.\n")
    
    print("Access denied. Too many incorrect attempts.")
    return False

def load_master(file_name):
    try:
        with open(file_name, "r") as file:
            data = json.load(file)
            return data
    except(json.JSONDecodeError, FileNotFoundError):
        return []

def check_valid(user_attempt):
    try:
        master_password_hash = load_master("master_password.json")
        password_hasher.verify(master_password_hash, user_attempt)
        return True
    except ValueError:
        return False

def menu():
    print("\n===PASSWORD VAULT===\n")

    print("1. Add Credential")
    print("2. View Stored Credentials")
    print("3. Search Accounts")
    print("4. Generate Random Password")
    print("5. Save & Exit")

if __name__ == "__main__":
    main()

