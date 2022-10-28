import tkinter as tk
from tkinter import ttk


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.iconbitmap(r'images/defect.ico')
        self.title('Treeview demo')
        self.geometry('620x200')

        self.tree = self.create_tree_widget()

    def create_tree_widget(self):
        columns = ('first_name', 'last_name', 'email')
        tree = ttk.Treeview(self, columns=columns, show='headings')

        # define headings
        tree.heading('first_name', text='First Name')
        tree.heading('last_name', text='Last Name')
        tree.heading('email', text='Email')

        tree.grid(row=0, column=0, sticky=tk.NSEW)

        # adding an item
        tree.insert('', tk.END, values=('John', 'Doe', 'john.doe@email.com'))

        # insert a the end
        tree.insert('', tk.END, values=('Jane', 'Miller', 'jane.miller@email.com'))

        # insert at the beginning
        tree.insert('', 0, values=('Alice', 'Garcia', 'alice.garcia@email.com'))

        tree.bind('<<TreeviewSelect>>', self.item_selected)

        return tree

    def item_selected(self, event):
        for selected_item in self.tree.selection():
            self.tree.delete(selected_item)


if __name__ == '__main__':
    app = App()
    app.mainloop()