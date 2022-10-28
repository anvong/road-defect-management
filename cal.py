import tkinter  as tk 
from tkcalendar import DateEntry
my_w = tk.Tk()
my_w.geometry("380x220")  

cal=DateEntry(my_w,selectmode='day')
cal.grid(row=0,column=0,padx=15,pady=10)

b1=tk.Button(my_w,text='Clear',font=20,command=lambda:cal.delete(0,'end'))
b1.grid(row=0,column=1,padx=10)
my_w.mainloop()