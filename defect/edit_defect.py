"""Edit defect info window."""

from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import sqlite3
from sqlite3 import Error
import os, sys, glob
from types import NoneType
from tkcalendar import DateEntry
from PIL import ImageTk, Image
from tkinter import filedialog
# from database import lms_database
py=sys.executable

class edit_defect(Tk):
    """Edit Defect Window Class."""
    def __init__(self, defect_id=None):
        """Class constructor."""
        super().__init__()
        # get commandline argument to find passed defect id
        if sys.argv[1]!= None:
            defect_id = sys.argv[1]
        # set window title
        self.title("Defect Management - Edit Defect")
        # set screen properties
        self.maxsize(1366, 768)
        self.minsize(1366, 768)
        # zoom to maximize size
        self.state("zoomed")
        # show window icon
        self.iconbitmap(r'images/defect.ico')
        # set background color
        self.configure(bg='light blue')
        # creating variables
        self.defect_id = StringVar()
        self.defect_road_name = StringVar()
        self.defect_address = StringVar()
        self.status = StringVar()
        self.severity = StringVar()
        self.priority = StringVar()
        self.reported_date = StringVar()
        self.fixed_date = StringVar()
        self.defect_photo = StringVar()
        # generate gui input
        self.create_window_widget()
        # show defect data by given id
        self.get_defect_data(defect_id)

    def update_data(self):
        """Update defect info."""
        try:
            # prepare database connection
            self.conn = sqlite3.connect("defect_management.db")
            self.myCursor = self.conn.cursor()
            # get descritop from text field
            description_value = self.defect_description.get("1.0", "end-1c")
            # get photo data
            photo = self.defect_photo.get()
            if photo != '':     # photo element is set
                binary_photo = self.convert_to_binary_data(photo)
            else:
                binary_photo = self.old_photo
            parameters = [
                        # self.defect_id.get(),
                          self.defect_road_name.get(),
                          self.defect_address.get(),
                          self.status.get(),
                          self.severity.get(),
                          self.priority.get(),
                          self.reported_date.get(),
                          self.fixed_date.get(),
                          description_value,
                          binary_photo,
                        #   self.convert_to_binary_data(self.defect_photo.get()),
                          self.defect_id.get()
                          ]
            # print(parameters)
            # parameters = [1, '213', 'ada', 'aD', 'ad', 'aDa', None , None ]
            query = """ UPDATE defects
                SET defect_road_name = ?,
                defect_address = ?,
                status = ?,
                severity = ?,
                priority = ?,
                reported_date = ?,
                fixed_date = ?,
                description = ?,
                image = ?
                WHERE defect_id = ? """
            # print(query)
            c = self.myCursor.execute(query, parameters)
            # commit and close cursor, connection
            self.conn.commit()
            self.myCursor.close()
            self.conn.close()
            if c:
                messagebox.showinfo("Confirm", "Data Updated Successfully")
                # self.destroy()
                # os.system('%s %s' % (py, 'main.py'))
        except Error:
            print(Error)
            messagebox.showinfo("Error", "Something Goes Wrong")

    def close(self):
        """Go back to main."""
        self.destroy()
        # os.system('%s %s' % (py, 'home.py'))

    def verify_input(self):
        """Verify defect input."""

        if len(self.defect_road_name.get()) == 0:   # road name is blank
            messagebox.showinfo("Error", "Please input road name")
        elif len(self.defect_address.get()) == 0:   # road address is blank
            messagebox.showinfo("Error", "Please input defect address")
        elif len(self.status.get()) == 0:   # road status is blank
            messagebox.showinfo("Error", "Please input status")
        elif len(self.severity.get()) == 0:   # severity is blank
            messagebox.showinfo("Error", "Please input severity")
        elif len(self.reported_date.get()) == 0:   # reported date is blank
            messagebox.showinfo("Error", "Please input reported date")
        else:   # validation passed
            # do update data
            self.update_data()

    def create_window_widget(self):
        # form title text 
        Label(self, text="Update defect information", font=("Arial", 35, 'bold'), bg="light blue").place(x=480, y=80)
        # input form lable
        Label(self, text="Defect ID", font=("Arial", 13, "bold"), bg="light blue").place(x=420, y=220)
        Label(self, text="Road Name", font=("Arial", 13, "bold"), bg="light blue").place(x=420, y=260)
        Label(self, text="Road Address", font=("Arial", 13, "bold"), bg="light blue").place(x=420, y=300)
        Label(self, text="Status", font=("Arial", 13, "bold"), bg="light blue").place(x=420, y=340)
        Label(self, text="Severity", font=("Arial", 13, "bold"), bg="light blue").place(x=420, y=380)
        Label(self, text="Priority", font=("Arial", 13, "bold"), bg="light blue").place(x=420, y=420)
        Label(self, text="Reported date", font=("Arial", 13, "bold"), bg="light blue").place(x=420, y=460)
        Label(self, text="Fixed date", font=("Arial", 13, "bold"), bg="light blue").place(x=420, y=500)
        Label(self, text="Description", font=("Arial", 13, "bold"), bg="light blue").place(x=420, y=540)
        test_lable = Label(self, text="test", font=("Arial", 13, "bold"), bg="light blue")
        Label(self, text="Upload image", font=('Arial', 13, 'bold'), bg="light blue").place(x=420, y=630)
        # input text field for defect id, road name, address
        # Entry(input_form, textvariable=self.defect_id, width=60).place(x=620,y=260)
        self.defect_id_input = Entry(self, textvariable=self.defect_id, width=60, state="readonly", readonlybackground="light gray")
        # self.defect_id_input.pack()
        self.defect_id_input.place(x=620, y=220)
        Entry(self, textvariable=self.defect_road_name, width=60).place(x=620, y=260)
        Entry(self, textvariable=self.defect_address, width=60).place(x=620, y=300)

        # combo box for status, serverity and priority
        ttk.Combobox(self, textvariable=self.status, values=["new", "in progress", "done"], width=57, state="readonly").place(x=620, y=340)
        ttk.Combobox(self, textvariable=self.severity, values=["critical", "major", "minor"], width=57, state="readonly").place(x=620, y=380)
        ttk.Combobox(self, textvariable=self.priority, values=["high", "medium", "low"], width=57, state="readonly").place(x=620, y=420)

        # Entry(self, textvariable=self.severity, width=60).place(x=620, y=420)
        # Entry(self, textvariable=self.priority, width=60).place(x=620, y=460)
        cal1 =DateEntry(self, selectmode='day', textvariable = self.reported_date, width=20)
        cal1.place(x=620, y=460)

        Button(self, text="clear", width=8, font=("Arial", 9), command=lambda: cal1.delete(0, 'end')).place(x=780, y=460)

        cal2 = DateEntry(self, selectmode='day', textvariable = self.fixed_date, width=20)
        cal2.place(x=620, y=500)
        Button(self, text="clear", width=8, font=("Arial", 9), command=lambda: cal2.delete(0, 'end')).place(x=780, y=500)
        # description field
        # Create text widget and specify size.
        self.defect_description = Text(self, height = 4, width = 47)
        self.defect_description.place(x=620, y=540)
        # photo upload area
        upload_image = Entry(self, textvariable=self.defect_photo, width=50).place(x=620, y=630)
        butt = Button(self, text="Browse", width=7, command=self.open_file_dialog).place(x=940, y=628)
        # button save
        Button(self, text="Save", width=10, font=("Arial", 13, "bold"), command=self.verify_input).place(x=620, y=670)
        # button cancel
        Button(self, text="Cancel", width=10, font=("Arial", 13, "bold"), command=self.close).place(x=780, y=670)

    def get_defect_data(self, defect_id):
        """Get data from database."""
        # create db connection
        self.conn = sqlite3.connect("defect_management.db")
        self.myCursor = self.conn.cursor()
        # query data
        self.myCursor.execute("Select * from defects where defect_id =? ", [defect_id])
        # fetch all data
        self.defect_data = self.myCursor.fetchall()
        # close cursor and connection
        self.myCursor.close()
        self.conn.close()

        if self.defect_data:
            # if data exist, pick first row from data records
            data_item = self.defect_data[0]
            # set the value to screen's elements
            self.defect_id.set(data_item[0])
            self.defect_road_name.set(data_item[1])
            self.defect_address.set(data_item[2])
            self.status.set(data_item[3])
            self.severity.set(data_item[4])
            self.priority.set(data_item[5])
            self.reported_date.set(data_item[6])
            self.fixed_date.set(data_item[7])
            # set description text area data
            if(data_item[8]!=None):
                self.defect_description.insert("1.0", data_item[8])
            # show photo if it is set in database
            # if(data_item[10]!=None):
            self.old_photo = data_item[10]  # store all photo info
            self.show_photo(defect_id)

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

    def show_photo(self, pic):
        """This function is to show the defect photo from DB."""
        try:
            # Prepare database connection
            self.conn = sqlite3.connect("defect_management.db")
            self.mycursor = self.conn.cursor()
            # Query data from defects table by defect id
            self.mycursor.execute("Select * from defects where defect_id = ?", [pic])
            # Fetch one record
            data = self.mycursor.fetchone()
            if data[10]: # check defects.image columns data exists
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
                self.photo = ImageTk.PhotoImage(Image.open("defect_image_tmp/noimage.png"))
            # set photo
            Label(image=self.photo, width=300, height=200).place(x=20, y=220)
        except Error:
            messagebox.showerror("Error", "Something goes wrong")

    def write_to_file(self, data, filename):
        """Write image data to file."""
        with open(filename, 'wb') as file:
            file.write(data)


# main loop this window
edit_defect().mainloop()