import tkinter as tk
from tkinter import *
from tkinter import ttk, filedialog

#GMAIL IMPORTS
import main
import threading

#UI
win = Tk()
win.geometry("700x400")
win.title("Gmail API Automation")

def on_exit():
   global label_status
   # MY_THREAD.join()

   label_status.config(text="Stopped", foreground="red")

   main.stop()
   main.exitout()
   win.destroy()

win.protocol('WM_DELETE_WINDOW', on_exit)

#Global Variables
LOCATION = "./"
MY_THREAD = None
label_status = None

label_location = Label(win, text=LOCATION, font=('Georgia 10'))
label_location.place(x=400, y=88)

label_status_title = Label(win, text="Status : ", font=('Georgia 10'))
label_status_title.place(x=20, y=370)

label_status = Label(win, text="Stopped", font=('Georgia 10'), foreground="red")
label_status.place(x=80, y=370)

listBox = Listbox(win, width=75, height=12, xscrollcommand=True, yscrollcommand=True)
listBox.place(x=200 , y=120, anchor=NW)


#UI Helper Functions

def on_start():
   global MY_THREAD, label_status

   main.LISTBOX = listBox
   MY_THREAD = threading.Thread(target=main.start)
   MY_THREAD.start()

   label_status.config(text="Running...", foreground="green")


def on_stop():
   global label_status
   main.stop()
   label_status.config(text="Stopped", foreground="red")
   



def open_file():
   global LOCATION
   folder = filedialog.askdirectory()
   if folder:
      LOCATION = folder
      label_location.configure(text=LOCATION)
      main.setLocation(LOCATION)


def on_reset():
   main.reset_listbox()

def type_of_user(text):
   main.set_type_of_user(text)

##Remove max button
win.resizable(0,0)



#Background
# bg = PhotoImage(file = "./bg.png")
# bglabel = Label(win, image=bg)
# bglabel.place(x=0, y=0, relheight=1, relwidth=1)

label_title = Label(win, text="Gmail Attachment Automation", font=("Times 24"), bg='#9ED2C6')
label_title.place(x=220, y=20)

label_select_folder = Label(win, text="Select folder", font=('Georgia 10'))
label_select_folder.place(x=200, y=88, anchor=NW)
# STYLING BUTTON
style_browse = ttk.Style()
style_browse.configure('TButton', font =('calibri', 12),borderwidth = '5')
style_browse.map('TButton', foreground = [('active', '!disabled', 'green')],background = [('active', 'black')])

## Browse Button
ttk.Button(win, text="Browse", width=8, command=open_file).place(x=300, y=85, anchor=NW)



#button widget
b1 = Button(win, text = "START", width=8,bg="green", fg="white", command=on_start)
b1.place( x =80, y = 140, anchor = NW)

b2 = Button(win, text = "STOP", bg="red", fg="white", width=8, command=on_stop)
b2.place( x =80, y = 190, anchor = NW)



resetBtn = Button(win, text = "CLEAR", bg="blue", fg="yellow", width=8, command=on_reset)
resetBtn.place( x=585, y = 319, anchor = NW)


menu= StringVar()
menu.set("Choose one")
label_type_of_user = Label(win, text="Type Of User", font=('Georgia 10'))
label_type_of_user.place(x=200, y=320, anchor=NW)

drop= OptionMenu(win, menu,"Very Frequent", "Casual", "Less Frequent", command=type_of_user)

drop.place(x=300, y=316, anchor=NW)

win.mainloop()