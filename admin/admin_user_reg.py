"""Admin User Registration Window."""

from tkinter import *
from tkinter import messagebox
import re
from tkinter import ttk, Tk
import sqlite3
from sqlite3 import Error
import os, sys
# from database import lms_database
py=sys.executable


class admin_user_reg(Tk):
    """Admin registration window class."""

    def __init__(self):
        """Class construction."""
        super().__init__()
        # window title
        self.title("Defect Management - Admin User Registration")
        # window size and state
        self.maxsize(1366, 768)
        self.minsize(1366, 768)
        self.state("zoomed")
        # set window icon
        self.iconbitmap(r'images/defect.ico')
        # set window background
        self.configure(background="dark blue")
        # data input elements
        admin_id = StringVar()
        admin_name = StringVar()
        admin_password = StringVar()
        admin_email = StringVar()
        admin_phone = StringVar()

        def insert():
            """Register new admin user."""
            try:
                # Connect to database
                self.conn = sqlite3.connect("defect_management.db")
                # start a cursor
                self.myCursor = self.conn.cursor()
                # execute data insert query
                result = self.myCursor.execute("Insert into admin values (?,?,?,?,?)", [admin_id.get(), admin_name.get(), admin_password.get(), admin_email.get(), admin_phone.get()])
                # close db cursor and connection then close it
                self.conn.commit()
                self.myCursor.close()
                self.conn.close()
                # if execute result is susccessfull
                if result:
                    # show success message
                    messagebox.showinfo("Confirm", "Data Inserted Successfully")
                    # close window
                    self.destroy()
                    # go to main screen for login
                    os.system('%s %s' % (py, 'main.py'))
            except Error:
                # in error case will show message
                messagebox.showinfo("Error", "Something Goes Wrong")

        def close():
            """Go back to main window."""
            self.destroy()
            os.system('%s %s' % (py, 'main.py'))

        def verify_input():
            """Verify user input."""
            if(len(admin_id.get())) < 5:    # user id is less then 5 letter
                messagebox.showinfo("Error", "Enter User Id\nUser Id should be greater than 5 letters")
            elif (len(admin_name.get())) < 3:
                messagebox.showinfo("Error", "Please Enter Full Name at least 3 letters")
            elif (len(admin_password.get())) < 8:
                if len(admin_password.get()) == 0:
                    messagebox.showinfo("Error", "Please Enter Password")
                else:
                    messagebox.showinfo("Error", "Minimum 8 characters.\nThe alphabets must be between [a-z]\nAt least one alphabet should be of Upper Case [A-Z]\nAt least 1 number or digit between [0-9].\nAt least 1 character from [ _ or @ or $ ].")
            elif (len(admin_password.get())) >= 8 and self.is_valid_password(admin_password.get()) is False:
                messagebox.showinfo("Error", "Minimum 8 characters.\nThe alphabets must be between [a-z]\nAt least one alphabet should be of Upper Case [A-Z]\nAt least 1 number or digit between [0-9].\nAt least 1 character from [ _ or @ or $ ].")
            elif len(admin_email.get()) == 0:
                messagebox.showinfo("Error", "Please input email")
            elif len(admin_phone.get()) == 0:
                messagebox.showinfo("Error", "Please input phone number")
            else:
                insert()
        # label
        input_form = Frame(self, width=650, height=400, bg="light blue").place(x=370, y=200)
        Label(self, text="Defect Management System", font=("Arial", 35, 'bold'), fg="white", bg="dark blue").place(x=350, y=80)
        Label(self, text="New user information", font=("Arial", 20, 'bold'), fg="white", bg="dark blue").place(x=450, y=650)
        # Label(input_form, text = "User Information",font = ("Arial",13,"bold"),bg="light blue").place(x=600,y=220)
        Label(input_form, text="User ID", font=("Arial", 13, "bold"), bg="light blue").place(x=420, y=260)
        Label(input_form, text="Full Name", font=("Arial", 13, "bold"), bg="light blue").place(x=420, y=300)
        Label(input_form, text="Password", font=("Arial", 13, "bold"), bg="light blue").place(x=420, y=340)
        Label(input_form, text="Email", font=("Arial", 13, "bold"), bg="light blue").place(x=420, y=380)
        Label(input_form, text="Phone", font=("Arial", 13, "bold"), bg="light blue").place(x=420, y=420)
        # input
        Entry(input_form, textvariable=admin_id, width=60).place(x=620, y=260)
        Entry(input_form, textvariable=admin_name, width=60).place(x=620, y=300)
        Entry(input_form, show='*', textvariable=admin_password, width=60).place(x=620, y=340)
        Entry(input_form, textvariable=admin_email, width=60).place(x=620, y=380)
        Entry(input_form, textvariable=admin_phone, width=60).place(x=620, y=420)
        Button(input_form, text="Save", width=10, font=("Arial", 13, "bold"), command=verify_input).place(x=560, y=540)
        Button(input_form, text="Cancel", width=10, font=("Arial", 13, "bold"), command=close).place(x=720, y=540)

    def is_valid_password(self, password):
        """Validate input password."""
        while True:
            # if not contain any lower case alphabete
            if not re.search("[a-z]", password):
                flag = -1
                break
            # if not contain any upper case alphabete
            elif not re.search("[A-Z]", password):
                flag = -1
                break
            # if not contain any numeric letter
            elif not re.search("[0-9]", password):
                flag = -1
                break
            # if not contain any special character
            elif not re.search("[_@$]", password):
                flag = -1
                break
            else:   # all condition passed
                flag = 0
                break
        # return true or false base on the flag value
        return flag==0


# main loop for this window
admin_user_reg().mainloop()