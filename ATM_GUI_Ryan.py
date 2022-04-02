from tkinter import *

import tkinter as tk
from tkinter import font as tkfont
from PIL import Image, ImageTk
from tkinter import ttk, messagebox

import RPi.GPIO as GPIO
import pn532.pn532 as nfc
import ATM


from pn532 import *
import time


pn532 = PN532_SPI(cs=4, reset=20, debug=False)
ic, ver, rev, support = pn532.get_firmware_version()
print('Found PN532 with firmware version: {0}.{1}'.format(ver, rev))

# Configure PN532 to communicate with NTAG215 cards
pn532.SAM_configuration()


#class that controls frame switching
class Controller(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        self.displayText = tk.StringVar()
        # self.displayText.set(str("${:,.2f}".format(ATM.currUser.balance)))

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, WelcomePage, LoginPage, Dashboard, moneyMoves):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        #Show a frame for the given page name
        frame = self.frames[page_name]
        frame.tkraise()



#startPage with activate scanner button
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

        info_label = Label(
            self, text="Scan your card to login", bg='#FEFEFE', font=("Arial", 15))
        info_label.place(x=300, y=100)

        # NFC Image
        nfcImg = Image.open('icon.png')
        resized = nfcImg.resize((85, 65), Image.ANTIALIAS)
        new_pic = ImageTk.PhotoImage(resized)

        nfc_label = Label(self, image=new_pic, bg='#FEFEFE')
        nfc_label.place(x=357.5, y=175)

        button = tk.Button(self, text="Activate Scanner", padx=25, pady=25,
               command=lambda:[controller.show_frame("LoginPage"), LoginPage.loop(0)])
        button.place(x=340, y=310)



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


        viewPassBtn = tk.Button(self, text="Show Password", padx=25,pady=25, fg="white", bg='#343332',
                                command=lambda:togglePassword())
        viewPassBtn.place(x=330, y=310)

        password = Entry(self, show="*", width=20, fg='black', font=('Arial 15'), borderwidth=2)
        password.place(x=290, y=205)

        backButton = tk.Button(self, text="Back", padx=50, pady=30, fg="white", bg='#da1723',
                                command=lambda: controller.show_frame("StartPage"))
        backButton.place(x=90, y=180)

        nextButton = tk.Button(self, text="Next", padx=50, pady=30, fg="white", bg='#1ebc3f',
                                command=lambda: controller.show_frame("Dashboard"))
        nextButton.place(x=575, y=180)



#unfinished, just using to test old code with new class implementation
class Dashboard(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        f4_frame = LabelFrame(self, width=800, height=480)
        f4_frame.pack(fill="both", expand=1)

        f4_canvas = Canvas(f4_frame, width=800, height=480, bg="white")
        f4_canvas.place(x=0, y=0)

        # Define a Canvas Widget
        canvasT4 = Canvas(f4_frame, width=800, height=400, bg='#75706F')
        canvasT4.place(x=0, y=0)

        canvasT2 = Canvas(f4_frame, width=390, height=150, bg='#343332')
        canvasT2.place(x=210, y=5)

        canvasT3 = Canvas(f4_frame, width=700, height=150, bg='#343332')
        canvasT3.place(x=50, y=180)

        recentLogLabel = Label(f4_frame, text="Available Features", padx=10, pady=10, bg='#343332', fg='gray',
                               font='Times 10 bold')
        recentLogLabel.place(x=335, y=185)

        checkingAccountLabel = Label(f4_frame, text="Account Balance", padx=10, pady=10, bg='#343332', fg='gray')
        checkingAccountLabel.place(x=220, y=10)

        availableBalanceLabel = Label(f4_frame, text="Available Balance", padx=10, pady=10, bg='#343332', fg='gray',
                                      font="Italics 7")
        availableBalanceLabel.place(x=215, y=105)


        checkingAccountBalanceLabel = Label(self, textvariable=controller.displayText, bg='#343332', fg='gray',
                                            font="Times 18 bold")
        checkingAccountBalanceLabel.place(x=225, y=80)

        moneyMovesButton = tk.Button(self, text="Deposit/Withdraw Screen", padx=7, pady=7, fg="white",
                                     bg='#343332', command=lambda: controller.show_frame("moneyMoves"))
        moneyMovesButton.place(x=120, y=240)


        #transferButton = tk.Button(self, text="Transfer Portal", padx=7, pady=7, fg="white", bg='#343332',
        #                           command=lambda: raiseFrame(transferFrame))
        #transferButton.place(x=310, y=240)

        #changePasswordButton = tk.Button(self, text="Change Password", padx=7, pady=7, fg="white", bg='#343332',
        #                                 command=lambda: raiseFrame(passwordChange))
        #changePasswordButton.place(x=450, y=240)

        logoutButton = tk.Button(self, text="logout", padx=10, pady=10, fg="white", bg='#da1723',
                                 command=lambda: controller.show_frame("StartPage"))
        logoutButton.place(x=30, y=10)


class moneyMoves(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        depoWithFrame = LabelFrame(self, width=800, height=400)
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
                                command=lambda: moneymoves())
        doneButton2.place(x=600, y=300)

        backButton = tk.Button(depoWithFrame, text="Back", padx=17, pady=17, fg="white", bg='#343332',
                               command=lambda: controller.show_frame("Dashboard"))
        backButton.place(x=100, y=300)

        options = [
            "Deposit",
            "Withdraw"
        ]

        myCombo = ttk.Combobox(depoWithFrame, value=options)
        myCombo.current(0)
        myCombo.pack(pady=80)

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
                        messagebox.showerror("Error",
                                            "Make sure that you are: Putting in only integers and that integer is greater than 0 and less than 999999999999")
                else:
                    try:
                        ATM.currUser.withdraw(float(money))
                    except ValueError:
                        messagebox.showerror("Error",
                                            "Make sure that you are: Putting in only integers and that integer is greater than 0 and not greater than your account balance")

                if balancePreMoneyMove == ATM.currUser.balance:
                    moneyInput.delete(0, END)
                else:
                    ATM.updateBalance()
                    self.update_p2_label()
                    moneyInput.delete(0, END)
                    controller.show_frame("Dashboard")

    def update_p2_label(self):
        self.controller.displayText.set("${:,.2f}".format(ATM.currUser.balance))


class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        global Welcome_name_label
        Welcome_name_label = Label(controller.frames["WelcomePage"], text="Hello ",
                            bg='#FEFEFE', font=("Arial Bold", 25))
        Welcome_name_label.place(x=315, y=20)

        global Secondary_label
        Secondary_label = Label(self, text="Waiting",
                        bg='#FEFEFE', font=("Arial Bold", 15))
        Secondary_label.place(x=295, y=145)


    #waiting animation
    def loop(dots): 
        Secondary_label.config(text="Waiting")

        while (True):
            Secondary_label.config(text="Waiting" + "." * (dots % 3 + 1), bg='#FEFEFE', font=("Arial Bold", 35))
            dots+=1
            root.update()
            time.sleep(0.5)
            uid = pn532.read_passive_target(timeout=0.5)            
            if uid is not None:
                break
            
        uidArr = [hex(i) for i in uid]
        uidStr = ""

        for i in uidArr:
            uidStr += str(i)

        login(uidStr)
        print(str(ATM.currUser.name))
        Welcome_name_label.config(text= str(ATM.currUser.name))
        root.show_frame("WelcomePage")




# End of GUI

def login(cardUID):
    ATM.logoutAll()
    expectedCardNum = ATM.get_key(cardUID)
    ATM.login(expectedCardNum) 


if __name__ == "__main__":
    root = Controller()
    root.mainloop()
    GPIO.cleanup()
