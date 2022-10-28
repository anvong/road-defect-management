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
        self.defect_id = StringVar()
        self.road_name = StringVar()
        self.mymenu = Menu(self)
        self.check()
        self.create_tree_widget()
        # self.show_all_data()
    #calling scripts
    def add_defect(self):
        os.system('%s %s' % (py, 'add_defect.py'))

        

        # def handle(event):
        #     if self.listTree.identify_region(event.x,event.y) == "separator":
        #         return "break"
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
        list1.add_command(label="Defects", command=self.add_defect)
            

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
            select_sql = "Select * from defects where 1 "
            parameters =[]
            # check search input
            if self.defect_id_input !="":
                select_sql += " AND defect_id = ?"
                parameters += [self.defect_id_input]
            if (self.defect_road_name_input):
                select_sql += " AND defect_road_name like ?"
                parameters += [self.defect_road_name_input]
            print(select_sql)
            self.myCursor.execute(select_sql,parameters)
            self.pc = self.myCursor.fetchall()
            if self.pc:
                self.listTree.delete(*self.listTree.get_children())
                row_num = 1
                for row in self.pc:
                    self.listTree.insert("",'end',text=row[0] ,values = (row_num, row[1],row[2],row[3],row[4],row[5],row[6],row[7]))
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
            
            self.myCursor.execute("Select * from defects")
            self.pc = self.myCursor.fetchall()
            if self.pc:
                self.listTree.delete(*self.listTree.get_children())
                row_num = 1
                for row in self.pc:
                    self.listTree.insert("",'end',text=row[0] ,values = (row_num, row[1],row[2],row[3],row[4],row[5],row[6],row[7]))
                    row_num +=1
            # else:
            #     messagebox.showinfo("Error", "Either Defect ID is wrong or the road name is not yet exist.")
        except Error:
            messagebox.showerror("Error","Something Goes Wrong")

    def check(self):
        try:
            conn = sqlite3.connect(defect_database.database_name)
            mycursor = conn.cursor()
            mycursor.execute("Select * from admin")
            z = mycursor.fetchone()
            if not z:
                messagebox.showinfo("Error", "Please Register A user")
                x = messagebox.askyesno("Confirm","Do you want to register a user")
                if x:
                    self.destroy()
                    os.system('%s %s' % (py, 'admin/admin_user_reg.py'))
            else:
                #label and input box
                self.label3 = Label(self, text='ASAP Defect List', bg='light blue', font=('Arial', 30, 'bold'))
                self.label3.place(x=350, y=80)
                # search defect id input field
                self.label4 = Label(self, text="Enter Defect ID", bg='light blue', font=('Arial', 14, 'bold'))
                self.label4.place(x=100, y=200)
                self.e1 = Entry(self, textvariable=self.defect_id, width=40).place(x=350, y=210)
                self.srt = Button(self, text='Search', width=15, font=('arial', 10),command = self.search_defect).place(x=700, y=206)
                # self.label5 = Label(self, text='OR', bg='light blue', font=('arial', 14, 'bold')).place(x=170, y=235)
                self.label5 = Label(self, text="Enter Road Name", bg='light blue', font=('Arial', 14, 'bold'))
                self.label5.place(x=100, y=260)
                # search road name input field
                self.e2 = Entry(self, textvariable=self.road_name, width=40).place(x=350, y=270)
                # self.brt = Button(self, text='Find', width=15, font=('arial', 10),command = search_by_road_name).place(x=700, y=266)
                self.label6 = Label(self, text="Details", bg='light blue', font=('Arial', 14, 'underline', 'bold'))
                self.label6.place(x=100, y=350)
                self.button = Button(self, text='Search Defect ID', width=20, font=('Algerian', 20)).place(x=1000,y=150)
                self.button = Button(self, text='Search Road Name', width=20, font=('Algerian', 20)).place(x=1000,y=250)
                
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
            # print(a)
            showinfo(title='Information', message=repr(tuple(record)))
            
            
        # check()
        # show_all_data()

HomeWindow().mainloop()