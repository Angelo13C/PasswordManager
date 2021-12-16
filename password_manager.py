from database import Database
import master_password
import string
import secrets

database = Database()
database.execute("""CREATE TABLE IF NOT EXISTS Account(
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Portal TEXT NOT NULL,
    Username TEXT NOT NULL,
    Password TEXT NOT NULL
    );""")

def is_registered():
    return master_password.exists()

def login(password):
    return master_password.verify(password)

def register(password):
    if is_registered():
        return False

    master_password.change(password)
    return True

def add_account(portal, username, password):
    encrypt_password = master_password.encrypt(password)
    
    database.execute("""INSERT INTO Account (Portal, Username, Password)
    VALUES (?, ?, ?);""", (portal, username, encrypt_password))

def get_password(portal, username):
    account = database.execute("""SELECT Password FROM Account WHERE
    Portal = ? AND Username = ?;""", (portal, username))
    if not account:
        return None
    
    password_field = account[0][0]
    password = master_password.decrypt(password_field)
    return password

def get_accounts():
    accounts = database.execute("""SELECT Portal, Username FROM Account;""")
    return accounts

def change_master_password(current_password, new_password):
    #If the current master password is valid, update the master password
    if master_password.verify(current_password):
        
        #Update current password stored with the new key
        fields = database.execute("""SELECT ID, Password FROM Account;""")
        passwords = [None] * len(fields)
        for i in range(len(fields)):
            passwords[i] = master_password.decrypt(fields[i][1])

        master_password.change(new_password)

        for i in range(len(passwords)):
            encrypted_password = master_password.encrypt(passwords[i])
            id = fields[i][0]
            database.execute("""UPDATE Account SET Password = ? WHERE ID = ?""", (encrypted_password, id))

        return True
    
    return False

def generate_random_password(lowercase_count = 3, uppercase_count = 3, digits_count = 4, symbols_count = 2):
    SYMBOLS = "@#$%&"
    CHARACTERS = string.ascii_letters + string.digits + SYMBOLS
    
    password_length = lowercase_count + uppercase_count + digits_count + symbols_count
    while True:
        password = ''.join(secrets.choice(CHARACTERS) for i in range(password_length))
        if (sum(c.islower() for c in password) >= lowercase_count
                and sum(c.isupper() for c in password) >= uppercase_count
                and sum(c.isdigit() for c in password) >= digits_count
                and sum(c in SYMBOLS for c in password) >= symbols_count):
            break
    return password