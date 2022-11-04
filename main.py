from tkinter import *
from tkinter import messagebox
import sqlite3
from sqlite3 import Error
import os, sys
from database.defect_database import defect_database

py=sys.executable


#creating window
class Asap(Tk):
    def __init__(self):
        super().__init__()
        self.user_id = StringVar()
        self.user_password = StringVar()
        self.geometry("1366x768")
        self.maxsize(1366, 768)
        self.minsize(1366, 768)
        self.state("zoomed")
        self.iconbitmap(r'images/defect.ico')
        self.canvas = Canvas(width=1366, height=768, bg='white')
        self.canvas.pack()
        self.photo = PhotoImage(file='images/road_defect_bg.png')
        self.canvas.create_image(0, 0, image=self.photo, anchor=NW)
        self.title("Defect Managemenet")


        #verifying input
        def check_login():
            if len(self.user_text.get()) < 0:
                messagebox.showinfo("Oop's","Please Enter Your User Id")
            elif len(self.pass_text.get()) < 0:
                messagebox.showinfo("Oop's","Please Enter Your Password")
            else:
                try:
                    self.conn = sqlite3.connect(defect_database.database_name)
                    self.myCursor = self.conn.cursor()
                    self.myCursor.execute("Select * from admin where id=? AND password =?",[self.user_text.get(),self.pass_text.get()])
                    self.pc = self.myCursor.fetchall()
                    self.myCursor.close()
                    self.conn.close()
                    if self.pc:
                        self.destroy()
                        os.system('%s %s' % (py, 'home.py'))
                    else:
                        messagebox.showinfo('Error', 'Username and password are not found')
                        # self.user_text.delete(0, END)
                        # self.pass_text.delete(0, END)
                except Error:
                    messagebox.showinfo('Error',"Something is not right. Restarting the application...")
        def fp():
            os.system('%s %s' % (py, 'f_passwd.py'))

        def check_admin_exists():
            try:
                conn = sqlite3.connect(defect_database.database_name)
                mycursor = conn.cursor()
                mycursor.execute("Select * from admin")
                admin_user = mycursor.fetchone()
                mycursor.close()
                conn.close()
                if not admin_user:
                    messagebox.showinfo("Error", "Current database does not have an admin user.")
                    x = messagebox.askyesno("Confirm","Do you want to register an user?")
                    if x:
                        self.destroy()
                        os.system('%s %s' % (py, 'admin/admin_user_reg.py'))
                else:
                    input_form = Frame(self, width=650, height=300, bg="light blue").place(x=370, y=200)
                    self.label = Label(self, text="Admin Login", font=("Arial", 35, 'bold'),bg="light blue")
                    self.label.place(x=530, y=30)
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
                    # buttons
                    self.butt = Button(input_form, text="Login", font=10, width=15, command=check_login).place(x=460, y=400)
                    self.butt2 = Button(input_form, text="Forgot Password", font=10, width=18, command=fp).place(x=700, y=400)
            except Error:
                messagebox.showinfo("Error", "The application can not start properly. \nPlease check the configuration.")

        check_admin_exists()

Asap().mainloop()