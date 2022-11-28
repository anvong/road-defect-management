"""This is assignment 2 - question 2: Road Defect Management Mini Application.
Entry point for the application."""
# student name: Gia An Vong - s354803

from tkinter import * # noqa
from tkinter import messagebox, Tk
import os, sys  # noqa
import sqlite3
from sqlite3 import Error
from database.defect_database import defect_database # noqa E0401

py = sys.executable

class Asap(Tk):
    """Startup windows of the application."""

    def __init__(self):
        """Class constructor."""
        super().__init__()
        # input field for user login
        self.user_id = StringVar()
        self.user_password = StringVar()
        # set window size 
        self.geometry("1366x768")
        self.maxsize(1366, 768)
        self.minsize(1366, 768)
        # make the windows zoomed to max size
        self.state("zoomed")
        # set the fav-icon on the window left-top corner
        self.iconbitmap(r'images/defect.ico')
        # show the screen backgound 
        self.canvas = Canvas(width=1366, height=768, bg='white')
        self.canvas.pack()
        self.photo = PhotoImage(file='images/road_defect_bg.png')
        self.canvas.create_image(0, 0, image=self.photo, anchor=NW)
        # set window title
        self.title("Defect Managemenet")
        # check if an exist admin user on the system
        self.check_admin_exists()

    def check_login(self):
        """Verify login user and password."""
        # user name is blank
        if len(self.user_text.get()) < 0:
            messagebox.showinfo("Oop's", "Please Enter User Id")
        # password is blank
        elif len(self.pass_text.get()) < 0:
            messagebox.showinfo("Oop's", "Please Enter Password")
        else:
            try:
                # setup db connection
                self.conn = sqlite3.connect(defect_database.database_name)
                self.myCursor = self.conn.cursor()
                # prepare select SQL
                self.myCursor.execute("Select * from admin where id=? AND password =?", [self.user_text.get(), self.pass_text.get()]) 
                # fetch data from given SQL exection
                self.pc = self.myCursor.fetchall()
                # close data cursor and connection
                self.myCursor.close()
                self.conn.close()
                if self.pc:
                    self.destroy()
                    os.system('%s %s' % (py, 'home.py'))
                else:
                    messagebox.showinfo('Error', 'Username and password are not found') 

            except Error:
                # Error happen
                messagebox.showinfo('Error', "Something is not right. Restarting the application...")

    def check_admin_exists(self):
        """Check if at least one records inside admin table, otherwise require user to register one."""
        try:
            # prepare database connection
            conn = sqlite3.connect(defect_database.database_name)
            mycursor = conn.cursor()
            # select data from admin table
            mycursor.execute("Select * from admin")
            admin_user = mycursor.fetchone()
            # close data reader and connection
            mycursor.close()
            conn.close()

            # If there is no admin user
            if not admin_user:
                # show error message
                messagebox.showinfo("Error", "Current database does not have an admin user.")
                # confirm if user would like to register an admin user for starting the system
                answer = messagebox.askyesno("Confirm", "Do you want to register an admin user?")
                if answer:
                    # close current windows
                    self.destroy()
                    # open admin register window
                    os.system('%s %s %s' % (py, 'admin/admin_user_reg.py', 'main'))
            else:
                # in case already have admin user will show the login form
                # create an admin user info input form
                input_form = Frame(self, width=650, height=300, bg="light blue").place(x=370, y=200)
                # form title label
                self.label = Label(self, text="Admin Login", font=("Arial", 35, 'bold'),bg="light blue")
                self.label.place(x=530, y=80)
                # user id label and input
                self.label1 = Label(input_form, text="User ID", font=("Arial", 15, "bold"), bg="light blue")
                self.label1.place(x=450, y=260)
                self.user_text = Entry(input_form, textvariable=self.user_id, width=45)
                self.user_text.place(x=650, y=260)
                # password label and input
                self.label2 = Label(input_form, text="Password", font=("Arial", 15, 'bold'), bg="light blue")
                self.label2.place(x=450, y=300)
                self.pass_text = Entry(input_form, show='*', textvariable=self.user_password, width=45)
                self.pass_text.place(x=650, y=300)
                # Login button
                self.butt = Button(input_form, text="Login", font=10, width=15, command=self.check_login).place(x=460, y=400)
                # Forgot Password button, disable for this version.
                self.butt2 = Button(input_form, text="Forgot Password", font=10, width=18, state=DISABLED).place(x=700, y=400)

        except Error:
            messagebox.showinfo("Error", "The application can not start. Please check the configuration.")

Asap().mainloop()
