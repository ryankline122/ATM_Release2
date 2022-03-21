from tkinter import *
from PIL import Image, ImageTk
import ntag2
import ATM


def raise_frame(frame):
    frame.tkraise()


def login():
    cardUID = ntag2.readCard()
    expectedCardNum = ATM.get_key(cardUID)
    ATM.login(expectedCardNum)
    raise_frame(f2)

root = Tk()
root.geometry("800x480")


f1 = Frame(root)
f2 = Frame(root)


for frame in (f1, f2):
    frame.grid(row=0, column=0, sticky='news')


# Frame 1 (Boot-up screen)
f1_frame = LabelFrame(f1, width=800, height=480)
f1_frame.pack(fill="both", expand=1)

f1_canvas = Canvas(f1_frame, width=800, height=480, bg="white")
f1_canvas.place(x=0, y=0)


main_label = Label(f1, text="Lakers Credit  Union",
                   bg='#FEFEFE', font=("Arial Bold", 25))
main_label.place(x=250, y=20)

info_label = Label(
    f1, text="Scan your card to login", bg='#FEFEFE', font=("Arial", 15))
info_label.place(x=315, y=100)

# NFC Image
nfcImg = Image.open('icon.png')
resized = nfcImg.resize((85, 65), Image.ANTIALIAS)
new_pic = ImageTk.PhotoImage(resized)

nfc_label = Label(f1, image=new_pic, bg='#FEFEFE')
nfc_label.place(x=375, y=175)


Button(f1, text="Activate Scanner", padx=25, pady=25,
       command=lambda: login()).place(x=340, y=310)

# End of Frame 1

# Frame 2 Confirm PIN Screen

f2_frame = LabelFrame(f2, width=800, height=480)
f2_frame.pack(fill="both", expand=1)

f2_canvas = Canvas(f2_frame, width=800, height=480, bg="white")
f2_canvas.place(x=0, y=0)


main_label = Label(f2, text="Please Confirm Your PIN",
                   bg='#FEFEFE', font=("Arial Bold", 25))
main_label.place(x=200, y=20)



raise_frame(f1)
root.mainloop()
