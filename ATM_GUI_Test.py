from tkinter import *

import tkinter as tk
from tkinter import font as tkfont
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
#import ntag2
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
        for F in (StartPage, WelcomePage, LoginPage, Dashboard, moneyMoves, DepositFrame, WithdrawFrame):
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
            self, text="Transfer To Another User", padx=40, pady=18, fg="white", bg='#343332', font=("Arial Bold", 10))
        transfer_button.place(x=100, y=350)

        transfer_button = tk.Button(
            self, text="Recent Transactions", padx=45, pady=18, fg="white", bg='#343332', font=("Arial Bold", 10))
        transfer_button.place(x=475, y=250)

        PIN_button = tk.Button(
            self, text="Change PIN", padx=71, pady=18, fg="white", bg='#343332', font=("Arial Bold", 10))
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

        amount_entry = Entry(self, width=20, fg='black', text="$",
                             font=('Arial 15'), borderwidth=2)
        amount_entry.place(x=290, y=220)

        cancel_button = tk.Button(
            self, text="Confirm", padx=60, pady=18, fg="white", bg='#343332', font=("Arial Bold", 10),
            command=lambda: deposit())
        cancel_button.place(x=475, y=300)

        cancel_button = tk.Button(
            self, text="Cancel", padx=60, pady=18, fg="white", bg='#343332', font=("Arial Bold", 10),
            command=lambda: controller.show_frame("moneyMoves"))
        cancel_button.place(x=150, y=300)

        def deposit():
            """
             Handles the deposit/withdraw functionality
            """
            money = amount_entry.get()
            try:
                ATM.currUser.deposit(float(money))
            except ValueError:
                messagebox.showerror("Error",
                                     "Invalid Input")
            amount_entry.delete(0, END)
            update_p2_label(self)
            ATM.updateBalance()
            controller.show_frame("Dashboard")

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
        moneyTransfer.place(x=300, y=175)

        amount_entry = Entry(self, width=20, fg='black', text="$",
                             font=('Arial 15'), borderwidth=2)
        amount_entry.place(x=290, y=220)

        cancel_button = tk.Button(
            self, text="Confirm", padx=60, pady=18, fg="white", bg='#343332', font=("Arial Bold", 10),
            command=lambda: withdraw())
        cancel_button.place(x=475, y=300)

        cancel_button = tk.Button(
            self, text="Cancel", padx=60, pady=18, fg="white", bg='#343332', font=("Arial Bold", 10),
            command=lambda: controller.show_frame("moneyMoves"))
        cancel_button.place(x=150, y=300)

        def withdraw():
            """
             Handles the deposit/withdraw functionality
            """
            money = amount_entry.get()
            try:
                ATM.currUser.withdraw(float(money))
            except ValueError:
                messagebox.showerror("Error",
                                     "Invalid Input")
            amount_entry.delete(0, END)
            update_p2_label(self)
            ATM.updateBalance()
            controller.show_frame("Dashboard")

        def update_p2_label(self):
            self.controller.displayText.set(
                "${:,.2f}".format(ATM.currUser.balance))


if __name__ == "__main__":
    root = Controller()
    root.mainloop()
