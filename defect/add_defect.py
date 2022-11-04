"""Add Defect Window."""
from tkinter import *
from tkinter import messagebox
from tkinter import ttk, Tk
from tkcalendar import DateEntry
from tkinter import filedialog
import sqlite3
from sqlite3 import Error
import os, sys

py = sys.executable


class add_defect(Tk):
    """Add Defect Window Class."""

    def __init__(self):
        """Class constructor."""
        super().__init__()
        # window title
        self.title("Defect Management")
        # setup window size
        self.maxsize(1366, 768)
        self.minsize(1366, 768)
        # zoom to maximize window
        self.state("zoomed")
        # set window icon
        self.iconbitmap(r'images/defect.ico')
        # set window background
        self.configure(background="light blue")
        # creating variables that input on form
        self.defect_id = StringVar()
        self.defect_road_name = StringVar()
        self.defect_address = StringVar()
        self.status = StringVar()
        self.severity = StringVar()
        self.priority = StringVar()
        self.reported_date = StringVar()
        self.fixed_date = StringVar()
        self.defect_photo = StringVar()
        # create window form widget
        self.create_window_form_widget()

    def insert(self):
        """Do insert new defect."""
        try:
            # prepare database connection
            self.conn = sqlite3.connect("defect_management.db")
            self.myCursor = self.conn.cursor()
            # get descritop from text field
            description_value = self.defect_description.get("1.0", "end-1c")
            # print(inputValue)
            parameters = [
                          self.defect_road_name.get(),
                          self.defect_address.get(),
                          self.status.get(),
                          self.severity.get(),
                          self.priority.get(),
                          self.reported_date.get(),
                          self.fixed_date.get(),
                          description_value,
                          '0',  # delete_flag = 0 by default
                          self.convert_to_binary_data(self.defect_photo.get())
                          ]
            # execute SQL to insert data
            execute_result = self.myCursor.execute("Insert into defects(defect_road_name,defect_address,status,severity,priority,reported_date,fixed_date,description,deleted_flag,image) values (?,?,?,?,?,?,?,?,?,?)", parameters)
            # commit database change
            self.conn.commit()
            # close data cursor
            self.myCursor.close()
            # close connection
            self.conn.close()
            if execute_result:  # successfully inserted
                # show message box
                messagebox.showinfo("Confirm", "Data Inserted Successfully")
                # close window
                self.destroy()
                # transit to  home page
                os.system('%s %s' % (py, 'home.py'))
        except Error:
            # show message if any exceptional error
            messagebox.showinfo("Error", "Something Goes Wrong")

    def close(self):
        """Go back to main."""
        self.destroy()

    def verify_input(self):
        """Do data validation."""
        if len(self.defect_road_name.get()) == 0:
            messagebox.showinfo("Error", "Please input road name")
        elif len(self.defect_address.get()) == 0:
            messagebox.showinfo("Error", "Please input defect address")
        elif len(self.status.get()) == 0:
            messagebox.showinfo("Error", "Please input status")
        elif len(self.severity.get()) == 0:
            messagebox.showinfo("Error", "Please input severity")
        elif len(self.reported_date.get()) == 0:
            messagebox.showinfo("Error", "Please input reported date")
        else:   # validation passed
            # insert data
            self.insert()

    def create_window_form_widget(self):
        """Generate form widget."""
        # form title text
        Label(self, text="New defect entry", font=("Arial", 35, 'bold'), bg="light blue").place(x=480, y=80)
        # input form lable
        Label(self, text="Road Name", font=("Arial", 13, "bold"), bg="light blue").place(x=420, y=260)
        Label(self, text="Road Address", font=("Arial", 13, "bold"), bg="light blue").place(x=420, y=300)
        Label(self, text="Status", font=("Arial", 13, "bold"), bg="light blue").place(x=420, y=340)
        Label(self, text="Severity", font=("Arial", 13, "bold"), bg="light blue").place(x=420, y=380)
        Label(self, text="Priority", font=("Arial", 13, "bold"), bg="light blue").place(x=420, y=420)
        Label(self, text="Reported date", font=("Arial", 13, "bold"), bg="light blue").place(x=420, y=460)
        Label(self, text="Description", font=("Arial", 13, "bold"), bg="light blue").place(x=420, y=540)
        Label(self, text="Upload image", font=('Arial', 13, 'bold'), bg="light blue").place(x=420, y=630)
        # input text field for road name, address
        Entry(self, textvariable=self.defect_road_name, width=60).place(x=620, y=260)
        Entry(self, textvariable=self.defect_address, width=60).place(x=620, y=300)
        # combo box for status, serverity and priority
        ttk.Combobox(self, textvariable=self.status, values=["new"], width=57, state="readonly").place(x=620, y=340)
        ttk.Combobox(self, textvariable=self.severity, values=["critical", "major", "minor"], width=57, state="readonly").place(x=620, y=380)
        ttk.Combobox(self, textvariable=self.priority, values=["high", "medium", "low"], width=57,state="readonly").place(x=620, y=420)
        # force status = new for new defect
        self.status.set("new")
        # reported date input by calendar
        cal_reported_date =DateEntry(self, selectmode='day', textvariable=self.reported_date, width=20)
        cal_reported_date.place(x=620, y=460)
        # A clear button to clear input date because tkinter DateEntry cannot clear its date
        Button(self, text="clear", width=8, font=("Arial", 9), command=lambda: cal_reported_date.delete(0, 'end')).place(x=780, y=460)
        # description field by a text area, create text widget and specify size.
        self.defect_description = Text(self, height=4, width=47)
        self.defect_description.place(x=620, y=540)
        # photo upload area
        Entry(self, textvariable=self.defect_photo, width=50).place(x=620, y=630)
        Button(self, text="Browse", width=7, command=self.open_file_dialog).place(x=940, y=628)
        # save button
        Button(self, text="Save", width=10, font=("Arial", 13, "bold"), command=self.verify_input).place(x=620, y=670)
        # cancel button
        Button(self, text="Cancel", width=10, font=("Arial", 13, "bold"), command=self.close).place(x=780, y=670)

    def open_file_dialog(self):
        """File open dialog photo."""
        filename = filedialog.askopenfilename(initialdir="/", title="Select a photo", filetype=(("jpeg", "*.jpeg"), ("png", "*.png"), ("All Files", "*.*")))
        self.defect_photo.set(filename)

    def convert_to_binary_data(self, filename):
        """Convert photo into binary data."""
        if filename != '':
            with open(filename, 'rb') as file:
                blobData = file.read()
            return blobData
        else:
            return None


# do main loop for this window
add_defect().mainloop()