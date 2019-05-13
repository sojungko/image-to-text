# this file is for user interface
# https://likegeeks.com/python-gui-examples-tkinter-tutorial/#Create-a-label-widget

from tkinter import *
from tkinter import filedialog
from os import path


def chooseFile():
    file = filedialog.askopenfilename(initialdir=path.dirname('term project'),
                                      filetypes=(("image files", "*.png"), ("jpeg files", "*.jpg")))
    # once you choose file, the file path will be stored in file variable
    return file  # return the file path


def enterClicked():
    result = 'Loading ' + inputBox.get() + '...'
    message = Label(window, text=result, font='Helvetica,12')
    message.grid(column=1, row=2)


def cancelClicked():
    result = "Exiting..."
    inputBox = Entry(window, width=15, state='disabled')
    message = Label(window, text=result, font="Helvetica,12")
    message.grid(column=1, row=2)
    window.quit()


def run():  # may not need any kind of window since chooseFile func does everything
    window = Tk()
    window.title("Select Image")  # this creates window named select image
    window.geometry('400x120')
    entry1 = Label(window, text='Input image path: ', font='Helvetica, 18')
    entry1.grid(column=0, row=0)
    inputBox = Entry(window, width=15)
    inputBox.grid(column=1, row=0)
    button1 = Button(window, text="Enter", bg='grey',
                     fg='black', command=enterClicked)
    button1.grid(column=3, row=2)
    button2 = Button(window, text="Cancel", bg='grey',
                     fg='red', command=cancelClicked)
    button2.grid(column=0, row=2)
    file = chooseFile()  # store the return value(file path) to variable file here

    inputBox.focus()
    window.mainloop()
    # when run, a message starting with 'objc[48448]' will appear.
    # please igonore it, for it is due to incompatibility issue between macOS High Sierra
    # and Tkinter
    return file


run()
