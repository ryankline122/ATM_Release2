"""
Module to run the command line version of the application
"""
#! /usr/bin/env python3
import RPi.GPIO as GPIO

import sqlite3
import sys
import getpass
import ATM
import ntag2


def main():
    """
    Runs command-line application. Provides user with commands to navigate the application
    :return:
    """
    commands = ["login", "new", "help", "balance",
                "deposit", "withdraw", "transfer", "data", "exit"]
    action = ""
    ATM.createTable()
    db = sqlite3.connect("user_info.db")
    c = db.cursor()

    # RUNS PROGRAM UNTIL USER ENTERS "exit" COMMAND
    while (action != "exit"):
        action = input(
            "Enter a command (Type 'help' for a list of commands): ")


        # CREATE NEW ACCOUNT
        if (action.lower() == "new"):
            if(not ATM.inUse()):
                name = input("Enter your name: ")
                userID = input("Create a unique userID: ")
                if(ATM.userExists(userID)):
                    print("Error - UserID already in use. Try again")
                else:
                    # "Run" --> "Edit Configuration" --> Check "Emulate terminal in output console
                    # Setting Password
                    pswrd = getpass.getpass("Create your password: ", stream=None)
                    confirmPassword = getpass.getpass("Confirm your password: ")
                    while (confirmPassword != pswrd):
                        print("Passwords don't match. Try again")
                        pswrd = getpass.getpass("Create your password: ", stream=None)
                        confirmPassword = getpass.getpass("Confirm your password: ")

                    # Setting PIN
                    PIN = getpass.getpass("Create your 4 digit PIN number: ", stream=None)
                    while (len(PIN) != 4):
                        print("PIN numbers must be 4 digits. Try again")
                        PIN = getpass.getpass("Create your 4 digit PIN number: ", stream=None)
                    confirmPIN = getpass.getpass("Confirm your 4 digit PIN number: ")

                    while (confirmPIN != PIN or len(confirmPIN) > 4):
                        print("PIN numbers don't match. Try again")
                        PIN = getpass.getpass("Create your PIN number: ", stream=None)
                        if(len(PIN) == 4):
                            confirmPIN = getpass.getpass("Confirm your PIN number: ")
                        else:
                            print("Error - PIN must be 4 digits")

                    # Setting Balance
                    try:
                        bal = float(input("Set initial deposit: $"))
                        if ATM.MAX_BALANCE > bal >= 0:
                            ATM.createAccount(name, userID, pswrd, PIN, bal)
                        else:
                            print("Error - Initial deposit must be within $0.00-$999 billion")
                    except ValueError:
                        print("Error - Invalid balance input")
            else:
                print("Error - ATM is currently in use")


        # LOGIN
        elif (action.lower() == "login"):
            if (ATM.inUse()):
                print("Error: In use by another user")
            else:
                cardUID = ntag2.readCard()
                expectedCardNum = ATM.get_key(cardUID)
                print(expectedCardNum)
                pinInput = input("Enter your PIN number:")
                c.execute("SELECT * FROM users where cardNum=? AND PIN=?",
                          (expectedCardNum, pinInput))
                row = c.fetchone()
                if row:
                    ATM.login(expectedCardNum)
                    c.execute("SELECT name FROM users where cardNum =?", (expectedCardNum,))
                    name = ','.join(c.fetchone())
                    print("Welcome " + name + "!")
                else:
                    print("Incorrect card or PIN number")


        # SHOW-BALANCE
        elif (action.lower() == "balance"):
            try:
                print("Balance: " + ("${:,.2f}".format(ATM.currUser.balance)))
            except TypeError:
                print("Error - No user logged in")


        # DEPOSIT
        elif (action.lower() == "deposit"):
            if(ATM.inUse()):
                try:
                    amount = float(input("How much would you like to deposit? $"))
                    if(amount > 0 and (ATM.currUser.balance + amount) < ATM.MAX_BALANCE):
                        ATM.currUser.deposit(amount)
                        print("New Balance: " + ("${:,.2f}".format(ATM.currUser.balance)))
                        ATM.updateBalance()
                    else:
                        print("Error - Balance either exceeds limit or is invalid input")
                except ValueError:
                    print("Error - Invalid Input")
            else:
                print("Error - No user logged in")


        # WITHDRAW
        elif (action.lower() == "withdraw"):
            if(ATM.inUse()):
                try:
                    amount = float(input("How much would you like to withdraw? $"))
                    if(amount <= ATM.currUser.balance):
                        ATM.currUser.withdraw(amount)
                        print("New Balance: " + ("${:,.2f}".format(ATM.currUser.balance)))
                        ATM.updateBalance()
                    else:
                        print("Error - insufficient funds")
                except ValueError:
                    print("Error - Invalid Input")
            else:
                print("Error - No user logged in")


        # TRANSFER
        elif (action.lower() == "transfer"):
            if(ATM.inUse()):
                try:
                    amount = float(input("How much would you like to transfer? $"))
                    if(amount <= ATM.currUser.balance):
                        recipient = input("Enter the recipients' userID: ")
                        if(recipient != ATM.currUser.userID):
                            ATM.currUser.transfer(amount, recipient)
                            print("New Balance: " + ("${:,.2f}".format(ATM.currUser.balance)))
                            ATM.updateBalance()
                        else:
                            print("Error - You are attempting to transfer to yourself")
                    else:
                        print("Error - Insufficient funds")
                except ValueError:
                    print("Error - Invalid Input")
            else:
                print("Error - No user logged in")

        # PRINT DATA
        elif (action.lower() == "data"):
            ATM.printData()

        # HELP
        elif (action.lower() == "help"):
            for i in commands:
                print(i)

        #DELETE ALL
        elif (action.lower() == "nuke"):
            ATM.deleteAll()


        # Forgot Password
        elif (action.lower() == "forgot-password"):
            usernameInput = input("Enter your userID: ")

            if(ATM.userExists(usernameInput)):
                pinInput = input("Enter your PIN number: ")
                newPass = input("Set your new password: ")
                ATM.forgotPassword(usernameInput, pinInput, newPass)
            else:
                print("Incorrect username")


        elif (action.lower() == "read"):
            ntag2.readCard()

        elif (action.lower() == "write"):
            ntag2.write_UID_to_pass(ATM.currUser.userID)


        # LOGOUT
        elif (action.lower() == "logout"):
            if(ATM.inUse()):
                ATM.logout()
                print("Goodbye " + ATM.currUser.name)
            else:
                print("Error - No user logged in")


        # Logs out of all accounts that are currently logged in.
        # For debugging purposes
        elif (action.lower() == "close"):
            ATM.logoutAll()
            print("Success")


        # EXIT
        elif (action.lower() == "exit"):
            if(ATM.inUse()):
                ATM.logout()
                GPIO.cleanup()
                print("Shutting Down")
                sys.exit()
        else:
            print("Invalid command")

        

# ATM Boot-up
print("Welcome to our ATM!")
main()