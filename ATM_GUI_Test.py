from tkinter import *

import tkinter as tk
from tkinter import font as tkfont
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
# import ntag2
import ATM


from multiprocessing import Pool
import sys
import time

# class that controls frame switching


class Controller(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(
            family='Helvetica', size=18, weight="bold", slant="italic")

        self.displayText = tk.StringVar()
        # self.displayText.set("${:,.2f}".format(ATM.currUser.balance)) change to be set right after login

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, WelcomePage, LoginPage, Dashboard,
                  moneyMoves, DepositFrame, WithdrawFrame, TransferFrame,
                  TransactionsFrame, PINChangeFrame1, PINChangeFrame2):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        # Show a frame for the given page name
        frame = self.frames[page_name]
        frame.tkraise()

    def login(self):
        cardUID = "0x40x130x840xb20x6f0x6f0x81"  # change to ntag2.readCard()
        expectedCardNum = ATM.get_key(cardUID)
        ATM.login(expectedCardNum)
        self.displayText.set("${:,.2f}".format(ATM.currUser.balance))


# startPage with activate scanner button
class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        f1_frame = LabelFrame(self, width=800, height=480)
        f1_frame.pack(fill="both", expand=1)

        f1_canvas = Canvas(f1_frame, width=800, height=480, bg="white")
        f1_canvas.place(x=0, y=0)

        main_label = Label(self, text="Lakers Credit Union",
                           bg='#FEFEFE', font=("Arial Bold", 25))
        main_label.place(x=250, y=20)

        login_button = tk.Button(self, text="Login", padx=70, pady=25, font=("Arial Bold", 10),
                                 command=lambda: [controller.show_frame("LoginPage"), LoginPage.loop(self, 0)])
        login_button.place(x=320, y=170)

        exit_button = tk.Button(self, text="Exit", padx=75, pady=25, font=("Arial Bold", 10),
                                command=lambda: powerOff())
        exit_button.place(x=320, y=290)

        def powerOff():
            # GPIO.cleanup()
            print("Shutting Down")
            sys.exit()


class WelcomePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        f3_frame = LabelFrame(self, width=800, height=480)
        f3_frame.pack(fill="both", expand=1)

        f3_canvas = Canvas(f3_frame, width=800, height=480, bg="white")
        f3_canvas.place(x=0, y=0)

        def togglePassword():
            """
            Allows user to toggle between show/hide password in the input box
            """
            if password.cget("show") == '*':
                password.config(show='')
                viewPassBtn.config(text='Hide Password')
            else:
                password.config(show='*')
                viewPassBtn.config(text='Show Password')

        Secondary_label = Label(self, text="Please Enter Your PIN",
                                bg='#FEFEFE', font=("Arial Bold", 15))
        Secondary_label.place(x=295, y=145)

        viewPassBtn = tk.Button(self, text="Show Password", padx=25, pady=15, fg="white", bg='#343332', font=("Arial Bold", 10),
                                command=lambda: togglePassword())
        viewPassBtn.place(x=325, y=250)

        password = Entry(self, show="*", width=20, fg='black',
                         font=('Arial 15'), borderwidth=2)
        password.place(x=290, y=205)

        backButton = tk.Button(self, text="Cancel", padx=50, pady=30, font=("Arial Bold", 10),
                               command=lambda: controller.show_frame("StartPage"))
        backButton.place(x=30, y=380)

        nextButton = tk.Button(self, text="Next", padx=55, pady=30, font=("Arial Bold", 10),
                               command=lambda: checkPIN())
        nextButton.place(x=620, y=380)

        def checkPIN():
            input = password.get()
            if(input == ATM.currUser.PIN):
                controller.show_frame("Dashboard")
            else:
                messagebox.showerror("Input Error", "Incorrect PIN")
            password.delete(0, END)

# unfinished, just using to test old code with new class implementation


class Dashboard(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        f4_frame = LabelFrame(self, width=800, height=480)
        f4_frame.pack(fill="both", expand=1)

        f4_canvas = Canvas(self, width=800, height=480, bg="white")
        f4_canvas.place(x=0, y=0)

        balanceLabel = Label(
            self, text="Account Balance", padx=10, pady=10, bg="white", font=("Arial Bold", 25))
        balanceLabel.place(x=275, y=10)

        checkingAccountBalanceLabel = Label(
            self, textvariable=controller.displayText, bg="white", font=("Arial Bold", 20))
        checkingAccountBalanceLabel.place(x=350, y=80)

        recentLogLabel = Label(self, text="Actions:",
                               padx=10, pady=10, bg="white", font=("Arial Bold", 15))
        recentLogLabel.place(x=365, y=185)

        # Action Buttons
        depositWithdraw_button = tk.Button(
            self, text="Deposit/Withdraw", padx=65, pady=18, fg="white", bg='#343332', font=("Arial Bold", 10),
            command=lambda: controller.show_frame("moneyMoves"))
        depositWithdraw_button.place(x=100, y=250)

        transfer_button = tk.Button(
            self, text="Transfer To Another User", padx=40, pady=18, fg="white", bg='#343332', font=("Arial Bold", 10),
            command=lambda: controller.show_frame("TransferFrame"))
        transfer_button.place(x=100, y=350)

        transfer_button = tk.Button(
            self, text="Recent Transactions", padx=45, pady=18, fg="white", bg='#343332', font=("Arial Bold", 10),
            command=lambda: controller.show_frame("TransactionsFrame"))
        transfer_button.place(x=475, y=250)

        PIN_button = tk.Button(
            self, text="Change PIN", padx=71, pady=18, fg="white", bg='#343332', font=("Arial Bold", 10),
            command=lambda: controller.show_frame("PINChangeFrame1"))
        PIN_button.place(x=475, y=350)

        logoutButton = tk.Button(self, text="Logout", padx=10, pady=10, font=("Arial Bold", 10),
                                 command=lambda: [controller.show_frame("StartPage"), ATM.logoutAll()])
        logoutButton.place(x=30, y=10)


class LoginPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        f1_canvas = Canvas(self, width=800, height=480, bg="white")
        f1_canvas.place(x=0, y=0)

        main_label = Label(self, text="Please Scan Your Card",
                           bg='#FEFEFE', font=("Arial Bold", 25))
        main_label.place(x=220, y=20)

    def loop(self, dots):  # waiting animation
        Secondary_label = Label(root.frames["LoginPage"], text="Waiting",
                                bg='#FEFEFE', font=("Arial Bold", 15))
        Secondary_label.place(x=325, y=200)

        while dots < 1:
            Secondary_label.config(
                text="Waiting" + "." * (dots % 3 + 1), bg='#FEFEFE', font=("Arial Bold", 25))
            dots += 1
            root.update()
            time.sleep(0.5)
        self.controller.login()
        root.show_frame("WelcomePage")

        Welcome_name_label = Label(root.frames["WelcomePage"], text="Hello " + ATM.currUser.name,
                                   bg='#FEFEFE', font=("Arial Bold", 25))
        Welcome_name_label.place(x=300, y=20)
        print(ATM.currUser.name)


class moneyMoves(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        money_frame = LabelFrame(self, width=800, height=480)
        money_frame.pack(fill="both", expand=1)

        money_canvas = Canvas(self, width=800, height=480, bg="white")
        money_canvas.place(x=0, y=0)

        balanceLabel = Label(
            self, text="Available Balance", padx=10, pady=10, bg="white", font=("Arial Bold", 25))
        balanceLabel.place(x=260, y=10)

        checkingAccountBalanceLabel = Label(
            self, textvariable=controller.displayText, bg="white", font=("Arial Bold", 20))
        checkingAccountBalanceLabel.place(x=340, y=80)

        moneyTransfer = Label(self, text="Select A Transfer Option:",
                              padx=10, pady=10, bg="white", font=("Arial Bold", 15))
        moneyTransfer.place(x=280, y=175)

        deposit_button = tk.Button(
            self, text="Deposit", padx=70, pady=18, fg="white", bg='#343332', font=("Arial Bold", 10),
            command=lambda: controller.show_frame("DepositFrame"))
        deposit_button.place(x=150, y=300)

        withdraw_button = tk.Button(
            self, text="Withdraw", padx=60, pady=18, fg="white", bg='#343332', font=("Arial Bold", 10),
            command=lambda: controller.show_frame("WithdrawFrame"))
        withdraw_button.place(x=475, y=300)

        backButton = tk.Button(self, text="Cancel", padx=10, pady=10, font=("Arial Bold", 10),
                               command=lambda: [controller.show_frame("Dashboard")])
        backButton.place(x=30, y=10)


class DepositFrame(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        deposit_frame = LabelFrame(self, width=800, height=480)
        deposit_frame.pack(fill="both", expand=1)

        deposit_canvas = Canvas(self, width=800, height=480, bg="white")
        deposit_canvas.place(x=0, y=0)

        balanceLabel = Label(
            self, text="Available Balance", padx=10, pady=10, bg="white", font=("Arial Bold", 25))
        balanceLabel.place(x=260, y=10)

        checkingAccountBalanceLabel = Label(
            self, textvariable=controller.displayText, bg="white", font=("Arial Bold", 20))
        checkingAccountBalanceLabel.place(x=340, y=80)

        moneyTransfer = Label(self, text="Amount to Deposit:",
                              padx=10, pady=10, bg="white", font=("Arial Bold", 15))
        moneyTransfer.place(x=300, y=175)

        amount_entry = Entry(self, width=20, fg='black',
                             font=('Arial 15'), borderwidth=2)
        amount_entry.place(x=290, y=240)

        submit_button = tk.Button(
            self, text="Confirm", padx=60, pady=18, fg="white", bg='#343332', font=("Arial Bold", 10),
            command=lambda: deposit())
        submit_button.place(x=310, y=300)

        backButton = tk.Button(self, text="Cancel", padx=10, pady=10, font=("Arial Bold", 10),
                               command=lambda: [controller.show_frame("Dashboard")])
        backButton.place(x=30, y=10)

        def deposit():
            """
             Handles the deposit/withdraw functionality
            """
            money = amount_entry.get()
            try:
                ATM.currUser.deposit(float(money))
                update_p2_label(self)
                ATM.updateBalance()
                controller.show_frame("Dashboard")
            except ValueError:
                messagebox.showerror("Error",
                                     "Invalid Input")
            amount_entry.delete(0, END)

        def update_p2_label(self):
            self.controller.displayText.set(
                "${:,.2f}".format(ATM.currUser.balance))


class WithdrawFrame(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        withdraw_frame = LabelFrame(self, width=800, height=480)
        withdraw_frame.pack(fill="both", expand=1)

        withdraw_canvas = Canvas(self, width=800, height=480, bg="white")
        withdraw_canvas.place(x=0, y=0)

        balanceLabel = Label(
            self, text="Available Balance", padx=10, pady=10, bg="white", font=("Arial Bold", 25))
        balanceLabel.place(x=260, y=10)

        checkingAccountBalanceLabel = Label(
            self, textvariable=controller.displayText, bg="white", font=("Arial Bold", 20))
        checkingAccountBalanceLabel.place(x=340, y=80)

        moneyTransfer = Label(self, text="Amount to Withdraw:",
                              padx=10, pady=10, bg="white", font=("Arial Bold", 15))
        moneyTransfer.place(x=290, y=175)

        amount_entry = Entry(self, width=20, fg='black',
                             font=('Arial 15'), borderwidth=2)
        amount_entry.place(x=290, y=240)

        submit_button = tk.Button(
            self, text="Confirm", padx=60, pady=18, fg="white", bg='#343332', font=("Arial Bold", 10),
            command=lambda: withdraw())
        submit_button.place(x=310, y=300)

        backButton = tk.Button(self, text="Cancel", padx=10, pady=10, font=("Arial Bold", 10),
                               command=lambda: [controller.show_frame("Dashboard")])
        backButton.place(x=30, y=10)

        def withdraw():
            """
             Handles the deposit/withdraw functionality
            """
            money = amount_entry.get()
            try:
                ATM.currUser.withdraw(float(money))
                update_p2_label(self)
                ATM.updateBalance()
                controller.show_frame("Dashboard")
            except ValueError:
                messagebox.showerror("Error",
                                     "Invalid Input")
            amount_entry.delete(0, END)

        def update_p2_label(self):
            self.controller.displayText.set(
                "${:,.2f}".format(ATM.currUser.balance))


class TransferFrame(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        transfer_frame = LabelFrame(self, width=800, height=480)
        transfer_frame.pack(fill="both", expand=1)

        transfer_canvas = Canvas(self, width=800, height=480, bg="white")
        transfer_canvas.place(x=0, y=0)

        balanceLabel = Label(
            self, text="Available Balance", padx=10, pady=10, bg="white", font=("Arial Bold", 25))
        balanceLabel.place(x=260, y=10)

        checkingAccountBalanceLabel = Label(
            self, textvariable=controller.displayText, bg="white", font=("Arial Bold", 20))
        checkingAccountBalanceLabel.place(x=340, y=80)

        moneyTransfer = Label(self, text="Account Number of Recipient:",
                              padx=10, pady=10, bg="white", font=("Arial Bold", 15))
        moneyTransfer.place(x=270, y=150)

        # Entry Fields
        accountNum_entry = Entry(
            self, width=20, fg='black', font=('Arial 15'), borderwidth=2)
        amount_entry = Entry(self, width=20, fg='black',
                             font=('Arial 15'), borderwidth=2)
        accountNum_entry.place(x=290, y=200)
        amount_entry.place(x=290, y=300)

        moneyTransfer = Label(self, text="Amount to be Transferred:",
                              padx=10, pady=10, bg="white", font=("Arial Bold", 15))
        moneyTransfer.place(x=270, y=250)

        submit_button = tk.Button(
            self, text="Confirm", padx=60, pady=18, fg="white", bg='#343332', font=("Arial Bold", 10),
            command=lambda: transfer())
        submit_button.place(x=310, y=390)

        backButton = tk.Button(self, text="Cancel", padx=10, pady=10, font=("Arial Bold", 10),
                               command=lambda: [controller.show_frame("Dashboard")])
        backButton.place(x=30, y=10)

        def transfer():
            """
             Handles the deposit/withdraw functionality
            """
            recipient = accountNum_entry.get()
            money = amount_entry.get()
            try:
                if(str(recipient) != str(ATM.currUser.cardNum)):
                    ATM.currUser.transfer(money, recipient)
                    update_p2_label(self)
                    ATM.updateBalance()
                    controller.show_frame("Dashboard")
                else:
                    messagebox.showerror("Error",
                                         "Cannot Transfer to yourself")
            except ValueError:
                messagebox.showerror("Error",
                                     "Invalid Input")
            except Exception:
                accountNum_entry.delete(0, END)
                messagebox.showerror("Error", "Invalid Account Number")
            amount_entry.delete(0, END)
            accountNum_entry.delete(0, END)

        def update_p2_label(self):
            self.controller.displayText.set(
                "${:,.2f}".format(ATM.currUser.balance))


class TransactionsFrame(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        transaction_frame = LabelFrame(self, width=800, height=480)
        transaction_frame.pack(fill="both", expand=1)

        transaction_canvas = Canvas(self, width=800, height=480, bg="white")
        transaction_canvas.place(x=0, y=0)

        header_label = Label(
            self, text="Recent Transactions", padx=10, pady=10, bg="white", font=("Arial Bold", 25))
        header_label.place(x=245, y=10)

        heading1_label = Label(
            self, text="Amount:", padx=10, pady=10, bg="white", font=("Arial Bold", 10)
        )
        heading1_label.place(x=250, y=100)

        heading2_label = Label(
            self, text="Initiated By:", padx=10, pady=10, bg="white", font=("Arial Bold", 10)
        )
        heading2_label.place(x=450, y=100)

        # Transaction Labels
        t1_amount_label = Label(
            self, text="--", padx=10, pady=10, bg="white", font=("Arial Bold", 10)
        )
        t1_amount_label.place(x=250, y=150)

        t1_User_label = Label(
            self, text="--", padx=10, pady=10, bg="white", font=("Arial Bold", 10)
        )
        t1_User_label.place(x=450, y=150)

        t2_amount_label = Label(
            self, text="--", padx=10, pady=10, bg="white", font=("Arial Bold", 10)
        )
        t2_amount_label.place(x=250, y=200)

        t2_User_label = Label(
            self, text="--", padx=10, pady=10, bg="white", font=("Arial Bold", 10)
        )
        t2_User_label.place(x=450, y=200)

        t3_amount_label = Label(
            self, text="--", padx=10, pady=10, bg="white", font=("Arial Bold", 10)
        )
        t3_amount_label.place(x=250, y=250)

        t3_User_label = Label(
            self, text="--", padx=10, pady=10, bg="white", font=("Arial Bold", 10)
        )
        t3_User_label.place(x=450, y=250)

        submit_button = tk.Button(
            self, text="OK", padx=60, pady=18, fg="white", bg='#343332', font=("Arial Bold", 10),
            command=lambda: controller.show_frame("Dashboard"))
        submit_button.place(x=340, y=390)


class PINChangeFrame1(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        PIN_frame = LabelFrame(self, width=800, height=480)
        PIN_frame.pack(fill="both", expand=1)

        PIN_canvas = Canvas(self, width=800, height=480, bg="white")
        PIN_canvas.place(x=0, y=0)

        Secondary_label = Label(self, text="Enter Current PIN",
                                bg='#FEFEFE', font=("Arial Bold", 15))
        Secondary_label.place(x=295, y=145)

        viewPassBtn = tk.Button(self, text="Show", padx=25, pady=15, fg="white", bg='#343332', font=("Arial Bold", 10),
                                command=lambda: togglePassword())
        viewPassBtn.place(x=575, y=180)

        password = Entry(self, show="*", width=20, fg='black',
                         font=('Arial 15'), borderwidth=2)
        password.place(x=290, y=205)

        nextButton = tk.Button(self, text="Next", padx=55, pady=30, font=("Arial Bold", 10),
                               command=lambda: checkPIN())
        nextButton.place(x=315, y=380)

        # TODO: fix show_frame button
        backButton = tk.Button(self, text="Cancel", padx=10, pady=10, font=("Arial Bold", 10),
                               command=lambda: [controller.show_frame("Dashboard")])
        backButton.place(x=30, y=10)

        def togglePassword():
            """
            Allows user to toggle between show/hide password in the input box
            """
            if password.cget("show") == '*':
                password.config(show='')
                viewPassBtn.config(text='Hide')
            else:
                password.config(show='*')
                viewPassBtn.config(text='Show')

        def checkPIN():
            input = password.get()
            if(input == ATM.currUser.PIN):
                controller.show_frame("PINChangeFrame2")
            else:
                messagebox.showerror("Input Error", "Incorrect PIN")
            password.delete(0, END)


class PINChangeFrame2(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        PIN_frame = LabelFrame(self, width=800, height=480)
        PIN_frame.pack(fill="both", expand=1)

        PIN_canvas = Canvas(self, width=800, height=480, bg="white")
        PIN_canvas.place(x=0, y=0)

        Secondary_label = Label(self, text="Enter New PIN",
                                bg='#FEFEFE', font=("Arial Bold", 15))
        Secondary_label.place(x=295, y=100)

        newPIN_1 = Entry(self, show="*", width=20, fg='black',
                         font=('Arial 15'), borderwidth=2)
        newPIN_1.place(x=290, y=150)

        confirm_label = Label(self, text="Confirm Your New PIN",
                              bg='#FEFEFE', font=("Arial Bold", 15))
        confirm_label.place(x=295, y=200)

        newPIN_2 = Entry(self, show="*", width=20, fg='black',
                         font=('Arial 15'), borderwidth=2)
        newPIN_2.place(x=290, y=250)

        viewPassBtn = tk.Button(self, text="Show", padx=25, pady=15, fg="white", bg='#343332', font=("Arial Bold", 10),
                                command=lambda: togglePassword())
        viewPassBtn.place(x=575, y=180)

        nextButton = tk.Button(self, text="Done", padx=55, pady=30, font=("Arial Bold", 10),
                               command=lambda: checkPIN())
        nextButton.place(x=315, y=380)

        backButton = tk.Button(self, text="Cancel", padx=10, pady=10, font=("Arial Bold", 10),
                               command=lambda: [controller.show_frame("Dashboard")])
        backButton.place(x=30, y=10)

        def togglePassword():
            """
            Allows user to toggle between show/hide password in the input box
            """
            if newPIN_1.cget("show") == '*':
                newPIN_1.config(show='')
                newPIN_2.config(show='')
                viewPassBtn.config(text='Hide PIN')
            else:
                newPIN_1.config(show='*')
                newPIN_2.config(show='*')
                viewPassBtn.config(text='Show PIN')

        def checkPIN():
            PIN_1 = newPIN_1.get()
            PIN_2 = newPIN_2.get()
            if(PIN_1 == ATM.currUser.PIN):
                messagebox.showerror(
                    "Input Error", "New PIN is the same as the current PIN")
            elif(PIN_1 != PIN_2):
                messagebox.showerror("Input Error", "PINs don't match")
            elif(len(PIN_1) > 10):
                messagebox.showerror(
                    "Input Error", "New PIN is too long. 9 digit max")
            else:
                ATM.currUser.changePassword(PIN_1)
                messagebox.showinfo("Success", "PIN has been updated")
                controller.show_frame("Dashboard")
            newPIN_1.delete(0, END)
            newPIN_2.delete(0, END)


if __name__ == "__main__":
    root = Controller()
    root.mainloop()
