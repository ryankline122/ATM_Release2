"""
Module for running the ATM application on the front-end

Functions:
    togglePassword()\n
    transfer()\n
    checkEntryBoxes()\n
    moneyMoves()\n
    dashboard()\n
    logout()\n
    raiseFrame(frame)\n
    getCreationData()\n
    passChangeData()\n
    forgotPassword()\n
"""
import sqlite3
import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox
import ATM



def togglePassword3():
    """
    Allows user to toggle between show/hide password in the input box
    """
    if password2.cget("show") == '*':
        password2.config(show='')
        viewPassBtn3.config(text='Hide Password')
    else:
        password2.config(show='*')
        viewPassBtn3.config(text='Show Password')


def togglePassword2():
    """
    Allows user to toggle between show/hide password in the input box
    """
    if password3.cget("show") == '*':
        password3.config(show='')
        viewPassBtn2.config(text='Hide Password')
    else:
        password3.config(show='*')
        viewPassBtn2.config(text='Show Password')


def togglePassword():
    """
    Allows user to toggle between show/hide password in the input box
    """
    if Password.cget("show") == '*':
        Password.config(show='')
        viewPassBtn.config(text='Hide Password')
    else:
        Password.config(show='*')
        viewPassBtn.config(text='Show Password')


def transfer():
    """
    Takes the input from transfer fields, verifies the information, and calls User transfer method
    if all input it valid
    """
    if ATM.currUser.loginStatus:
        recipient = userNameTransferEntry.get()
        currPin = secPINTransfer.get()
        amount = transferAmountEntry.get()
        pinCheck = ATM.currUser.PIN
    if ((len(transferAmountEntry.get())) != 0 and (len(userNameTransferEntry.get())) != 0 and (len(secPINTransfer.get())) != 0):
        try:
            float(transferAmountEntry.get())
            if ATM.userExists(recipient):
                if recipient != ATM.currUser.userID:
                    if pinCheck == currPin:
                        if (float(transferAmountEntry.get()) >0 and float(transferAmountEntry.get()) <=ATM.currUser.balance):
                            ATM.currUser.transfer(amount, recipient)
                            ATM.updateBalance()
                            displayText.set("${:,.2f}".format(ATM.currUser.balance))
                            raiseFrame(topFrame)
                        else:
                            messagebox.showerror("Error", "Amount must be greater than 0 and cannot be greater than your current balance")
                    else:
                        messagebox.showerror("Error", "PIN was incorrect.")
                else:
                    messagebox.showerror("Error", "Cannot send money to yourself")
            else:
                messagebox.showerror("Error", "UserID does not exist.")
        except ValueError:
            messagebox.showerror("Invalid input for transfer amount",
                             "the transfer amount must be an integer")
    else:
        messagebox.showerror("Error", "message field cannot be left empty")
    userNameTransferEntry.delete(0, END)
    secPINTransfer.delete(0, END)
    transferAmountEntry.delete(0, END)


def checkEntryBoxes():
    """
    Ensures all input boxes have been correctly filled out
    """
    if len(firstName.get()) == 0:
        messagebox.showerror("Invalid input", "You cannot leave \"What is your name?\" empty")
    elif len(userName1.get()) == 0:
        messagebox.showerror("Invalid input", "You cannot leave \"What would you like your username to be?\" empty")
    elif len(password1.get()) == 0:
        messagebox.showerror("Invalid input", "You cannot leave \"What would you like your password to be?\" empty")
    elif len(confirmPasswordEntry.get()) == 0:
        messagebox.showerror("Invalid input", "You cannot leave \"Confirm Password\" empty")
    elif len(secPIN1.get()) == 0:
        messagebox.showerror("Invalid input", "You cannot leave \"Add a PIN number of 4 digits.\" empty")
    elif len(confirmSecPIN1.get()) == 0:
        messagebox.showerror("Invalid input", "You cannot leave \"Confirm PIN\" empty")
    else:
        try:
            float(deposit.get())
            if(float(deposit.get()) < 0 or float(deposit.get()) > ATM.MAX_BALANCE):
                messagebox.showerror("Invalid input for initial deposit",
                                 "Your deposit must be an integer that is >0 and <999999999999")
            else:
                getCreationData()
        except ValueError:
            messagebox.showerror("Invalid input for initial deposit", "Your deposit must be an integer that is >0 and <999999999999")


def moneymoves():
    """
    Handles the deposit/withdraw functionality
    """
    if ATM.currUser.loginStatus:
        money = moneyInput.get()
        balancePreMoneyMove = ATM.currUser.balance
        if myCombo.get() == "Deposit":
            try:
                ATM.currUser.deposit(float(money))
            except ValueError:
                messagebox.showerror("Error", "Make sure that you are: Putting in only integers and that integer is greater than 0 and less than 999999999999")
        else:
            try:
                ATM.currUser.withdraw(float(money))
            except ValueError:
                messagebox.showerror("Error", "Make sure that you are: Putting in only integers and that integer is greater than 0 and not greater than your account balance")

        if balancePreMoneyMove == ATM.currUser.balance:
            moneyInput.delete(0, END)
        else:
            ATM.updateBalance()
            displayText.set("${:,.2f}".format(ATM.currUser.balance))
            moneyInput.delete(0, END)
            raiseFrame(topFrame)


def dashboard():
    """
    Populates the main account screen with accurate user data
    """
    success = False
    Username = User.get()
    Passw = Password.get()
    db = sqlite3.connect('user_info.db')
    c = db.cursor()
    c.execute("SELECT * FROM users where userID=? AND password=?",
              (Username, Passw))
    row = c.fetchone()
    if row:
        success = True

    if success:
        ATM.login(Username, Passw)
        displayText.set("${:,.2f}".format(ATM.currUser.balance))
        User.delete(0, END)
        Password.delete(0, END)
        raiseFrame(topFrame)
    else:
        if len(User.get()) == 0:
            messagebox.showerror("Invalid input", "You cannot leave \"Username\" empty")
        elif len(Password.get()) == 0:
            messagebox.showerror("Invalid input", "You cannot leave \"Password\" empty")
        else:
            myLabel4 = Label(root, text="Incorrect username or password", fg='red', font="Times 12 bold")
            myLabel4.place(x=290, y=300)

def logout():
    """
    Logs out the current user and returns to login page
    """
    ATM.logout()
    raiseFrame(homePage)


def raiseFrame(f):
    """
    Raises the next frame
    """
    f.tkraise()

def getCreationData():
    """
    Collects input from new user registration
    """
    nameEntry = firstName.get()
    userNameEntry = userName1.get()
    pinNum = secPIN1.get()
    passEntry = password1.get()
    depositEntry = deposit.get()
    confirmPinNum = confirmSecPIN1.get()
    confirmPassEntry = confirmPasswordEntry.get()

    if ATM.userExists(userNameEntry):
        userName1.delete(0, END)
        messagebox.showerror("Error", "UserID already exists.")
    else:
        if passEntry == confirmPassEntry:
            if pinNum == confirmPinNum:
                ATM.createAccount(nameEntry, userNameEntry, passEntry, pinNum, depositEntry)
                firstName.delete(0,END)
                userName1.delete(0,END)
                secPIN1.delete(0,END)
                password1.delete(0,END)
                deposit.delete(0,END)
                confirmPasswordEntry.delete(0, END)
                confirmSecPIN1.delete(0, END)
                raiseFrame(homePage)
            else:
                messagebox.showerror("Error", "PINs do not match.")
                confirmSecPIN1.delete(0, END)
                secPIN1.delete(0, END)

        else:
            messagebox.showerror("Error", "Passwords do not match.")
            password1.delete(0, END)
            confirmPasswordEntry.delete(0, END)


def passChangeData():
    """
    Collects data and calls User.changePassword when changing password while logged in
    """
    pinNumIn = secPIN.get()
    newPass = password2.get()

    if (ATM.currUser.PIN == pinNumIn and ATM.currUser.password == currentPassInput.get()):
        if ATM.currUser.password != newPass:
            ATM.currUser.changePassword(newPass)
            raiseFrame(topFrame)
        else:
            messagebox.showerror("Error", "New password cannot be the same as old password")
    else:
        messagebox.showerror("Error", "Incorrect userID or PIN")

    currentPassInput.delete(0, END)
    secPIN.delete(0, END)
    password2.delete(0, END)


def forgotPassword():
    """
    Collects data and calls ATM.forgotPassword when changing password without being logged in
    """
    userNameData = userName3.get()
    pinNumIn = secPIN2.get()
    newPass = password3.get()

    if ATM.userExists(userNameData):
        if ATM.currUser.password != newPass:
            try:
                ATM.forgotPassword(userNameData, pinNumIn, newPass)
                raiseFrame(homePage)
            except ValueError:
                messagebox.showerror("Error", "Could not change password")
        else:
            messagebox.showerror("Error", "New password cannot be the same as old password")
    userName3.delete(0, END)
    secPIN2.delete(0, END)
    password3.delete(0, END)


# GUI ELEMENTS
root = tk.Tk()
root.geometry("800x400")

homePage = Frame(root)
createAccount = Frame(root)
moneyMoves = Frame(root)
passwordChange = Frame(root)
passwordChange2 = Frame(root)
topFrame = Frame(root)
transferFrame = Frame(root)

for frame in (homePage, createAccount, passwordChange, passwordChange2, moneyMoves, topFrame, transferFrame):
    frame.grid(row=0, column=0, sticky='news')

createAccountFrame = LabelFrame(createAccount, width=800, height=400)
createAccountFrame.pack(fill="both", expand=1)

createAccountcanvas = Canvas(createAccountFrame, width=800, height=400, bg='#75706F')
createAccountcanvas.place(x=0, y=0)

nameLabel = Label(createAccountFrame, text="What is your name?",
                          padx=67, pady=15, bg='#343332', fg='white', font="Italics 7")
nameLabel.place(x=20, y=20)
firstName = Entry(createAccountFrame, width=20, fg='black', borderwidth=2)
firstName.place(x=270, y=35)

passwordLabel = Label(createAccountFrame, text="What would you like your password to be?",
                          padx=21, pady=15, bg='#343332', fg='white', font="Italics 7")
passwordLabel.place(x=20, y=90)
password1 = Entry(createAccountFrame, show="*", width=20, fg='black', borderwidth=2)
password1.place(x=270, y=103)

confirmPasswordLabel = Label(createAccountFrame, text="Confirm Password",
                          padx=72, pady=15, bg='#343332', fg='white', font="Italics 7")
confirmPasswordLabel.place(x=20, y=160)
confirmPasswordEntry = Entry(createAccountFrame, show="*", width=20, fg='black', borderwidth=2)
confirmPasswordEntry.place(x=270, y=170)

initialDepositLabel = Label(createAccountFrame, text="What would you like your initial deposit to be?",
                                  padx=15, pady=15, bg='#343332', fg='white', font="Italics 7")
initialDepositLabel.place(x=20, y=230)
deposit = Entry(createAccountFrame, width=20, fg='black', borderwidth=2)
deposit.place(x=270, y=240)

userNameLabel = Label(createAccountFrame, text="What would you like your username to be?",
                          padx=15, pady=15, bg='#343332', fg='white', font="Italics 7")
userNameLabel.place(x=415, y=20)
userName1 = Entry(createAccountFrame, width=20, fg='black', borderwidth=2)
userName1.place(x=645, y=35)

securityPINNLabel = Label(createAccountFrame, text="Add a PIN number of 4 digits.",
                                  padx=42, pady=15, bg='#343332', fg='white', font="Italics 7")
securityPINNLabel.place(x=415, y=90)
secPIN1 = Entry(createAccountFrame, show="*", width=20, fg='black', borderwidth=2)
secPIN1.place(x=645, y=103)

confirmSecurityPINNLabel = Label(createAccountFrame, text="Confirm PIN",
                                  padx=78, pady=15, bg='#343332', fg='white', font="Italics 7")
confirmSecurityPINNLabel.place(x=415, y=160)
confirmSecPIN1 = Entry(createAccountFrame, show="*", width=20, fg='black', borderwidth=2)
confirmSecPIN1.place(x=645, y=170)


updateButton = tk.Button(createAccountFrame, text="Add to database!", padx=60, pady=17, fg="white", bg='#343332' #17
                         , command=lambda:checkEntryBoxes())
updateButton.place(x=500, y=275)

backButton2 = tk.Button(createAccountFrame, text="Back", padx=17, pady=17, fg="white", bg='#343332',
                        command=lambda:raiseFrame(homePage))
backButton2.place(x=30, y=325)


#password change while logged in
passwordChangeLabel = LabelFrame(passwordChange, width=800, height=400)
passwordChangeLabel.pack(fill="both", expand=1)

passwordChangecanvas = Canvas(passwordChangeLabel, width=800, height=400, bg='#75706F')
passwordChangecanvas.place(x=0, y=0)

forgotPasswordLabel = Label(passwordChangeLabel, text="Change Password", bg='#75706F', fg='Black', font= "Times 36 bold underline")
forgotPasswordLabel.place(x=210, y=50)

currentPass = Label(passwordChangeLabel, text="Confirm your current password?",
                          padx=15, pady=15, bg='#343332', fg='white', font="Italics 7")
currentPass.place(x=200, y=135)
currentPassInput = Entry(passwordChangeLabel, show="*", width=25, fg='black', borderwidth=2)
currentPassInput.place(x=400, y=150)

securityPINLabel = Label(passwordChangeLabel, text="Confirm your PIN number",
                                  padx=15, pady=15, bg='#343332', fg='white', font="Italics 7")
securityPINLabel.place(x=235, y=210)
secPIN = Entry(passwordChangeLabel, show="*", width=25, fg='black', borderwidth=2)
secPIN.place(x=400, y=225)

passwordLabel = Label(passwordChangeLabel, text="Set new password",
                          padx=15, pady=15, bg='#343332', fg='white', font="Italics 7")
passwordLabel.place(x=275, y=285)
password2 = Entry(passwordChangeLabel, show="*", width=25, fg='black', borderwidth=2)
password2.place(x=400, y=295)

doneButton = tk.Button(passwordChangeLabel, text="All Done!", padx=17, pady=17, fg="white", bg='#343332',
                       command=lambda:passChangeData())
doneButton.place(x=590, y=330)

backButton3 = tk.Button(passwordChangeLabel, text="Back", padx=17, pady=17, fg="white", bg='#343332',
                        command=lambda:raiseFrame(topFrame)) #CHANGE BACK AFTER DONE TESTING
backButton3.place(x=50, y=330)

viewPassBtn3 = tk.Button(passwordChangeLabel, text="Show Password", width = 15, fg="white", bg='#343332',
                        command=lambda:togglePassword3())
viewPassBtn3.place(x=575, y=293)

#password change used for inside home page
passwordChangeLabel2 = LabelFrame(passwordChange2, width=800, height=400)
passwordChangeLabel2.pack(fill="both", expand=1)

passwordChangecanvas2 = Canvas(passwordChangeLabel2, width=800, height=400, bg='#75706F')
passwordChangecanvas2.place(x=0, y=0)

forgotPassword2 = Label(passwordChangeLabel2, text="Change Password", bg='#75706F', fg='Black', font= "Times 36 bold underline")
forgotPassword2.place(x=210, y=50)

userNameLabel2 = Label(passwordChangeLabel2, text="What is your username?",
                          padx=15, pady=15, bg='#343332', fg='white', font="Italics 7")
userNameLabel2.place(x=250, y=135)
userName3 = Entry(passwordChangeLabel2, width=25, fg='black', borderwidth=2)
userName3.place(x=400, y=150)

securityPINLabel2 = Label(passwordChangeLabel2, text="What is your PIN number?",
                                  padx=15, pady=15, bg='#343332', fg='white', font="Italics 7")
securityPINLabel2.place(x=235, y=210)
secPIN2 = Entry(passwordChangeLabel2, show="*", width=25, fg='black', borderwidth=2)
secPIN2.place(x=400, y=225)

passwordLabel2 = Label(passwordChangeLabel2, text="What would you like your new password to be?",
                          padx=15, pady=15, bg='#343332', fg='white', font="Italics 7")
passwordLabel2.place(x=150, y=285)
password3 = Entry(passwordChangeLabel2, show="*", width=25, fg='black', borderwidth=2)
password3.place(x=400, y=295)

doneButton2 = tk.Button(passwordChangeLabel2, text="All Done!", padx=17, pady=17, fg="white", bg='#343332',
                       command=lambda:forgotPassword())
doneButton2.place(x=590, y=330)

backButton4 = tk.Button(passwordChangeLabel2, text="Back", padx=17, pady=17, fg="white", bg='#343332',
                        command=lambda:raiseFrame(homePage)) #CHANGE BACK AFTER DONE TESTING
backButton4.place(x=50, y=330)

viewPassBtn2 = tk.Button(passwordChangeLabel2, text="Show Password", width = 15, fg="white", bg='#343332',
                        command=lambda:togglePassword2())
viewPassBtn2.place(x=575, y=293)


#topFrame Frame Original Selmir
accountFrame = LabelFrame(topFrame, width=800, height=400)
accountFrame.pack(fill="both", expand=1)

# Define a Canvas Widget
canvasT4 = Canvas(accountFrame, width=800, height=400, bg='#75706F')
canvasT4.place(x=0, y=0)


canvasT2 = Canvas(accountFrame, width=390, height=150, bg='#343332')
canvasT2.place(x=210, y=5)

canvasT3 = Canvas(accountFrame, width=700, height=150, bg='#343332')
canvasT3.place(x=50, y=180)

recentLogLabel = Label(accountFrame, text="Available Features", padx=10, pady=10, bg='#343332', fg='gray',
                           font='Times 10 bold')
recentLogLabel.place(x=335, y=185)


checkingAccountLabel = Label(accountFrame, text="Account Balance", padx=10, pady=10, bg='#343332', fg='gray')
checkingAccountLabel.place(x=220, y=10)

availableBalanceLabel = Label(accountFrame, text="Available Balance", padx=10, pady=10, bg='#343332', fg='gray',
                                  font="Italics 7")
availableBalanceLabel.place(x=215, y=105)

displayText = tk.StringVar()

checkingAccountBalanceLabel = Label(accountFrame, textvariable=displayText, bg='#343332', fg='gray', font="Times 18 bold")
checkingAccountBalanceLabel.place(x=225, y=80)

logoutButton = tk.Button(accountFrame, text="Logout", padx=7, pady=7, fg="white", bg='#343332', command=lambda:logout())
logoutButton.place(x=620, y=240)

moneyMovesButton = tk.Button(accountFrame, text="Deposit/Withdraw Screen", padx=7, pady=7, fg="white", bg='#343332', command=lambda:raiseFrame(moneyMoves))
moneyMovesButton.place(x=120,y=240)

transferButton = tk.Button(accountFrame, text="Transfer Portal", padx=7, pady=7, fg="white", bg='#343332', command=lambda:raiseFrame(transferFrame))
transferButton.place(x=310, y=240)

changePasswordButton = tk.Button(accountFrame, text="Change Password",padx=7, pady=7, fg="white", bg='#343332', command=lambda:raiseFrame(passwordChange))
changePasswordButton.place(x=450, y=240)


#moneyMoves Original Logan Reneau updated by selmir
depoWithFrame = LabelFrame(moneyMoves, width=800, height=400)
depoWithFrame.pack(fill="both", expand=1)

canvasM = Canvas(depoWithFrame, width=800, height=400, bg='#75706F')
canvasM.place(x=0, y=0)

moneyTransfer = Label(depoWithFrame, text="Would you like to deposit or withdraw?",
                          padx=10, pady=10, fg="black", font="Italics 15", bg='#75706F')
moneyTransfer.place(x=225, y=20)

moneyInputLabel = Label(depoWithFrame, text="How much?",
                          padx=10, pady=10, fg="black", font="Italics 15", bg='#75706F')
moneyInputLabel.place(x=325, y=120)

moneyInput = Entry(depoWithFrame, width=23, fg='black', borderwidth=2)
moneyInput.place(x=320, y=175)

doneButton2 = tk.Button(depoWithFrame, text="Submit", padx=17, pady=17, fg="white", bg='#343332',
                        command=lambda:moneymoves())
doneButton2.place(x=600, y=300)

backButton = tk.Button(depoWithFrame, text="Back", padx=17, pady=17, fg="white", bg='#343332',
                        command=lambda:raiseFrame(topFrame))
backButton.place(x=100, y=300)

options = [
    "Deposit",
    "Withdraw"
]

myCombo = ttk.Combobox(depoWithFrame, value=options)
myCombo.current(0)
myCombo.pack(pady=80)


#homePage Frame Original Selmir Lelak, Updated by Logan Reneau
User = Entry(homePage, width=30, fg='black', borderwidth=2)
User.place(x=300, y=175)

Password = Entry(homePage, show="*", width=30, fg='black', borderwidth=2)
Password.place(x=300, y=205)

newUserLabel = Label(homePage, text="New User?", fg='black')
newUserLabel.place(x=660, y=360)

UserNameLabel = Label(homePage, text="Username", font="Italics 12", fg="gray")
UserNameLabel.place(x=215, y=173)

PasswordLabel = Label(homePage, text="Password", font="Italics 12", fg="gray")
PasswordLabel.place(x=215, y=203)

# Buttons
welcomeLabel = Label(homePage, text= "Welcome to the ATM!", font="Italics 36", fg="black")
welcomeLabel.place(x=175, y=50)

viewPassBtn = tk.Button(homePage, text='Show Password', width=15, fg="white", bg='#343332', command=togglePassword)
viewPassBtn.place(x=500, y=200)

loginBtn = tk.Button(homePage, text="Login", padx=25, pady=5, fg="white", bg='#343332', command=lambda:dashboard(),
                    borderwidth=0)
loginBtn.place(x=350, y=235)

createAccBtn = tk.Button(homePage, text="Register", padx=5, pady=5, fg="white", bg='#343332', command=lambda:raiseFrame(createAccount), borderwidth=0)
createAccBtn.place(x=725, y=350)

forgotPasswordButton = tk.Button(homePage, text="Forgot Password?", padx=5, pady=5, fg="white", bg='#343332', command=lambda:raiseFrame(passwordChange2))
forgotPasswordButton.place(x=670,y=305)

#transfer
TransferCanvas = LabelFrame(transferFrame, width=800, height=400)
TransferCanvas.pack(fill="both", expand=1)

greyTransferCanvas = Canvas(TransferCanvas, width=800, height=400, bg='#75706F')
greyTransferCanvas.place(x=0, y=0)

transferLabel = Label(TransferCanvas, text="Transfer Portal", bg='#75706F', fg='Black', font= "Times 36 bold underline")
transferLabel.place(x=210, y=50)

userNameTransferLabel = Label(TransferCanvas, text="What userID to send to?",
                          padx=15, pady=15, bg='#343332', fg='white', font="Italics 7")
userNameTransferLabel.place(x=250, y=135)
userNameTransferEntry = Entry(TransferCanvas, width=25, fg='black', borderwidth=2)
userNameTransferEntry.place(x=400, y=150)

securityPINTransferLabel = Label(TransferCanvas, text="What is your PIN number?",
                                  padx=15, pady=15, bg='#343332', fg='white', font="Italics 7")
securityPINTransferLabel.place(x=235, y=210)
secPINTransfer = Entry(TransferCanvas, show="*", width=25, fg='black', borderwidth=2)
secPINTransfer.place(x=400, y=225)

transferAmountLabel = Label(TransferCanvas, text="How much would you like to send?",
                          padx=15, pady=15, bg='#343332', fg='white', font="Italics 7")
transferAmountLabel.place(x=180, y=285)
transferAmountEntry = Entry(TransferCanvas, width=25, fg='black', borderwidth=2)
transferAmountEntry.place(x=400, y=295)

doneButtonTransfer = tk.Button(TransferCanvas, text="All Done!", padx=17, pady=17, fg="white", bg='#343332',
                       command=lambda:transfer())
doneButtonTransfer.place(x=600, y=300)

backButton3 = tk.Button(TransferCanvas, text="Back", padx=17, pady=17, fg="white", bg='#343332',
                        command=lambda:raiseFrame(topFrame))
backButton3.place(x=50, y=300)

ATM.logoutAll()
raiseFrame(homePage)
root.mainloop()
