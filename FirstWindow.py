# import the required libraries
from tkinter import *
from tkinter import filedialog
from PIL import Image
from pathlib import Path
from SecondWindow import SecondWindow


class FirstWindow:
    def __init__(self, root):
        self.image_details = {
            'name': "",
            'size': "",
            'type': "",
            'path': ""
        }
        self.root_bg_color = "#F9F6EE"
        self.root = root

        # add a title
        self.root.title("Image Editor")

        # setting window size
        self.root.geometry("800x800")

        # set window color
        self.root.configure(bg=self.root_bg_color)

        # disabling resizing the GUI
        self.root.resizable(False, False)

        select_image_label = Label(self.root, text="Select an image", background=self.root_bg_color,
                                   font="Helvetica 14")
        select_image_label.place(x=300, y=10, width=157, height=30)

        browse_button = Button(self.root, text="Browse Image .....", bg="#28a745", font="Helvetica 14", fg="#ffffff",
                               command=self.openImage)
        browse_button.place(x=290, y=50, width=173, height=30)

        image_name_label = Label(self.root, text="Image Name: ", background=self.root_bg_color, font="Helvetica 12",
                                 justify="left")
        image_name_label.place(x=250, y=140, width=102, height=30)

        file_size_label = Label(self.root, text="Image Size: ", background=self.root_bg_color, font="Helvetica 12",
                                justify="left")
        file_size_label.place(x=250, y=180, width=85, height=30)

        file_type_label = Label(self.root, text="File Type: ", background=self.root_bg_color, font="Helvetica 12",
                                justify="left")
        file_type_label.place(x=250, y=220, width=79, height=30)

    def openImage(self):
        f_types = [('Jpg Files', '*.jpg'), ('Png Files', '*.png')]
        filename = filedialog.askopenfilename(title="Select A File", filetypes=f_types)
        img = Image.open(filename)

        self.image_details['path'] = filename
        self.image_details['name'] = Path(img.filename).name
        self.image_details['size'] = f"{img.size[0]}x{img.size[1]}"
        self.image_details['type'] = img.format

        if self.image_details['name'] != "":
            self.displayImageInfo()

    def displayImageInfo(self):
        display_image_name = Label(self.root, text=self.image_details['name'], background=self.root_bg_color,
                                   font="Helvetica 12",
                                   justify="left", anchor="w")
        display_image_name.place(x=370, y=140, width=296, height=30)

        display_file_size = Label(self.root, text=self.image_details['size'], background=self.root_bg_color,
                                  font="Helvetica 12",
                                  justify="left", anchor="w")
        display_file_size.place(x=370, y=180, width=296, height=25)

        display_file_type = Label(self.root, text=self.image_details['type'], background=self.root_bg_color,
                                  font="Helvetica 12",
                                  justify="left", anchor="w")
        display_file_type.place(x=370, y=220, width=296, height=25)

        started_button = Button(self.root, text="Get Started", font="Helvetica 18", bg="#007bff", fg="#ffffff",
                                justify="center", anchor="center", command=self.startButtonAction)
        started_button.place(x=190, y=660, width=420, height=49)

    def startButtonAction(self):
        for widgets in self.root.winfo_children():
            widgets.destroy()
        SecondWindow(self.root, self.image_details)
