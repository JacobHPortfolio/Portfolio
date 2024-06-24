import json
from cryptography.fernet import Fernet

#generates key file using fernet in cryptography
def keyFileGenerator(filename):
    key = Fernet.generate_key()
    with open(filename, 'wb') as file:
        file.write(key)

#Opens key.key to get key written in plain text            
def getKey(filename):
    try:
        with open(filename, 'rb') as file:
            return file.read()
    except FileNotFoundError:
        print("Please insert key file in folder")
        return None

#encrypts passwords using fernet in cryptography            
def encryptPasswords(data, key):
    fernet = Fernet(key)
    encryptedData = fernet.encrypt(data.encode())
    return encryptedData

#encrypts passwords using fernet in cryptography 
def decryptPassword(data, key):
    fernet = Fernet(key)
    decryptedData = fernet.decrypt(data).decode()
    return decryptedData

#adds password to password dictionary    
def addPassword(passwords, service, username, password):
    passwords[service] = {'username': username, 'password': password}

#gets passwords from the file and decrypt them using fernet and json
def getPasswords(filename, key):
    try:
        with open(filename, 'rb') as file:
            data = decryptPassword(file.read(), key)
            return json.loads(data)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

#saves and encrypts passwords to password.dat using json         
def savePasswords(filename, passwords, key):
    with open(filename, 'wb') as file:
        file.write(encryptPasswords(json.dumps(passwords), key))




def main():
    passwordFile = 'passwords.dat'
    keyFile = 'key.key'
    
    # Loop to ensure key file is present or create a new one if needed
    while True:
        key = getKey(keyFile)
        if key is not None:
            break
        else:
            create_new_key = input("Key file not found. Would you like to create a new one? (yes/no): ")
            if create_new_key.lower() == 'yes':
                keyFileGenerator(keyFile)
                print("New key file created, please run the program again.")
                return
            else:
                print("Please add the key file to the folder and run the program again.")
                return

    passwords = getPasswords(passwordFile, key)
    
     # Menu loop for the password manager
    while True:
        print("\nPassword Manager Menu:")
        print("1. Add/Change a password")
        print("2. Look up a password")
        print("3. Delete a password")
        print("4. All stored services")
        print("5. Exit")
        choice = input("Enter your choice: ")
        
        if choice == '1':
            service = input("Enter the service name: ")
            username = input("Enter the service username: ")
            password = input("Enter the password: ")
            addPassword(passwords, service, username, password)
            savePasswords(passwordFile, passwords, key)
            print("Password saved.")
        elif choice == '2':
            service = input("Enter service name: ")
            if service in passwords:
                foundUsername = passwords[service]['username']
                foundPassword = passwords[service]['password']
                print(foundUsername)
                print(foundPassword)
            else:
                print("Service not found.")
        elif choice == '3':
            service = input("Enter service name: ")
            if service in passwords:
                del passwords[service]
                print(f"Password for {service} deleted successfully.")
            else:
                print("Service not found")
        elif choice == '4':
            for service in passwords:
                print(service)
        elif choice == '5':
            print("Exiting password manager. Please store key.key on a safe external flash drive.")
            break
        else:
            print("invalid input, please try again.")

    
if __name__ == "__main__":
    main()
    
