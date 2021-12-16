import password_manager
import os
from tabulate import tabulate
import pyperclip
import getpass

def main():
  __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
  
  if password_manager.is_registered():
    login()
  else:
    register()

  print("\nWelcome!")
  menu()
  print("\nProgram ended!")

def login():
  valid_password = False
  while not valid_password:
    master_password = getpass.getpass("- Insert the master password: ")
    valid_password = password_manager.login(master_password)
    if not valid_password:
      print("Login failed, password not valid, retry")

def register():
  print("Registering an account because no database has been found")
  master_password = getpass.getpass("- Insert the master password of the account that will be generated (YOU MUST REMEMBER THIS): ")
  password_manager.register(master_password)
  
def menu():
  while True:
    print("\n")
    choice = print_menu(["Insert new account", "Get password from account", "List accounts", "Change master password", "Exit"])
    
    if choice == 1:
      portal = input("- Insert the portal: ")
      username = input("- Insert the username of the new account: ")
      password = password_manager.generate_random_password()
      
      password_manager.add_account(portal, username, password)
    
    elif choice == 2:
      portal = input("- Insert the portal: ")
      username = input("- Insert the username of the account to retrieve: ")

      password = password_manager.get_password(portal, username)
      print("")
      if password is None:
        print("An account registered at this portal with this username does not exist!")
      else:
        pyperclip.copy(password)
        print("Password copied in the clipboard!")

    elif choice == 3:
      accounts = password_manager.get_accounts()
      print("\n")
      print(tabulate(accounts, headers=["Portal", "Username"]))

    elif choice == 4:
      current_master_password = getpass.getpass("- Insert the current master password: ")
      new_master_password = getpass.getpass("- Insert the new master password: ")
      print("")

      if(password_manager.change_master_password(current_master_password, new_master_password)):
        print("Master password changed successfully!")
      else:
        print("The current password you inserted is invalid!")

    elif choice == 5:
      break

    print("\n")

def print_menu(options):
  for i in range(len(options)):
    print(str(i + 1) + ") " + options[i])
  
  choice = -1
  while choice < 1 or choice > len(options):
    choice = int(input("- Insert what you want to do: "))
  
  return choice

if __name__ == "__main__":
  main()