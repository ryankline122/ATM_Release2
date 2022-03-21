"""
Module to test functions and methods in ATM.py and User.py
"""
import sqlite3
import unittest
import ATM

# In the terminal:
# "python -m pytest --cov-report=html --cov=(filename) --cov-branch

class TestAccountCreation(unittest.TestCase):

    def testNewAccount(self):
        ATM.createTable()

        db = sqlite3.connect('user_info.db')
        c = db.cursor()
        ATM.createAccount("John", "jdoe123", "passphrase", 1234, 100.99)
        c.execute("SELECT exists(SELECT userID FROM users where userID=?)", ("jdoe123",))
        [exists] = c.fetchone()
        success = exists
        self.assertEqual(True, success)

        ATM.deleteAll()

    def testInUseFalse(self):
        ATM.createTable()
        ATM.createAccount("John", "jdoe123", "passphrase", 1234, 100.99)
        ATM.logout()
        res = ATM.inUse()

        self.assertEqual(False, res)

        ATM.deleteAll()


    def testInUseTrue(self):
        ATM.createTable()
        ATM.createAccount("John", "jdoe123", "passphrase", 1234, 100.99)
        res = ATM.inUse()

        self.assertEqual(True, res)

        ATM.deleteAll()


    def testloginCheckName(self):
        ATM.createTable()

        ATM.createAccount("John", "jdoe123", "passphrase", 1234, 100.99)
        ATM.login("jdoe123", "passphrase")

        self.assertEqual("John", ATM.currUser.name)

        ATM.deleteAll()

    def testLoginCheckUserID(self):
        ATM.createTable()
        ATM.createAccount("John", "jdoe123", "passphrase", 1234, 100.99)

        self.assertEqual("jdoe123", ATM.currUser.userID)
        ATM.deleteAll()


    def testloginCheckPassword(self):
        ATM.createTable()
        ATM.createAccount("John", "jdoe123", "passphrase", 1234, 100.99)

        self.assertEqual("passphrase", ATM.currUser.password)
        ATM.deleteAll()


    def testloginCheckPIN(self):
        ATM.createTable()
        ATM.createAccount("John", "jdoe123", "passphrase", 1234, 100.99)

        self.assertEqual('1234', ATM.currUser.PIN)
        ATM.deleteAll()


    def testLoginCheckBalance(self):
        ATM.createTable()
        ATM.createAccount("John", "jdoe123", "passphrase", 1234, 100.99)

        self.assertEqual(100.99, ATM.currUser.balance)
        ATM.deleteAll()


    def testLoginStatus(self):
        ATM.createTable()
        ATM.createAccount("John", "jdoe123", "passphrase", 1234, 100.99)

        self.assertEqual(True, ATM.currUser.loginStatus)
        ATM.deleteAll()


    def testLogout(self):
        ATM.createTable()

        ATM.createAccount("John", "jdoe123", "passphrase", 1234, 100.99)
        ATM.login("jdoe123", "passphrase")
        ATM.logout()

        self.assertEqual("False", ATM.currUser.loginStatus)


    def testForgotPassword(self):
        ATM.createTable()
        ATM.createAccount("John", "jdoe123", "passphrase", 1234, 100.99)
        ATM.forgotPassword("jdoe123", "1234", "newpassword")

        db = sqlite3.connect('user_info.db')
        c = db.cursor()
        c.execute("SELECT userID FROM users")
        c.execute("SELECT password FROM users where userID=?", ("jdoe123",))
        currPass = ','.join(c.fetchone())

        self.assertEqual("newpassword", currPass)
        ATM.deleteAll()


    def testForgotPasswordIncorrectPIN(self):
        with self.assertRaises(ValueError):
            ATM.createTable()
            ATM.createAccount("John", "jdoe123", "passphrase", 1234, 100.99)
            ATM.forgotPassword("jdoe123", "4567", "newpassword")

            db = sqlite3.connect('user_info.db')
            c = db.cursor()
            c.execute("SELECT userID FROM users")
            c.execute("SELECT password FROM users where userID=?", ("jdoe123",))

        ATM.deleteAll()


    def testUserExistsTrue(self):
        ATM.createTable()
        ATM.createAccount("John", "jdoe123", "passphrase", 1234, 100.99)

        self.assertEqual(True, ATM.userExists("jdoe123"))
        ATM.deleteAll()


    def testUserExistsFalse(self):
        ATM.createTable()
        ATM.createAccount("John", "jdoe123", "passphrase", 1234, 100.99)

        self.assertEqual(False, ATM.userExists("janedoe"))
        ATM.deleteAll()


    def testDeposit(self):
        ATM.createTable()
        ATM.createAccount("John", "jdoe123", "passphrase", 1234, 100.00)
        ATM.currUser.deposit(50.00)

        self.assertEqual(150.0, ATM.currUser.balance)
        ATM.deleteAll()


    def testDepositOverMax(self):
        with self.assertRaises(ValueError):
            ATM.createTable()
            ATM.createAccount("John", "jdoe123", "passphrase", 1234, 100.00)
            ATM.currUser.deposit(1000000000000.00)

        ATM.deleteAll()


    def testDepositUnderMin(self):
        with self.assertRaises(ValueError):
            ATM.createTable()
            ATM.createAccount("John", "jdoe123", "passphrase", 1234, 100.00)
            ATM.currUser.deposit(-1.00)

        ATM.deleteAll()


    def testWithdraw(self):
        ATM.createTable()
        ATM.createAccount("John", "jdoe123", "passphrase", 1234, 100.00)
        ATM.currUser.withdraw(50.0)

        self.assertEqual(50.0, ATM.currUser.balance)
        ATM.deleteAll()


    def testWithdrawTooMuch(self):
        with self.assertRaises(ValueError):
            ATM.createTable()
            ATM.createAccount("John", "jdoe123", "passphrase", 1234, 100.00)
            ATM.currUser.withdraw(150.0)

        ATM.deleteAll()


    def testWithdrawTooLow(self):
        with self.assertRaises(ValueError):
            ATM.createTable()
            ATM.createAccount("John", "jdoe123", "passphrase", 1234, 100.00)
            ATM.currUser.withdraw(-1.0)

        ATM.deleteAll()


    def testTransfer(self):
        ATM.createTable()
        ATM.createAccount("John", "jdoe123", "passphrase", 1234, 100.00)
        ATM.logout()
        ATM.createAccount("Jane", "janedoe123", "password", 1234, 250.00)
        ATM.currUser.transfer(75.0, "jdoe123")
        ATM.logout()
        ATM.login("jdoe123", "passphrase")

        self.assertEqual(175.0, ATM.currUser.balance)
        ATM.deleteAll()


    def testTransferInvalidAmount(self):
        with self.assertRaises(Exception):
            ATM.createTable()
            ATM.createAccount("John", "jdoe123", "passphrase", 1234, 100.00)
            ATM.logout()
            ATM.createAccount("Jane", "janedoe123", "password", 1234, 250.00)
            ATM.currUser.transfer(375.0, "jdoe123")
            ATM.logout()
            ATM.login("jdoe123", "passphrase")

        ATM.deleteAll()


    def testTransferInvalidAmount2(self):
        with self.assertRaises(Exception):
            ATM.createTable()
            ATM.createAccount("John", "jdoe123", "passphrase", 1234, 100.00)
            ATM.logout()
            ATM.createAccount("Jane", "janedoe123", "password", 1234, 250.00)
            ATM.currUser.transfer(-375.0, "jdoe123")
            ATM.logout()
            ATM.login("jdoe123", "passphrase")

        ATM.deleteAll()


    def testTransferRecipientDNE(self):
        with self.assertRaises(Exception):
            ATM.createTable()
            ATM.createAccount("John", "jdoe123", "passphrase", 1234, 100.00)
            ATM.currUser.transfer(15.0, "janedoe123")

        ATM.deleteAll()


    def testPasswordChange(self):
        ATM.createTable()
        ATM.createAccount("John", "jdoe123", "passphrase", 1234, 100.00)
        ATM.currUser.changePassword("newPassword")

        self.assertEqual("newPassword", ATM.currUser.password)


if __name__ == '__main__':
    unittest.main()
