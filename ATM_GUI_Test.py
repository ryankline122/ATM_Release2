from tkinter import *

import tkinter as tk
from tkinter import font as tkfont
from PIL import Image, ImageTk
# import ntag2
import ATM
from tkinter.ttk import Progressbar
from multiprocessing import Pool
import sys
import time


#class that controls frame switching
class Controller(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, WelcomePage, LoginPage, Dashboard):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
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

        main_label = Label(self, text="Hello User",
                        bg='#FEFEFE', font=("Arial Bold", 25))
        main_label.place(x=315, y=20)


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

class LoginPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller


    def loop(dots): #waiting animation
        Secondary_label = Label(root.frames["LoginPage"], text="Waiting",
                    bg='#FEFEFE', font=("Arial Bold", 15))
        Secondary_label.place(x=295, y=145)

        while login():
            Secondary_label.config(text="Waiting" + "." * (dots % 3 + 1), bg='#FEFEFE', font=("Arial Bold", 35))
            dots+=1
            root.update()
            time.sleep(0.5)
        root.show_frame("WelcomePage")

        Welcome_name_label = Label(root.frames["WelcomePage"], text="Hello " + ATM.currUser.name,
                        bg='#FEFEFE', font=("Arial Bold", 25))
        Welcome_name_label.place(x=315, y=20)
        print(ATM.currUser.name)


def login():
    cardUID = "0x40x130x840xb20x6f0x6f0x81" #change to ntag2.readCard()
    expectedCardNum = ATM.get_key(cardUID)
    ATM.login(expectedCardNum) 


if __name__ == "__main__":
    root = Controller()
    root.mainloop()
