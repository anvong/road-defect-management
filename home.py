"""Home windows to show defect list."""
from tkinter import *
from tkinter import messagebox, Menu, Label, Entry, Radiobutton, Button
# from tkinter.messagebox import showinfo
import sqlite3
from sqlite3 import Error
import os
import glob
import sys
from tkinter import ttk, Tk
from PIL import ImageTk, Image
from database.defect_database import defect_database

py = sys.executable


class HomeWindow(Tk):
    """Home window class to show defect list, edit, delete, add new records."""

    def __init__(self):
        """Class constructor."""
        super().__init__()
        # display fav-icon on left-top of the window
        self.iconbitmap(r'images/defect.ico')
        # set background color
        self.configure(bg='light blue')
        # set screen size
        self.geometry("1366x768")
        self.maxsize(1366, 768)
        self.minsize(1366, 768)
        self.state('zoomed')
        # set window title
        self.title('Defect Management - Home')
        # search condition input elements
        self.defect_id = StringVar()
        self.road_name = StringVar()
        self.search_status = StringVar()
        self.search_severity = StringVar()
        self.search_priority = StringVar()
        # set up menu
        self.menu_setup()
        # setup_search_condition
        self.setup_search_condition()
        # generate grid layout
        self.create_tree_widget()
        # load data to list
        self.show_all_data()

    def add_defect(self):
        """Create a link menu to add defect window."""
        os.system('%s %s' % (py, 'defect/add_defect.py'))

    def add_user(self):
        """Create a link menu to add admin user window."""
        os.system('%s %s' % (py, 'admin/admin_user_reg.py'))

    def create_tree_widget(self):
        """Generate the data list, scroll bar."""
        # creating table
        data_columns = ('defect_id', 'defect_road_name', 'defect_address', 'status', 'severity', 'priority', 'reported_date', 'fixed_date')
        # define headings properties
        self.listTree = ttk.Treeview(self, height=14, columns=data_columns)
        # scrollbars
        self.vsb = ttk.Scrollbar(self, orient="vertical", command=self.listTree.yview)
        self.hsb = ttk.Scrollbar(self, orient="horizontal", command=self.listTree.xview)

        # tree view header text
        self.listTree.heading("#0", text='#', anchor='center')
        self.listTree.heading('defect_id', text='defect id')
        self.listTree.heading('defect_road_name', text='Road name')
        self.listTree.heading('defect_address', text='Address')
        self.listTree.heading('status', text='Status')
        self.listTree.heading('severity', text='Severity')
        self.listTree.heading('priority', text='Priority')
        self.listTree.heading('reported_date', text='Reported date')
        self.listTree.heading('fixed_date', text='Fixed date')

        # config column size and text alignment
        self.listTree.column("#0", width=50, minwidth=50, anchor='center')
        self.listTree.column("defect_id", width=100, minwidth=100, anchor='center')
        self.listTree.column("defect_road_name", width=200, minwidth=200, anchor='center')
        self.listTree.column("defect_address", width=200, minwidth=200, anchor='center')
        self.listTree.column("status", width=100, minwidth=100, anchor='center')
        self.listTree.column("severity", width=100, minwidth=100, anchor='center')
        self.listTree.column("priority", width=100, minwidth=100, anchor='center')
        self.listTree.column("reported_date", width=100, minwidth=100, anchor='center')
        self.listTree.column("fixed_date", width=100, minwidth=100, anchor='center')
        self.listTree.bind("<ButtonRelease-1>", self.item_selected)
        # set the location for the tree view
        self.listTree.place(x=90, y=360, height=350)
        # add scrollbard next to datagrid
        self.vsb.place(x=1142, y=360, height=346)
        # self.hsb.place(x=91, y=711, width=1050) # uncomment to have horizontal bar display

        # Tree view font size
        ttk.Style().configure("Treeview", font=('Arial', 10))

        # Add a preview photo lable
        Label(self, text="Preview photo", bg='light blue', font=('Arial', 12, 'bold')).place(x=1180, y=330)
        # Add a no-image photo at the beginning
        self.photo = ImageTk.PhotoImage(Image.open("defect_image_tmp/noimage.png"))
        # set photo location
        Label(image=self.photo, width=150, height=100).place(x=1180, y=360)

    def menu_setup(self):
        """Create menu bar."""
        # menu setup
        self.mymenu = Menu(self)
        # creaet defect menu
        list1 = Menu(self, tearoff=False)
        # create admin user menu
        list2 = Menu(self, tearoff=False)
        list1.add_command(label="Add Defects", command=self.add_defect)
        list2.add_command(label="Add User", command=self.add_user)
        # add sub menus to menu bar
        self.mymenu.add_cascade(label='Defects', menu=list1)
        self.mymenu.add_cascade(label='Admin Tools', menu=list2)
        # assign menu object to current window
        self.config(menu=self.mymenu)

    def search_defect(self):
        """Search data by defect id."""
        try:
            # prepare database connection
            self.conn = sqlite3.connect(defect_database.database_name)
            self.myCursor = self.conn.cursor()
            # get values search input of defect, road name
            self.defect_id_input = self.defect_id.get()
            self.defect_road_name_input = self.road_name.get()
            # search SQL
            select_sql = "Select * from defects where deleted_flag = 0 "
            # create SQL parameters
            parameters = []
            # check and add SQL condition to SQL where condition and parameters
            if self.defect_id_input != "":
                # defect id is input
                select_sql += " AND defect_id = ?"
                parameters += [self.defect_id_input]
            if self.defect_road_name_input:
                # road name is input 
                select_sql += " AND defect_road_name like ?"
                parameters += [self.defect_road_name_input]
            if self.search_status.get() != "" and self.search_status.get() != "all":
                # status value is input and not equal to all
                select_sql += " AND status = ?"
                parameters += [self.search_status.get()]
            if self.search_severity.get() != "" and self.search_severity.get() != "all":
                # severity value is input and not equal to all
                select_sql += " AND severity = ?"
                parameters += [self.search_severity.get()]
            if self.search_priority.get() != "" and self.search_priority.get() != "all":
                # priority value is input and not equal to all
                select_sql += " AND priority = ?"
                parameters += [self.search_priority.get()]

            # execute SQL to select data
            self.myCursor.execute(select_sql, parameters)
            # fecth all data
            self.pc = self.myCursor.fetchall()
            # if data is available
            if self.pc:
                # clear data from the list before fill in new data
                self.listTree.delete(*self.listTree.get_children())
                row_num = 1     # row number of the list
                # loop all records to add each row element to list cells
                for row in self.pc:
                    # add value to columns: defect_id, road_name, address, status, severity, priority, reported_date, fixed_date
                    self.listTree.insert("", 'end', text=row_num, values=(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]))
                    row_num += 1
            else:
                # messagebox.showinfo("Error", "No data found.")
                self.listTree.delete(*self.listTree.get_children())
        except Error:
            messagebox.showerror("Error", "Something Goes Wrong")

    def show_all_data(self):
        """Search data by defect id."""
        try:
            """ Create database connection."""
            self.conn = sqlite3.connect(defect_database.database_name)
            self.myCursor = self.conn.cursor()
            # Create SQL to select data
            self.myCursor.execute("SELECT * FROM defects WHERE deleted_flag = 0 ")
            self.pc = self.myCursor.fetchall()
            # Check if data exist
            if self.pc:
                # Clear all grid data
                self.listTree.delete(*self.listTree.get_children())
                row_num = 1
                # Fill data into list
                for row in self.pc:
                    # add value to columns: defect_id, road_name, address, status, severity, priority, reported_date, fixed_date
                    self.listTree.insert("", 'end', text=row_num, values=(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]))
                    # increase row number
                    row_num += 1
        except Error:
            messagebox.showerror("Error", "Something Goes Wrong")

    def setup_search_condition(self):
        """Generate the window upper section: search condition."""
        try:
            # Create database connection
            conn = sqlite3.connect(defect_database.database_name)
            mycursor = conn.cursor()
            # execute SQL to find existing data
            mycursor.execute("Select * from admin")
            admin_data = mycursor.fetchone()
            if not admin_data:
                messagebox.showinfo("Error", "Please Register A user")
                answer = messagebox.askyesno("Confirm", "Do you want to register a user?")
                if answer:
                    # close current window
                    self.destroy()
                    # open admin registration window
                    os.system('%s %s' % (py, 'admin/admin_user_reg.py'))
            else:   # admin user exists
                # label and input box
                self.label3 = Label(self, text='ASAP Defect List', bg='light blue', font=('Arial', 25, 'bold'))
                self.label3.place(x=450, y=40)
                # search defect id input field
                self.label4 = Label(self, text="Enter Defect ID", bg='light blue', font=('Arial', 12, 'bold'))
                self.label4.place(x=100, y=150)
                self.e1 = Entry(self, textvariable=self.defect_id, width=40)
                self.e1.place(x=350, y=150)
                # self.label5 = Label(self, text='OR', bg='light blue', font=('arial', 12, 'bold')).place(x=170, y=235)
                self.label5 = Label(self, text="Enter Road Name", bg='light blue', font=('Arial', 12, 'bold'))
                self.label5.place(x=100, y=190)
                
                # search road name input field
                Entry(self, textvariable=self.road_name, width=40).place(x=350, y=190)
                # status condition
                self.label_status = Label(self, text="Status", bg='light blue', font=('Arial', 12, 'bold'))
                self.label_status.place(x=660, y=150)
                # status radio button values
                self.radio_status_1 = Radiobutton(self, text="New", variable=self.search_status, value="new", bg='light blue')
                self.radio_status_1.place(x=760, y=150)
                self.radio_status_2 = Radiobutton(self, text="In progress", variable=self.search_status, value="in progress", bg='light blue')
                self.radio_status_2.place(x=840, y=150)
                self.radio_status_3 = Radiobutton(self, text="Done", variable=self.search_status, value="done", bg='light blue')
                self.radio_status_3.place(x=940, y=150)
                self.radio_status_all = Radiobutton(self, text="All", variable=self.search_status, value="all", bg='light blue')
                self.radio_status_all.place(x=1020, y=150)
                # radio button for severity
                self.label_severity = Label(self, text="Severity", bg='light blue', font=('Arial', 12, 'bold'))
                self.label_severity.place(x=660, y=190)
                # severity radio button values
                self.radio_severity_1 = Radiobutton(self, text="Critical", variable=self.search_severity, value="critical", bg='light blue')
                self.radio_severity_1.place(x=760, y=190)
                self.radio_severity_2 = Radiobutton(self, text="Major", variable=self.search_severity, value="major", bg='light blue')
                self.radio_severity_2.place(x=840, y=190)
                self.radio_severity_3 = Radiobutton(self, text="Minor", variable=self.search_severity, value="minor", bg='light blue')
                self.radio_severity_3.place(x=940, y=190)
                self.radio_severity_all = Radiobutton(self, text="All", variable=self.search_severity, value="all", bg='light blue')
                self.radio_severity_all.place(x=1020, y=190)
                # radio button for priority
                self.label_priority = Label(self, text="Priority", bg='light blue', font=('Arial', 12, 'bold'))
                self.label_priority.place(x=660, y=230)
                # value for priority
                self.radio_priority_1 = Radiobutton(self, text="High", variable=self.search_priority, value="high", bg='light blue')
                self.radio_priority_1.place(x=760, y=230)
                self.radio_priority_2 = Radiobutton(self, text="Medium", variable=self.search_priority, value="medium", bg='light blue')
                self.radio_priority_2.place(x=840, y=230)
                self.radio_priority_3 = Radiobutton(self, text="Low", variable=self.search_priority, value="low", bg='light blue')
                self.radio_priority_3.place(x=940, y=230)
                self.radio_priority_all = Radiobutton(self, text="All", variable=self.search_priority, value="all", bg='light blue')
                self.radio_priority_all.place(x=1020, y=230)

                # set default value to radio to all
                self.search_status.set("all")
                self.search_severity.set("all")
                self.search_priority.set("all")
                # search result list
                self.label6 = Label(self, text="Defect list", bg='light blue', font=('Arial', 13, 'bold'))
                self.label6.place(x=100, y=300)
                # search button, and bind click event on seach button to function search_defect
                Button(self, text='Search', width=15, font=('arial', 10), command=self.search_defect).place(x=1100, y=190)
                # edit button, bind the click event to open defect edit window
                Button(self, text='Edit', width=10, font=('Arial', 11), command=self.goto_defect_edit).place(x=1200, y=620)
                # delete button, bind the delete data function to click event
                Button(self, text='Delete', width=10, font=('Arial', 11), fg="red", command=self.delete_defect).place(x=1200, y=670)
        except Error:   # exception
            messagebox.showerror("Error", "Something Goes Wrong")

    def item_selected(self, event):
        """Handle a list item seleted then do some actions."""
        # loop the list item that are being selected
        for selected_item in self.listTree.selection():
            item = self.listTree.item(selected_item)
            # get selected row values
            record = item['values']
            # show photo by defect_id = record[0]
            self.show_photo(record[0])

    def show_photo(self, pic):
        """Show the defect photo which stored from database."""
        try:
            # Prepare database connection
            self.conn = sqlite3.connect(defect_database.database_name)
            self.mycursor = self.conn.cursor()
            # Query data from defects table by defect id
            self.mycursor.execute("Select * from defects where defect_id = ?", [pic])
            # Fetch one record
            data = self.mycursor.fetchone()

            if data[10]:    # check defects.image columns data exists
                # Define temporory image folder for showing image on windows
                photo_path = "defect_image_tmp/" + str(data[0]) + ".jpeg"
                # Write binary data to image file
                self.write_to_file(data[10], photo_path)
                # open image file
                defect_photo = Image.open(photo_path)
                # set image file to window image object
                self.photo = ImageTk.PhotoImage(defect_photo)
                # get file list in temporory folder
                filelist = glob.glob("defect_image_tmp/*.jpeg")
                # delete all jpeg file in this temporory folder
                for file in filelist:
                    os.remove(file)
            else:
                # display representative image if no image is stored in database
                self.photo = ImageTk.PhotoImage(Image.open("defect_image_tmp/noimage.png"))
            # set photo
            Label(image=self.photo, width=150, height=100).place(x=1180, y=360)

        except Error:
            messagebox.showerror("Error", "Something goes wrong")

    def write_to_file(self, data, filename):
        """Write image data to file."""
        with open(filename, 'wb') as file:
            file.write(data)

    def goto_defect_edit(self):
        """Go to defect edit screen."""
        for selected_item in self.listTree.selection():
            # get selected item
            item = self.listTree.item(selected_item)
            # get seleted item data
            record = item['values']
            # open edit defect window with selected defect id
            os.system('%s %s %s' % (py, 'defect/edit_defect.py', record[0]))
        # call show data by previously selected condition
        self.search_defect()

    def delete_defect(self):
        """Do show a confirmation and delete a defect record."""
        for selected_item in self.listTree.selection():
            item = self.listTree.item(selected_item)
            record = item['values']

            answer = messagebox.askyesno("Confirm", "Do you want to delete this defect information?")
            if answer:
                try:
                    # prepare parametter
                    parameters = [record[0]]
                    query = """ UPDATE defects SET deleted_flag = 1 WHERE defect_id = ? """
                    # prepare database connection
                    self.conn = sqlite3.connect("defect_management.db")
                    self.myCursor = self.conn.cursor()
                    # execute update data
                    self.myCursor.execute(query, parameters)
                    # commit transaction and close db connection
                    self.conn.commit()
                    self.myCursor.close()
                    self.conn.close()
                    # call load newest data with current search condition
                    self.search_defect()
                except Error:
                    messagebox.showerror("Error", "Something Goes Wrong")


# main loop this windows
HomeWindow().mainloop()