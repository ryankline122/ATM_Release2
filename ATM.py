"""
Module for all backend functionality of the ATM Application.

Functions:
    createTable()\n
    createAccount(string, string, string, string, float, string)\n
    inUse()\n
    login(string, string)\n
    logout()\n
    updateBalance()\n
    forgotPassword(string, string, string)\n
    userExists(string)\n
    printData()\n
    logoutAll()\n
    deleteAll()\n
"""
import sqlite3
from User import User

currUser = User(None, None, None, None, None)
MAX_BALANCE = 999999999999

cards = {
    "admin": "0x10x230x450x67",
    35001: "0x40x130x840xb20x6f0x6f0x81",
    35002: "0x40x270x6c0xb20x6f0x6f0x80",
    35003: "0x40xd60xf20xb20x6f0x6f0x80",
    35004: "0x40x490x6f0xb20x6f0x6f0x81",
}

def get_key(val):
    for key, value in cards.items():
        if val == value:
            return key


def createTable():
    """
    Creates a SQLite database to store user data if one does not already exist
    """
    db = sqlite3.connect('user_info.db')
    c = db.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS users(
                      name text,
                      cardNum integer,
                      PIN text,
                      balance real,
                      loginStatus text
                  )""")
    if(not userExists("Ryan")):
        createAccount("Ryan", 35001, 1234, 1500.0)
    if(not userExists("Logan")):
        createAccount("Logan", 35002, 1234, 1500.0)
    if(not userExists("Selmir")):
        createAccount("Selmir", 35003, 1234, 1500.0)
    if(not userExists("Dr. Nandigam")):
        createAccount("Dr. Nandigam", 35004, 1234, 1500.0)

def createTransactionTable():
    """
    Creates a SQLite table for recent transactions of users
    """
    db = sqlite3.connect('user_info.db')
    c = db.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS transactions(
                        name text,
                        t1 text,
                        t2 text,
                        t3 text
                        )""")
    if (userExists("Ryan")):
        createTransactionLog("Ryan", 0, 0, 0)
    if (userExists("Logan")):
        createTransactionLog("Logan", 0, 0, 0)
    if (userExists("Selmir")):
        createTransactionLog("Selmir", 0, 0, 0)
    if (userExists("Dr. Nandigam")):
        createTransactionLog("Dr. Nandigam", 0, 0, 0)
    db.commit()
    c.close()
    db.close()


def createTransactionLog(name, t1, t2, t3):
    """
    Takes information about users and adds them to the transactions table
    """
    db = sqlite3.connect('user_info.db')
    c = db.cursor()
    c.execute("INSERT INTO transactions VALUES(?,?,?,?)", (name, t1, t2, t3))
    db.commit()
    c.close()
    db.close()


def newTransaction(name, amount):
    """
    Takes in a values from the ATM and adds it to the current users transaction table
    """
    db = sqlite3.connect('user_info.db')
    c = db.cursor()
    c.execute("SELECT t1 FROM transactions WHERE name=?", (name,))
    t1 = c.fetchone()[0]
    c.execute("SELECT t2 FROM transactions WHERE name=?", (name,))
    t2 = c.fetchone()[0]
    c.execute("UPDATE transactions SET t1=? WHERE name=?", (amount, name))
    c.execute("UPDATE transactions SET t2=? WHERE name=?", (t1, name))
    c.execute("UPDATE transactions SET t3=? WHERE name=?", (t2, name))
    db.commit()
    c.close()
    db.close()

def createAccount(name, cardNum, PIN, balance):
    """
    Creates a new entry in the database with the given parameters

        :param name: Name of the user
        :type name: str
        :param userID: The userID to be associated with the user
        :type userID: str
        :param password: The password to be associated with the user
        :type password: str
        :param PIN: A 4-digit number to be associated with the user
        :type PIN: int
        :param balance: Represents the users starting balance
        :type balance: float

    """
    db = sqlite3.connect('user_info.db')
    c = db.cursor()
    usr = User(name, cardNum, PIN, balance, "False")
    c.execute("INSERT INTO users VALUES(?,?,?,?,?)",
              (usr.name, usr.cardNum, usr.PIN, usr.balance, usr.loginStatus))
    db.commit()
    c.close()
    db.close()


def inUse():
    """
    Gives the current use status of the ATM\n
    :return: Boolean
    """
    db = sqlite3.connect('user_info.db')
    c = db.cursor()
    c.execute(
        "SELECT exists(SELECT name FROM users where loginStatus=?)", ("True",))
    [exists] = c.fetchone()
    return exists


def login(cardNum):
    """
    Sets the currUser parameters to the info of the user logging in

    :param userID: The userID of the user logging in
    :type userID: str
    :param password: The password of the user logging in
    :type password: str

    """
    db = sqlite3.connect('user_info.db')
    c = db.cursor()
    c.execute(
        "UPDATE users SET loginStatus = 'True' WHERE cardNum =?", (cardNum,))
    db.commit()
    c.execute("SELECT name FROM users where cardNum =?", (cardNum,))
    name = ','.join(c.fetchone())
    c.execute("SELECT balance FROM users where cardNum =?", (cardNum,))
    balance = c.fetchone()[0]
    c.execute("SELECT PIN FROM users where cardNum =?", (cardNum,))
    PIN = c.fetchone()[0]

    currUser.name = name
    currUser.cardNum = cardNum
    currUser.PIN = PIN
    currUser.balance = balance
    currUser.loginStatus = True

    c.close()
    db.close()


def logout():
    """
    Sets currUser's login status to "False" and calls updateBalance()
    """
    currUser.loginStatus = "False"
    updateBalance()

    db = sqlite3.connect('user_info.db')
    c = db.cursor()
    c.execute("UPDATE users SET loginStatus =? WHERE cardNum=?",
              (currUser.loginStatus, currUser.cardNum,))
    db.commit()
    c.close()
    db.close()


def updateBalance():
    """
     Updates the balance of the current user in the database
    """
    db = sqlite3.connect('user_info.db')
    c = db.cursor()
    c.execute("UPDATE users SET balance =? WHERE cardNum =?", (currUser.balance, currUser.cardNum,))
    db.commit()
    c.close()
    db.close()



# TODO: Change to forgotPIN(name, currPIN, newPIN)
def forgotPassword(userID, PIN, newPassword):
    """
    Allows a user to change their password by confirming their PIN number

    :param userID: The userID of the user wanted to change their password
    :type userID: str
    :param PIN: The PIN number associated with the given userID
    :type PIN: str
    :param newPassword: The user's desired new password
    :type newPassword: str
    """
    db = sqlite3.connect('user_info.db')
    c = db.cursor()
    c.execute("SELECT PIN FROM users WHERE userID=?", (userID,))
    usrPIN = c.fetchone()[0]

    if PIN == usrPIN:
        c.execute("UPDATE users SET password=? WHERE userID=?", (newPassword, userID,))
        db.commit()
    else:
        raise ValueError
    c.close()
    db.close()


def userExists(name):
    """
    Checks if the given userID exists in the database

    :param userID: The userID to search for
    :type userID: str
    :return: Boolean
    """
    db = sqlite3.connect('user_info.db')
    c = db.cursor()
    c.execute("SELECT name FROM users")
    (c.execute("SELECT exists(SELECT name FROM users where name=?)", (name,)))
    [exists] = c.fetchone()

    return exists


# DEBUGGING FUNCTIONS

def printData():
    """
    FOR DEBUGGING: Prints all user data to the console
    """
    db = sqlite3.connect("user_info.db")
    c = db.cursor()
    c.execute("SELECT * FROM users")
    print(c.fetchall())
    c.execute("SELECT * FROM transactions")
    print(c.fetchall())
    c.close()
    db.close()


def logoutAll():
    """
    FOR DEBUGGING: Logs out all users
    """
    db = sqlite3.connect("user_info.db")
    c = db.cursor()
    c.execute("UPDATE users SET loginStatus =? where loginStatus =?", ("False", "True",))
    db.commit()
    c.close()
    db.close()


def deleteAll():
    """
    FOR DEBUGGING: Erases all user data
    """
    db = sqlite3.connect('user_info.db')
    c = db.cursor()
    c.execute('DELETE FROM users')
    db.commit()
    c.close()
    db.close()
