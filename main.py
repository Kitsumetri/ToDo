from front import application_ui
import customtkinter
from tkinter import *


def test1():
    app = customtkinter.CTk()
    app.grid_rowconfigure(0, weight=1)
    app.grid_columnconfigure(0, weight=1)

    # create scrollable textbox
    tk_textbox = Text(app, highlightthickness=0)
    tk_textbox.grid(row=0, column=0, sticky="nsew")

    # create CTk scrollbar
    ctk_textbox_scrollbar = customtkinter.CTkScrollbar(app, command=tk_textbox.yview)
    ctk_textbox_scrollbar.grid(row=0, column=1, sticky="ns")

    # connect textbox scroll event to CTk scrollbar
    tk_textbox.configure(yscrollcommand=ctk_textbox_scrollbar.set)

    app.mainloop()


def test2():
    root = Tk()
    scrollbar = Scrollbar(root)
    scrollbar.pack(side=RIGHT, fill=Y)

    mylist = Listbox(root, yscrollcommand=scrollbar.set)
    for line in range(100):
        mylist.insert(END, "This is line number " + str(line))

    mylist.pack(side=LEFT, fill=BOTH)
    scrollbar.config(command=mylist.yview)

    mainloop()


if __name__ == "__main__":
    #test1()
    # test2()
    application_ui()


