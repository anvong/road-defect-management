from tkinter import *
from tkinter import messagebox
import re
from tkinter import ttk
import sqlite3
from sqlite3 import Error
import os,sys
# from database import lms_database
py=sys.executable

#creating window
class admin_user_reg(Tk):
    def __init__(self):
        super().__init__()
        self.title("Defect Management")
        self.maxsize(1366, 768)
        self.minsize(1366, 768)
        self.state("zoomed")
        self.iconbitmap(r'images/defect.ico')
        self.configure(background="dark blue")
        #creating variables Please chech carefully
        admin_id = StringVar()
        admin_name = StringVar()
        admin_password = StringVar()
        admin_email = StringVar()
        admin_phone = StringVar()
        
        # u = StringVar()
        # s = StringVar()
        # r = StringVar()

        def insert():
            try:
                # lms_db = lms_database()
                self.conn = sqlite3.connect("defect_management.db")
                self.myCursor = self.conn.cursor()
                c = self.myCursor.execute("Insert into admin values (?,?,?,?,?)", [admin_id.get(), admin_name.get(), admin_password.get(), admin_email.get(), admin_phone.get()])
                self.conn.commit()
                self.myCursor.close()
                self.conn.close()
                if c:
                    messagebox.showinfo("Confirm", "Data Inserted Successfully")
                    self.destroy()
                    os.system('%s %s' % (py, 'main.py'))
            except Error:
                messagebox.showinfo("Error", "Something Goes Wrong")
        
        def close():
            """Go back to main."""
            self.destroy()
            os.system('%s %s' % (py, 'main.py'))
            
        # verify input
        def verify():
            if(len(admin_id.get())) < 5:
                messagebox.showinfo("Error","Enter User Id\nUser Id should be greater than 5 letters")
            elif (len(admin_name.get())) < 3:
                messagebox.showinfo("Error", "Please Enter Your Full Name at least 3 letters")
            elif (len(admin_password.get())) < 8:
                while True:
                    if not re.search("[a-z]", admin_password.get()):
                        flag = -1
                        break
                    elif not re.search("[A-Z]", admin_password.get()):
                        flag = -1
                        break
                    elif not re.search("[0-9]", admin_password.get()):
                        flag = -1
                        break
                    elif not re.search("[_@$]", admin_password.get()):
                        flag = -1
                        break
                    elif re.search("\s", admin_password.get()):
                        flag = -1
                        break
                    else:
                        flag = 0
                        break
                if len(admin_password.get()) == 0:
                    messagebox.showinfo("Error","Please Enter Your Password")
                elif flag == -1:
                    messagebox.showinfo("Error","Minimum 8 characters.\nThe alphabets must be between [a-z]\nAt least one alphabet should be of Upper Case [A-Z]\nAt least 1 number or digit between [0-9].\nAt least 1 character from [ _ or @ or $ ].")
            elif len(admin_email.get()) == 0:
                messagebox.showinfo("Error","Please input your email")
            elif len(admin_phone.get()) == 0:
                messagebox.showinfo("Error","Please input your phone number")    
            else:
                insert()
        # label 
        input_form = Frame(self, width=650, height=400, bg="light blue").place(x=370, y=200)
        Label(self,text="Defect Management System",font=("Arial",35,'bold'),fg="white",bg="dark blue").place(x=350,y=80)
        Label(self,text="New user information",font=("Arial",20,'bold'),fg="white",bg="dark blue").place(x=450,y=650)
        # Label(input_form, text = "User Information",font = ("Arial",13,"bold"),bg="light blue").place(x=600,y=220)
        Label(input_form, text="User ID", font=("Arial", 13, "bold"), bg="light blue").place(x=420, y=260)
        Label(input_form, text="Full Name", font=("Arial", 13, "bold"), bg="light blue").place(x=420, y=300)
        Label(input_form, text="Password", font=("Arial", 13, "bold"), bg="light blue").place(x=420, y=340)
        Label(input_form, text="Email", font=("Arial", 13, "bold"), bg="light blue").place(x=420, y=380)
        Label(input_form, text="Phone", font=("Arial", 13, "bold"), bg="light blue").place(x=420, y=420)
        # input
        Entry(input_form, textvariable=admin_id, width=60).place(x=620,y=260)
        Entry(input_form, textvariable=admin_name, width=60).place(x=620, y=300)
        Entry(input_form, show = '*', textvariable=admin_password, width=60).place(x=620, y=340)
        Entry(input_form, textvariable=admin_email, width=60).place(x=620, y=380)
        Entry(input_form, textvariable=admin_phone, width=60).place(x=620, y=420)
        Button(input_form, text="Save", width=10, font=("Arial", 13, "bold"), command=verify).place(x=560, y=540)
        Button(input_form, text="Cancel", width=10, font=("Arial", 13, "bold"),command=close).place(x=720, y=540)

admin_user_reg().mainloop()