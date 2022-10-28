from tkinter import *
from tkinter import messagebox
from tkinter.messagebox import showinfo

import sqlite3
from sqlite3 import Error
import os
import sys
from tkinter import ttk
from database.defect_database import defect_database


py=sys.executable

#creating window
class HomeWindow(Tk):
    def __init__(self):
        super().__init__()
        self.iconbitmap(r'images/defect.ico')
        self.configure(bg='light blue')
        self.maxsize(1366, 768)
        self.minsize(1366, 768)
        self.state('zoomed')
        self.title('Defect Management - Home')
        # search value
        self.defect_id = StringVar()
        self.road_name = StringVar()
        self.search_status = StringVar()
        self.search_severity = StringVar()
        self.search_priority = StringVar()
        # menu setup
        self.mymenu = Menu(self)
        # setup_search_condition
        self.setup_search_condition()
        # generate grid layout
        self.create_tree_widget()
        # load data to list
        self.show_all_data()
    #calling scripts
    def add_defect(self):
        os.system('%s %s' % (py, 'defect/add_defect.py'))

    def add_user(self):
        os.system('%s %s' % (py, 'admin/admin_user_reg.py'))
        
    def create_tree_widget(self):
        #creating table
        data_columns = ('defect_id', 'defect_road_name', 'defect_address','status','severity','priority','reported_date','fixed_date')
        # define headings
        self.listTree = ttk.Treeview(self,height=13,columns=data_columns)
        self.vsb = ttk.Scrollbar(self,orient="vertical",command=self.listTree.yview)
        self.hsb = ttk.Scrollbar(self,orient="horizontal",command=self.listTree.xview)
        
        # test tree view
        self.listTree.heading("#0",text='#',anchor = 'center')
        self.listTree.heading('defect_id', text='defect id')
        self.listTree.heading('defect_road_name', text='Road name')
        self.listTree.heading('defect_address', text='Address')
        self.listTree.heading('status', text='Status')
        self.listTree.heading('severity', text='Severity')
        self.listTree.heading('priority', text='Priority')
        self.listTree.heading('reported_date', text='Reported date')
        self.listTree.heading('fixed_date', text='Fixed date')
        
        # heading size
        self.listTree.column("#0",width=50,minwidth=50,anchor='center')
        self.listTree.column("defect_id",width=100,minwidth=100,anchor='center')
        self.listTree.column("defect_road_name",width=200,minwidth=200,anchor='center')
        self.listTree.column("defect_address",width=200,minwidth=200,anchor='center')
        self.listTree.column("status",width=100,minwidth=100,anchor='center')
        self.listTree.column("severity",width=100,minwidth=100,anchor='center')
        self.listTree.column("priority",width=100,minwidth=100,anchor='center')
        self.listTree.column("reported_date",width=100,minwidth=100,anchor='center')
        self.listTree.column("fixed_date",width=100,minwidth=100,anchor='center')
        self.listTree.bind("<ButtonRelease-1>",self.item_selected)

        self.listTree.place(x=90,y=400)
        self.vsb.place(x=1142,y=400,height=287)
        self.hsb.place(x=91,y=687,width=1050)
        
        ttk.Style().configure("Treeview",font=('Arial',10))

        list1 = Menu(self)
        list1.add_command(label="Add Defects", command=self.add_defect)
            

        list2 = Menu(self)
        list2.add_command(label = "Add User",command = self.add_user)
        

        self.mymenu.add_cascade(label='Defects', menu=list1)
        
        self.mymenu.add_cascade(label = 'Admin Tools', menu = list2)

        self.config(menu=self.mymenu)

    def search_defect(self):
        """Search data by defect id."""
        
        try:
            self.conn = sqlite3.connect(defect_database.database_name)
            self.myCursor = self.conn.cursor()
            self.defect_id_input = self.defect_id.get()
            self.defect_road_name_input = self.road_name.get()
            status_radio = self.search_status.get()
            print("status",status_radio)
            select_sql = "Select * from defects where deleted_flag = 0 "
            parameters =[]
            # check search input
            if self.defect_id_input !="":
                select_sql += " AND defect_id = ?"
                parameters += [self.defect_id_input]
            if self.defect_road_name_input:
                select_sql += " AND defect_road_name like ?"
                parameters += [self.defect_road_name_input]
            if self.search_status.get() != "" and self.search_status.get() != "all":
                select_sql += " AND status = ?"
                parameters += [self.search_status.get()]
            if self.search_severity.get() != "" and self.search_severity.get() != "all":
                select_sql += " AND severity = ?"
                parameters += [self.search_severity.get()]
            if self.search_priority.get() != "" and self.search_priority.get() != "all":
                select_sql += " AND priority = ?"
                parameters += [self.search_priority.get()]
                
            print(select_sql)
            print(parameters)
            self.myCursor.execute(select_sql,parameters)
            self.pc = self.myCursor.fetchall()
            if self.pc:
                self.listTree.delete(*self.listTree.get_children())
                row_num = 1
                for row in self.pc:
                    print(row)
                    self.listTree.insert("",'end',text=row_num ,values = (row[0], row[1],row[2],row[3],row[4],row[5],row[6],row[7]))
                    row_num +=1
            else:
                # messagebox.showinfo("Error", "Either Defect ID is wrong or the road name is not yet exist.")
                self.listTree.delete(*self.listTree.get_children())
        except Error:
            messagebox.showerror("Error","Something Goes Wrong")
    
    def show_all_data(self):
        """Search data by defect id."""
        
        try:
            self.conn = sqlite3.connect(defect_database.database_name)
            self.myCursor = self.conn.cursor()
            
            self.myCursor.execute("SELECT * FROM defects WHERE deleted_flag = 0 ")
            self.pc = self.myCursor.fetchall()
            if self.pc:
                self.listTree.delete(*self.listTree.get_children())
                row_num = 1
                for row in self.pc:
                    self.listTree.insert("",'end',text=row_num ,values = (row[0], row[1],row[2],row[3],row[4],row[5],row[6],row[7]))
                    row_num +=1
            # else:
            #     messagebox.showinfo("Error", "Either Defect ID is wrong or the road name is not yet exist.")
        except Error:
            messagebox.showerror("Error","Something Goes Wrong")

    def setup_search_condition(self):
        try:
            conn = sqlite3.connect(defect_database.database_name)
            mycursor = conn.cursor()
            mycursor.execute("Select * from admin")
            z = mycursor.fetchone()
            if not z:
                messagebox.showinfo("Error", "Please Register A user")
                x = messagebox.askyesno("Confirm","Do you want to register a user?")
                if x:
                    self.destroy()
                    os.system('%s %s' % (py, 'admin/admin_user_reg.py'))
            else:
                #label and input box
                self.label3 = Label(self, text='ASAP Defect List', bg='light blue', font=('Arial', 30, 'bold'))
                self.label3.place(x=450, y=40)
                # search defect id input field
                self.label4 = Label(self, text="Enter Defect ID", bg='light blue', font=('Arial', 12, 'bold'))
                self.label4.place(x=100, y=150)
                self.e1 = Entry(self, textvariable=self.defect_id, width=40).place(x=350, y=150)
                # self.label5 = Label(self, text='OR', bg='light blue', font=('arial', 12, 'bold')).place(x=170, y=235)
                self.label5 = Label(self, text="Enter Road Name", bg='light blue', font=('Arial', 12, 'bold'))
                self.label5.place(x=100, y=190)
                
                # search road name input field
                self.e2 = Entry(self, textvariable=self.road_name, width=40).place(x=350, y=190)
                # status condition
                self.label_status = Label(self, text="Status", bg='light blue', font=('Arial', 12, 'bold'))
                self.label_status.place(x=660, y=150)
                self.radio_status_1 = Radiobutton(self, text="New", variable=self.search_status, value="new",bg='light blue')
                self.radio_status_1.place(x=760, y=150)
                self.radio_status_2 = Radiobutton(self, text="In progress", variable=self.search_status, value="in progress",bg='light blue')
                self.radio_status_2.place(x=840, y=150)
                self.radio_status_3 = Radiobutton(self, text="Done", variable=self.search_status, value="done",bg='light blue')
                self.radio_status_3.place(x=940, y=150)
                self.radio_status_all = Radiobutton(self, text="All", variable=self.search_status, value="all",bg='light blue')
                self.radio_status_all.place(x=1020, y=150)
                # radio button for severity
                self.label_severity = Label(self, text="Severity", bg='light blue', font=('Arial', 12, 'bold'))
                self.label_severity.place(x=660, y=190)
                self.radio_severity_1 = Radiobutton(self, text="Critical", variable=self.search_severity, value="critical",bg='light blue')
                self.radio_severity_1.place(x=760, y=190)
                self.radio_severity_2 = Radiobutton(self, text="Major", variable=self.search_severity, value="major",bg='light blue')
                self.radio_severity_2.place(x=840, y=190)
                self.radio_severity_3 = Radiobutton(self, text="Minor", variable=self.search_severity, value="minor",bg='light blue')
                self.radio_severity_3.place(x=940, y=190)
                self.radio_severity_all = Radiobutton(self, text="All", variable=self.search_severity, value="all",bg='light blue')
                self.radio_severity_all.place(x=1020, y=190)
                # radio button for priority
                self.label_priority = Label(self, text="Priority", bg='light blue', font=('Arial', 12, 'bold'))
                self.label_priority.place(x=660, y=230)
                self.radio_priority_1 = Radiobutton(self, text="High", variable=self.search_priority, value="high",bg='light blue')
                self.radio_priority_1.place(x=760, y=230)
                self.radio_priority_2 = Radiobutton(self, text="Medium", variable=self.search_priority, value="medium",bg='light blue')
                self.radio_priority_2.place(x=840, y=230)
                self.radio_priority_3 = Radiobutton(self, text="Low", variable=self.search_priority, value="low",bg='light blue')
                self.radio_priority_3.place(x=940, y=230)
                self.radio_priority_all = Radiobutton(self, text="All", variable=self.search_priority, value="all",bg='light blue')
                self.radio_priority_all.place(x=1020, y=230)
                
                #set default value to radio to all
                self.search_status.set("all")
                self.search_severity.set("all")
                self.search_priority.set("all")
                # search result list
                # self.brt = Button(self, text='Find', width=15, font=('arial', 10),command = search_by_road_name).place(x=700, y=266)
                self.label6 = Label(self, text="Details", bg='light blue', font=('Arial', 12, 'underline', 'bold'))
                self.label6.place(x=100, y=350)
                # search button
                self.srt = Button(self, text='Search', width=15, font=('arial', 10),command = self.search_defect).place(x=700, y=280)
                # edit button 
                self.button = Button(self, text='Edit', width=10, font=('Arial', 11), command=self.goto_defect_edit).place(x=1200,y=500)
                
        except Error:
            messagebox.showerror("Error", "Something Goes Wrong")
                
    def item_selected(self,event):
        """Data is seleted then do some actions."""
        for selected_item in self.listTree.selection():
            item = self.listTree.item(selected_item)
            record = item['values']
            # show a message
            # self.showinfo(title='Information', message=','.join(record))
            print(type(record))
            # a = ','.join(str(record))
            print(repr(tuple(record)))
            # showinfo(title='Information', message=repr(tuple(record)))
            
    def goto_defect_edit(self):
        for selected_item in self.listTree.selection():
            item = self.listTree.item(selected_item)
            record = item['values']
            # showinfo(title='Information', message=repr(tuple(record)))
            print(record[0])
            os.system('%s %s %s' % (py, 'defect/edit_defect.py',record[0]))
            
        # setup_search_condition()
        self.search_defect()
    
    
    
HomeWindow().mainloop()