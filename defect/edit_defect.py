from tkinter import *
from tkinter import messagebox
import re
from tkinter import ttk
import sqlite3
from sqlite3 import Error
import os,sys, glob
from types import NoneType
from tkcalendar import DateEntry
from PIL import ImageTk,Image

# from database import lms_database
py=sys.executable

#creating window
class edit_defect(Tk):
    def __init__(self,defect_id=None):
        
        super().__init__()
        # top = Toplevel()
        # self = Frame(top)
        # self.update = update
        #
        print(sys.argv[1])
        if sys.argv[1]!= None:
            defect_id = sys.argv[1]
            
        self.title("Defect Management")
        self.maxsize(1366, 768)
        self.minsize(1366, 768)
        self.state("zoomed")
        self.iconbitmap(r'images/defect.ico')
        self.configure(bg='light blue')
        #creating variables Please chech carefully
        self.defect_id = StringVar()
        self.defect_road_name = StringVar()
        self.defect_address = StringVar()
        self.status = StringVar()
        self.severity = StringVar()
        self.priority = StringVar()
        self.reported_date = StringVar()
        self.fixed_date = StringVar()
        self.defect_photo = StringVar()
        
        self.create_tree_widget()
       
        self.get_defect_data(defect_id)

    def update_data(self):
        try:
            # lms_db = lms_database()
            self.conn = sqlite3.connect("defect_management.db")
            self.myCursor = self.conn.cursor()
            #get descritop from text field
            description_value = self.defect_description.get("1.0","end-1c")
            # print(inputValue)
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
                          self.defect_id.get()
                          ]
            print(parameters)
            # parameters = [1, '213', 'ada', 'aD', 'ad', 'aDa', None , None ]
            query = """ UPDATE defects
                SET defect_road_name = ?,
                defect_address = ?,
                status = ?,
                severity = ?,
                priority = ?,
                reported_date = ?,
                fixed_date = ?,
                description = ?
                WHERE defect_id = ? """
            print(query)
            c = self.myCursor.execute(query, parameters)
           
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
            
    # verify input
    def verify(self):
        
        
        # if len(self.defect_id.get()) == 0:
        #     messagebox.showinfo("Error","Please enter defect id")
        # el
        if len(self.defect_road_name.get()) == 0:
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
            self.update_data()
                
    def create_tree_widget(self):   
        # form title text 
        # input_form = self
        # self = Frame(self, width=700, height=500, bg="light blue").place(x=370, y=200)
        Label(self,text="Update defect information",font=("Arial",35,'bold'),bg="light blue").place(x=480,y=80)
        # input form lable
        Label(self, text="Defect ID", font=("Arial", 13, "bold"), bg="light blue").place(x=420, y=220)
        Label(self, text="Road Name", font=("Arial", 13, "bold"), bg="light blue").place(x=420, y=260)
        Label(self, text="Road Address", font=("Arial", 13, "bold"), bg="light blue").place(x=420, y=300)
        Label(self, text="Status", font=("Arial", 13, "bold"), bg="light blue").place(x=420, y=340)
        Label(self, text="Severity", font=("Arial", 13, "bold"), bg="light blue").place(x=420, y=380)
        Label(self, text="Rriority", font=("Arial", 13, "bold"), bg="light blue").place(x=420, y=420)
        Label(self, text="Reported date", font=("Arial", 13, "bold"), bg="light blue").place(x=420, y=460)
        Label(self, text="Fixed date", font=("Arial", 13, "bold"), bg="light blue").place(x=420, y=500)
        Label(self, text="Description", font=("Arial", 13, "bold"), bg="light blue").place(x=420, y=540)
        test_lable = Label(self, text="test", font=("Arial", 13, "bold"), bg="light blue")
        Label(self,text="Upload image", font=('Arial', 13, 'bold'),bg="light blue").place(x=420,y=630)
        # input text field for defect id, road name, address
        # Entry(input_form, textvariable=self.defect_id, width=60).place(x=620,y=260)
        self.defect_id_input = Entry(self, textvariable=self.defect_id, width=60, state="readonly", readonlybackground="light gray")
        # self.defect_id_input.pack()
        self.defect_id_input.place(x=620,y=220)
        Entry(self, textvariable=self.defect_road_name, width=60).place(x=620, y=260)
        Entry(self, textvariable=self.defect_address, width=60).place(x=620, y=300)
        
        # combo box for status, serverity and priority
        ttk.Combobox(self,textvariable=self.status,values=["new","in progress","done"],width=57,state="readonly").place(x = 620, y = 340)
        ttk.Combobox(self,textvariable=self.severity,values=["critical","major","minor"],width=57,state="readonly").place(x = 620, y = 380)
        ttk.Combobox(self,textvariable=self.priority,values=["high","medium","low"],width=57,state="readonly").place(x = 620, y = 420)
        
        # Entry(self, textvariable=self.severity, width=60).place(x=620, y=420)
        # Entry(self, textvariable=self.priority, width=60).place(x=620, y=460)
        cal1 =DateEntry(self,selectmode='day', textvariable = self.reported_date, width=20)
        cal1.place(x=620, y=460)
        
        Button(self,text="clear", width=8, font=("Arial", 9), command=lambda:cal1.delete(0,'end')).place(x=780, y=460)
        
        cal2 = DateEntry(self,selectmode='day', textvariable = self.fixed_date, width=20)
        cal2.place(x=620, y=500)
        Button(self, text="clear", width=8, font=("Arial", 9), command=lambda:cal2.delete(0,'end')).place(x=780, y=500)
        
        
        # description field
        # Create text widget and specify size.
        self.defect_description = Text(self, height = 4, width = 47)
        self.defect_description.place(x=620, y=540)
        # photo upload area
        upload_image = Entry(self,textvariable = self.defect_photo,width = 50).place(x=620,y=630)
        butt=Button(self,text="Browse",width=7,command=self.open_file_dialog).place(x=940,y=628)
        
        # Entry(self, textvariable=self.reported_date, width=60).place(x=620, y=500)
        # Entry(self, textvariable=self.fixed_date, width=60).place(x=620, y=540)
        Button(self, text="Save", width=10, font=("Arial", 13, "bold"), command=self.verify).place(x=560, y=670)
        Button(self, text="Cancel", width=10, font=("Arial", 13, "bold"),command=self.close).place(x=720, y=670)
    
    def get_defect_data(self, defect_id):
        """Get data from database."""
        self.conn = sqlite3.connect("defect_management.db")
        self.myCursor = self.conn.cursor()
        self.myCursor.execute("Select * from defects where defect_id =? ", [defect_id])
        self.defect_data = self.myCursor.fetchall()
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
                self.defect_description.insert("1.0",data_item[8])
                
            # show photo if it is set in database
            # if(data_item[10]!=None):
            self.show_photo(defect_id)
                
    def open_file_dialog(self):
        """File open dialog photo."""
        filename = filedialog.askopenfilename(initialdir = "/",title = "Select a photo",filetype = (("jpeg","*.jpg"),("png","*.png"),("All Files","*.*")))
        self.defect_photo.set(filename)
            
    def convert_to_binary_data(self,filename):
        """Convert photo into binary data."""
        with open(filename, 'rb') as file:
            blobData = file.read()
        return blobData
    
    def show_photo(self, pic):
            try:
                self.conn = sqlite3.connect("defect_management.db")
                self.mycursor = self.conn.cursor()
                self.mycursor.execute("Select * from defects where defect_id = ?", [pic])
                pc = self.mycursor.fetchone()
                if pc[10]: # check defects.image columns data exists
                    # print("Image",pc[10])
                    photoPath = "defect_image_tmp/" + str(pc[0]) + ".jpeg"
                    self.write_to_file(pc[10], photoPath)
                    defect_photo = Image.open("defect_image_tmp/" + str(pc[0]) + ".jpeg")
                    self.photo = ImageTk.PhotoImage(defect_photo)
                    filelist = glob.glob("defect_image_tmp/*.jpeg")
                    for file in filelist:
                        os.remove(file)
                else:
                    self.photo = ImageTk.PhotoImage(Image.open("defect_image_tmp/noimage.png"))
                # set photo
                Label(image=self.photo, width=150, height=100).place(x=1180, y=450)
            except Error:
                messagebox.showerror("Error", "Something goes wrong")
                
    def write_to_file(self, data, filename):
            with open(filename,'wb') as file:
                file.write(data)
                
edit_defect().mainloop()