# import the required libraries
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
from PIL.ImageFilter import (
    BLUR, CONTOUR, DETAIL, EDGE_ENHANCE, EDGE_ENHANCE_MORE,
    EMBOSS, FIND_EDGES, SMOOTH, SMOOTH_MORE, SHARPEN
)
from pathlib import Path


class FirstWindow:
    def __init__(self, root):
        self.image_details = {
            'name': "",
            'size': "",
            'type': "",
            'path': ""
        }
        self.root_bg_color = "#F9F6EE"

        # add a title
        root.title("Image Editor")

        # setting window size
        root.geometry("800x800")

        # set window color
        root.configure(bg=self.root_bg_color)

        # disabling resizing the GUI
        root.resizable(False, False)

        select_image_label = Label(root, text="Select an image", background=self.root_bg_color, font="Helvetica 14")
        select_image_label.place(x=300, y=10, width=157, height=30)

        browse_button = Button(root, text="Browse Image .....", bg="#28a745", font="Helvetica 14", fg="#ffffff",
                               command=self.openImage)
        browse_button.place(x=290, y=50, width=173, height=30)

        image_name_label = Label(root, text="Image Name: ", background=self.root_bg_color, font="Helvetica 12",
                                 justify="left")
        image_name_label.place(x=250, y=140, width=102, height=30)

        file_size_label = Label(root, text="Image Size: ", background=self.root_bg_color, font="Helvetica 12",
                                justify="left")
        file_size_label.place(x=250, y=180, width=85, height=30)

        file_type_label = Label(root, text="File Type: ", background=self.root_bg_color, font="Helvetica 12",
                                justify="left")
        file_type_label.place(x=250, y=220, width=79, height=30)

    def openImage(self):
        f_types = [('Jpg Files', '*.jpg')]
        filename = filedialog.askopenfilename(title="Select A File", filetypes=f_types)
        img = Image.open(filename)

        self.image_details['path'] = filename
        self.image_details['name'] = Path(img.filename).name
        self.image_details['size'] = f"{img.size[0]}x{img.size[1]}"
        self.image_details['type'] = img.format

        if self.image_details['name'] != "":
            self.displayImageInfo()

    def displayImageInfo(self):
        display_image_name = Label(root, text=self.image_details['name'], background=self.root_bg_color,
                                   font="Helvetica 12",
                                   justify="left", anchor="w")
        display_image_name.place(x=370, y=140, width=296, height=30)

        display_file_size = Label(root, text=self.image_details['size'], background=self.root_bg_color,
                                  font="Helvetica 12",
                                  justify="left", anchor="w")
        display_file_size.place(x=370, y=180, width=296, height=25)

        display_file_type = Label(root, text=self.image_details['type'], background=self.root_bg_color,
                                  font="Helvetica 12",
                                  justify="left", anchor="w")
        display_file_type.place(x=370, y=220, width=296, height=25)

        started_button = Button(root, text="Get Started", font="Helvetica 18", bg="#007bff", fg="#ffffff",
                                justify="center", anchor="center", command=self.startButtonAction)
        started_button.place(x=190, y=660, width=420, height=49)

    def startButtonAction(self):
        for widgets in root.winfo_children():
            widgets.destroy()
        SecondWindow(root, self.image_details)


class SecondWindow:
    def __init__(self, root, image_details):
        self.canvas = None
        self.image_container = None
        self.root_bg_color = "#F9F6EE"
        self.image_details = image_details
        self.original_image = Image.open(self.image_details['path'])
        self.width, self.height = self.original_image.size

        # add the image to the label
        img = Image.open(self.image_details['path'])
        self.loadImage(img)
        # img = img.resize((500, 500), Image.LANCZOS)
        # img = ImageTk.PhotoImage(img)
        # self.canvas = Canvas(root, width=500, height=500, highlightbackground="#000", highlightthickness=1)
        # self.image_container = self.canvas.create_image(0, 0, anchor=NW, image=img)
        # self.canvas.image = img
        # self.canvas.place(x=15, y=15, width=500, height=500)

        # image_frame = Label(root, width=500, height=500, image=img)
        # image_frame.image = img
        # image_frame.place(x=15, y=15, width=500, height=500)

        upload_button = Button(root, text="Upload", justify="center", font="Helvetica 14", bg="#28a745",
                               fg="#ffffff", command=self.uploadButtonAction)
        upload_button.place(x=20, y=550, width=155, height=30)

        download_button = Button(root, text="Download", justify="center", font="Helvetica 14", bg="#28a745",
                                 fg="#ffffff", command=self.downloadButtonAction)
        download_button.place(x=350, y=550, width=158, height=30)

        reset_button = Button(root, text="Reset", justify="center", font="Helvetica 14", bg="#28a745",
                              fg="#ffffff", command=self.resetButtonAction)
        reset_button.place(x=20, y=630, width=153, height=30)

        view_history_button = Button(root, text="View History", justify="center", font="Helvetica 14", bg="#28a745",
                                     fg="#ffffff", command=self.viewHistoryButtonAction)
        view_history_button.place(x=350, y=630, width=157, height=30)

        add_filter_label = StringVar(root)
        options = ["Select filter", "CONTOUR", "DETAIL", "EDGE_ENHANCE", "FIND_EDGES", "SHARPEN"]
        add_filter_label.set(options[0])  # default value
        add_filter_menu = OptionMenu(root, add_filter_label, *options, command=self.filterSelect)
        add_filter_menu.config(bg="#28a745", fg="#ffffff", font="Helvetica 14")
        add_filter_menu.place(x=530, y=10, width=230, height=35)

        add_resize_label = StringVar(root)
        options = ["Select resize option", "10%", "50%", "60%", "80%"]
        add_resize_label.set(options[0])  # default value
        add_resize_menu = OptionMenu(root, add_resize_label, *options, command=self.resizeSelect)
        add_resize_menu.config(bg="#28a745", fg="#ffffff", font="Helvetica 14")
        add_resize_menu.place(x=530, y=65, width=230, height=35)

        self.display_width_height = Label(root, text=f"{self.width}x{self.height}", background=self.root_bg_color,
                                          font="Helvetica 12",
                                          justify="left", anchor="w")
        self.display_width_height.place(x=530, y=95, width=296, height=25)

        grayscale_button = Button(root, text="Grayscale", justify="center", font="Helvetica 14", bg="#28a745",
                                  fg="#ffffff", command=self.grayscaleButtonAction)
        grayscale_button.place(x=530, y=130, width=230, height=30)

    def uploadButtonAction(self):
        print("command")

    def downloadButtonAction(self):
        print("command")

    def resetButtonAction(self):
        print("command")

    def viewHistoryButtonAction(self):
        print("command")

    def grayscaleButtonAction(self):
        img = self.original_image.convert('L')
        self.canvas.delete("all")
        self.loadImage(img)

    def loadImage(self, img, reduce_picture=False):
        if not reduce_picture:
            img = img.resize((500, 500), Image.LANCZOS)
        img = ImageTk.PhotoImage(img)
        self.canvas = Canvas(root, width=500, height=500, highlightbackground="#000", highlightthickness=1)
        self.image_container = self.canvas.create_image(0, 0, anchor=NW, image=img)
        self.canvas.image = img
        self.canvas.place(x=15, y=15, width=500, height=500)

    def filterSelect(self, event):
        match event:
            case "CONTOUR":
                img = self.original_image.filter(CONTOUR)
            case "DETAIL":
                img = self.original_image.filter(DETAIL)
            case "EDGE_ENHANCE":
                img = self.original_image.filter(EDGE_ENHANCE)
            case "FIND_EDGES":
                img = self.original_image.filter(FIND_EDGES)
            case "SHARPEN":
                img = self.original_image.filter(SHARPEN)
            case _:
                img = self.original_image

        self.canvas.delete("all")
        self.loadImage(img)

    def resizeSelect(self, event):
        reduce_picture = False
        if event != "Select resize option":
            value = int(event.split("%")[0])
            width = int(self.width - ((value / 100) * self.width))
            height = int(self.height - ((value / 100) * self.height))
            self.display_width_height["text"] = f"{width}x{height}"
            img = self.original_image.resize((width, height))
            if width < 500 and height < 500:
                reduce_picture = True
        else:
            self.display_width_height["text"] = f"{self.width}x{self.height}"
            img = self.original_image.resize((self.width, self.height))

        self.canvas.delete("all")
        self.loadImage(img, reduce_picture)


if __name__ == "__main__":
    root = Tk()
    app = FirstWindow(root)
    root.mainloop()
