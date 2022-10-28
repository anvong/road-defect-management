from tkinter import *
from tkinter import messagebox
import re
from tkinter import ttk
import sqlite3
from sqlite3 import Error
import os,sys
from tkcalendar import DateEntry

# from database import lms_database
py=sys.executable

#creating window
class add_defect(Tk):
    def __init__(self):
        super().__init__()
        self.title("Defect Management")
        self.maxsize(1366, 768)
        self.minsize(1366, 768)
        self.state("zoomed")
        self.iconbitmap(r'images/defect.ico')
        self.configure(background="dark blue")
        #creating variables Please chech carefully
        self.defect_id = StringVar()
        self.defect_road_name = StringVar()
        self.defect_address = StringVar()
        self.status = StringVar()
        self.severity = StringVar()
        self.priority = StringVar()
        self.reported_date = StringVar()
        self.fixed_date = StringVar()
        
        self.create_tree_widget()
        # u = StringVar()
        # s = StringVar()
        # r = StringVar()

    def insert(self):
        try:
            # lms_db = lms_database()
            self.conn = sqlite3.connect("defect_management.db")
            self.myCursor = self.conn.cursor()
            parameters = [self.defect_id.get(),
                          self.defect_road_name.get(),
                          self.defect_address.get(),
                          self.status.get(),
                          self.severity.get(),
                          self.priority.get(),
                          self.reported_date.get(),
                          self.fixed_date.get(),
                          ]
            print(parameters)
            # parameters = [1, '213', 'ada', 'aD', 'ad', 'aDa', None , None ]
            c = self.myCursor.execute("Insert into defects values (?,?,?,?,?,?,?,?)", parameters)
            self.conn.commit()
            self.myCursor.close()
            self.conn.close()
            if c:
                messagebox.showinfo("Confirm", "Data Inserted Successfully")
                self.destroy()
                os.system('%s %s' % (py, 'main.py'))
        except Error:
            print(Error)
            messagebox.showinfo("Error", "Something Goes Wrong")
        
    def close(self):
        """Go back to main."""
        self.destroy()
        os.system('%s %s' % (py, 'home.py'))
            
    # verify input
    def verify(self):
        
        if len(self.defect_id.get()) == 0:
            messagebox.showinfo("Error","Please enter defect id")
        elif len(self.defect_road_name.get()) == 0:
            messagebox.showinfo("Error","Please input road name")
        elif len(self.defect_address.get()) == 0:
            messagebox.showinfo("Error","Please input defect address")
        elif len(self.status.get()) == 0:
            messagebox.showinfo("Error","Please input status")
        elif len(self.severity.get()) == 0:
            messagebox.showinfo("Error","Please input severity")
        elif len(self.reported_date.get()) == 0:
            messagebox.showinfo("Error","Please input reported date")
        else:
            self.insert()
                
    def create_tree_widget(self):   
        # form title text 
        input_form = Frame(self, width=650, height=480, bg="light blue").place(x=370, y=200)
        Label(self,text="New defect entry",font=("Arial",35,'bold'),fg="white",bg="dark blue").place(x=480,y=80)
        # input form lable
        Label(input_form, text="Defect ID", font=("Arial", 13, "bold"), bg="light blue").place(x=420, y=260)
        Label(input_form, text="Road Name", font=("Arial", 13, "bold"), bg="light blue").place(x=420, y=300)
        Label(input_form, text="Road Address", font=("Arial", 13, "bold"), bg="light blue").place(x=420, y=340)
        Label(input_form, text="Status", font=("Arial", 13, "bold"), bg="light blue").place(x=420, y=380)
        Label(input_form, text="Severity", font=("Arial", 13, "bold"), bg="light blue").place(x=420, y=420)
        Label(input_form, text="Rriority", font=("Arial", 13, "bold"), bg="light blue").place(x=420, y=460)
        Label(input_form, text="Reported date", font=("Arial", 13, "bold"), bg="light blue").place(x=420, y=500)
        Label(input_form, text="Fixed date", font=("Arial", 13, "bold"), bg="light blue").place(x=420, y=540)
        
        # input text field for defect id, road name, address
        Entry(input_form, textvariable=self.defect_id, width=60).place(x=620,y=260)
        Entry(input_form, textvariable=self.defect_road_name, width=60).place(x=620, y=300)
        Entry(input_form, textvariable=self.defect_address, width=60).place(x=620, y=340)
        
        # combo box for status, serverity and priority
        ttk.Combobox(input_form,textvariable=self.status,values=["new","in progress","done"],width=57,state="readonly").place(x = 620, y = 380)
        ttk.Combobox(input_form,textvariable=self.severity,values=["critical","major","minor"],width=57,state="readonly").place(x = 620, y = 420)
        ttk.Combobox(input_form,textvariable=self.priority,values=["high","medium","low"],width=57,state="readonly").place(x = 620, y = 460)
        
        # Entry(input_form, textvariable=self.severity, width=60).place(x=620, y=420)
        # Entry(input_form, textvariable=self.priority, width=60).place(x=620, y=460)
        cal1 =DateEntry(input_form,selectmode='day', textvariable = self.reported_date, width=20)
        cal1.place(x=620, y=500)
        Button(input_form,text="clear", width=8, font=("Arial", 9), command=lambda:cal1.delete(0,'end')).place(x=780, y=500)
        
        cal2 = DateEntry(input_form,selectmode='day', textvariable = self.fixed_date, width=20)
        cal2.place(x=620, y=540)
        Button(input_form, text="clear", width=8, font=("Arial", 9), command=lambda:cal2.delete(0,'end')).place(x=780, y=540)
        # Entry(input_form, textvariable=self.reported_date, width=60).place(x=620, y=500)
        # Entry(input_form, textvariable=self.fixed_date, width=60).place(x=620, y=540)
        Button(input_form, text="Save", width=10, font=("Arial", 13, "bold"), command=self.verify).place(x=560, y=620)
        Button(input_form, text="Cancel", width=10, font=("Arial", 13, "bold"),command=self.close).place(x=720, y=620)
    
add_defect().mainloop()