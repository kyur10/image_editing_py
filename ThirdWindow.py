# import the required libraries
from tkinter import *
from tkinter.ttk import Treeview, Style

from PIL import Image, ImageTk

import db


class ThirdWindow:
    def __init__(self, root):
        self.root = root
        self.root_bg_color = "#F9F6EE"

        # define columns
        columns = ('sn', 'file_name', 'dimension', 'uploaded_at', 'action')

        # Using treeview widget style
        style = Style()
        style.configure('Treeview', rowheight=50)  # increase height
        tree = Treeview(root, columns=columns, show=('headings', 'tree'))

        # define headings
        tree.heading('#0', text='Image')
        tree.column('#0', minwidth=0, width=100)

        tree.heading('sn', text='SN')
        tree.column('sn', minwidth=0, width=100, anchor='center')

        tree.heading('file_name', text='File Name')
        tree.column('file_name', minwidth=0, width=150, anchor='center')

        tree.heading('dimension', text='Dimension')
        tree.column('dimension', minwidth=0, width=120, anchor='center')

        tree.heading('uploaded_at', text='Uploaded At')
        tree.column('uploaded_at', minwidth=0, width=150, anchor='center')

        tree.heading('action', text='Action')
        tree.column('action', minwidth=0, width=150, anchor='center')

        tree_data = []
        count = 1
        image_paths = []
        fetched_data = db.fetch()
        for data in fetched_data:
            image_paths.append(data["IMAGE"])
            tree_data.append(
                (count, data["FILE_NAME"], data["DIMENSION"], data["CREATED_AT"], "Action"))
            count = count + 1

        # add data to the treeview
        counter = 0
        for record in tree_data:
            img = Image.open(image_paths[counter])
            img = img.resize((50, 50), Image.ANTIALIAS)
            img = ImageTk.PhotoImage(img)

            tree.insert("", "end", image=img, values=record)
            Label.image = img
            counter = counter + 1

        tree.place(x=20, y=20, width=759, height=757)
