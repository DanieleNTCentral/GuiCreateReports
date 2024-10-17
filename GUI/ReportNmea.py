from tkinter import *
import CreateReport
from tkinter import ttk




root= Tk()

# root window title and dimension
root.title("Create Report")
# Set geometry(widthxheight)
root.geometry('800x600+800-100')

icon=PhotoImage(file='satellite.png')
root.iconphoto(True,icon)
root.resizable(False,False)#disabilitato il resize della form

#adding a label to the root window
lbl = Label(root, text ="ok")
lbl.grid()

#botton
iconBotton=PhotoImage(file='report3.png')
btn=Button(text="Create Report",command=CreateReport.writeReport(),image=iconBotton, compound="left", background="white")
btn.grid()
# Execute Tkinter
root.mainloop()