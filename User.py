"""
Module to store the User class and its methods

Functions:
    __init__(self, str, str, str, str, str, float, loginStatus)\n
    deposit(self, float)\n
    withdraw(self, float)\n
    transfer(self, float, str)\n
    changePassword(self, str)\n
"""
import sqlite3
import ATM


class User:
    """
    A class to represent a user within the ATM database
    name : str
        Name of the user
    userID : str
        Username associated with the user
    password : str
        Password associated with the user
    PIN : str
        4 digit PIN number associated with the user
    balance : float
        Value that represents the users balance
    loginStatus : str
        Boolean value to store the status of the user
    """

    def __init__(self, name, cardNum, PIN, balance, loginStatus):
        self.name = name
        self.cardNum = cardNum
        self.PIN = PIN
        self.balance = balance
        self.loginStatus = loginStatus

    def deposit(self, amount):
        """
        Adds amount to the users current balance

        :param amount: Amount to be deposited
        :type amount: float
        """
        if float(amount) > 0 and self.balance + float(amount) < ATM.MAX_BALANCE:
            self.balance += float(amount)
        else:
            raise ValueError("Invalid Balance")

    def withdraw(self, amount):
        """
        Subtracts amount from the users current balance

        :param amount: Amount to be withdrawn
        :type amount: float
        """
        if (float(amount) > 0 and float(amount) <= self.balance):
            self.balance -= float(amount)
        else:
            raise ValueError("Insufficient Funds")

    def transfer(self, amount, recipient):
        """
        Transfers funds from this user to another

        :param amount: Amount to be transferred
        :type amount: float
        :param recipient: username of the the recipient
        :type recipient: str
        """
        if (ATM.userExists(recipient) and float(amount) > 0 and float(amount) <= self.balance):
            db = sqlite3.connect('user_info.db')
            c = db.cursor()
            c.execute("SELECT balance FROM users where name=?", (recipient,))
            balance = c.fetchone()[0]
            balance += float(amount)
            c.execute("UPDATE users SET balance =? WHERE name =?", (balance, recipient,))
            db.commit()
            c.close()
            db.close()
            self.withdraw(amount)
        else:
            raise Exception("Recipient does not exist or Invalid Balance")


    # TODO: Change to "changePIN(self, newPIN)"
    def changePassword(self, newPassword):
        """
        Allows user to change their password

        :param newPassword: The desired password for the user
        :type newPassword: str
        """
        self.password = newPassword
        db = sqlite3.connect('user_info.db')
        c = db.cursor()
        c.execute("UPDATE users SET password =? WHERE userID =?", (newPassword, self.userID,))
        db.commit()
        c.close()
        db.close()
