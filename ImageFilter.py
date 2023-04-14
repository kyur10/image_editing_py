# import the required libraries
from tkinter import *
from tkinter.ttk import Treeview, Style
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk, ImageFilter
from PIL.ImageFilter import (CONTOUR, DETAIL, EDGE_ENHANCE, FIND_EDGES, SHARPEN)
import db
import time
import shutil
from pathlib import Path


# First Window Class
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
        self.root.geometry("700x700")

        # set window color
        self.root.configure(bg=self.root_bg_color)

        # disabling resizing the GUI
        self.root.resizable(False, False)

        select_image_label = Label(self.root, text="Select an image", background=self.root_bg_color,
                                   font="Helvetica 14")
        select_image_label.place(x=270, y=10, width=157, height=30)

        browse_button = Button(self.root, text="Browse Image .....", bg="#28a745", font="Helvetica 14", fg="#ffffff",
                               command=self.openImage)
        browse_button.place(x=260, y=50, width=173, height=30)

        image_name_label = Label(self.root, text="Image Name: ", background=self.root_bg_color, font="Helvetica 12",
                                 justify="left")
        image_name_label.place(x=230, y=140, width=102, height=30)

        file_size_label = Label(self.root, text="Image Size: ", background=self.root_bg_color, font="Helvetica 12",
                                justify="left")
        file_size_label.place(x=230, y=180, width=85, height=30)

        file_type_label = Label(self.root, text="File Type: ", background=self.root_bg_color, font="Helvetica 12",
                                justify="left")
        file_type_label.place(x=230, y=220, width=79, height=30)

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
        display_image_name.place(x=350, y=140, width=296, height=30)

        display_file_size = Label(self.root, text=self.image_details['size'], background=self.root_bg_color,
                                  font="Helvetica 12",
                                  justify="left", anchor="w")
        display_file_size.place(x=350, y=180, width=296, height=25)

        display_file_type = Label(self.root, text=self.image_details['type'], background=self.root_bg_color,
                                  font="Helvetica 12",
                                  justify="left", anchor="w")
        display_file_type.place(x=350, y=220, width=296, height=25)

        started_button = Button(self.root, text="Get Started", font="Helvetica 18", bg="#007bff", fg="#ffffff",
                                justify="center", anchor="center", command=self.startButtonAction)
        started_button.place(x=150, y=600, width=420, height=49)

    def startButtonAction(self):
        for widgets in self.root.winfo_children():
            widgets.destroy()
        SecondWindow(self.root, self.image_details)


# Second Window class
class SecondWindow:
    def __init__(self, root, image_details):
        self.root = root
        self.canvas = None
        self.image_container = None
        self.root_bg_color = "#F9F6EE"
        self.image_details = image_details
        self.original_image = Image.open(self.image_details['path'])
        self.width, self.height = self.original_image.size
        self.current_image_base64 = None
        self.updated_image = Image.open(self.image_details['path'])
        self.grayscale_added = False

        self.filters = {
            "filter": "",
            "resize": "",
            "grayscale": False,
            "blur": "",
            "rotate": "",
            "resolution": ""
        }

        # add the image to the label
        img = Image.open(self.image_details['path'])
        self.loadImage(img)

        upload_button_image = PhotoImage(file='./icons/upload.png')
        upload_button = Button(self.root, text="Upload", justify="center", font="Helvetica 12", bg="#28a745",
                               fg="#ffffff", command=self.uploadButtonAction, image=upload_button_image, compound=LEFT)
        upload_button.image = upload_button_image
        upload_button.place(x=20, y=550, width=158, height=30)

        download_button_image = PhotoImage(file='./icons/downloads.png')
        download_button = Button(self.root, text="Download", justify="center", font="Helvetica 12", bg="#28a745",
                                 fg="#ffffff", command=self.downloadButtonAction, image=download_button_image,
                                 compound=LEFT)
        download_button.image = download_button_image
        download_button.place(x=350, y=550, width=158, height=30)

        reset_button_image = PhotoImage(file='./icons/reset.png')
        reset_button = Button(self.root, text="Reset", justify="center", font="Helvetica 12", bg="#28a745",
                              fg="#ffffff", command=self.resetButtonAction, image=reset_button_image, compound=LEFT)
        reset_button.image = reset_button_image
        reset_button.place(x=20, y=630, width=158, height=30)

        back_button_image = PhotoImage(file='./icons/back.png')
        back_button = Button(self.root, text='Back', justify="center", font="Helvetica 12", bg="#28a745",
                             fg="#ffffff", image=back_button_image, command=self.backToHomePage, compound=LEFT)
        back_button.image = back_button_image
        back_button.place(x=185, y=630, width=158, height=30)

        view_history_button_image = PhotoImage(file='./icons/history.png')
        view_history_button = Button(self.root, text="View History", justify="center", font="Helvetica 12",
                                     bg="#28a745",
                                     fg="#ffffff", command=self.viewHistoryButtonAction,
                                     image=view_history_button_image, compound=LEFT)
        view_history_button.image = view_history_button_image
        view_history_button.place(x=350, y=630, width=158, height=30)

        add_filter_label = StringVar(self.root)
        add_filter_options = ["Select Filter", "CONTOUR", "DETAIL", "EDGE_ENHANCE", "FIND_EDGES", "SHARPEN"]
        add_filter_label.set(add_filter_options[0])  # default value
        add_filter_menu = OptionMenu(self.root, add_filter_label, *add_filter_options, command=self.filterSelect)
        add_filter_menu.config(bg="#28a745", fg="#ffffff", font="Helvetica 12")
        add_filter_menu.place(x=520, y=10, width=175, height=35)

        add_resize_label = StringVar(self.root)
        add_resize_options = ["Select Resize", "10%", "50%", "60%", "80%"]
        add_resize_label.set(add_resize_options[0])  # default value
        add_resize_menu = OptionMenu(self.root, add_resize_label, *add_resize_options, command=self.resizeSelect)
        add_resize_menu.config(bg="#28a745", fg="#ffffff", font="Helvetica 12")
        add_resize_menu.place(x=520, y=65, width=175, height=35)

        self.display_width_height = Label(self.root, text=f"{self.width}x{self.height}", background=self.root_bg_color,
                                          font="Helvetica 12",
                                          justify="left", anchor="w")
        self.display_width_height.place(x=520, y=95, width=175, height=25)

        grayscale_button = Button(self.root, text="Grayscale", justify="center", font="Helvetica 12", bg="#28a745",
                                  fg="#ffffff", command=self.grayscaleButtonAction)
        grayscale_button.place(x=520, y=130, width=175, height=30)

        blur_label = StringVar(self.root)
        options = ["Select Blur", "Low", "Medium", "High"]
        blur_label.set(options[0])  # default value
        blur_menu = OptionMenu(root, blur_label, *options, command=self.blurSelect)
        blur_menu.config(bg="#28a745", fg="#ffffff", font="Helvetica 12")
        blur_menu.place(x=520, y=190, width=175, height=35)

        rotate_label = StringVar(self.root)
        options = ["Select Rotate", "Rotate Right 90", "Rotate Left 90", "Rotate 180"]
        rotate_label.set(options[0])  # default value
        rotate_menu = OptionMenu(self.root, rotate_label, *options, command=self.rotateSelect)
        rotate_menu.config(bg="#28a745", fg="#ffffff", font="Helvetica 12")
        rotate_menu.place(x=520, y=250, width=175, height=35)

        resolution_label = StringVar(self.root)
        options = ["Select Resolution", "Medium", "Low"]
        resolution_label.set(options[0])  # default value
        resolution_menu = OptionMenu(self.root, resolution_label, *options, command=self.resolutionSelect)
        resolution_menu.config(bg="#28a745", fg="#ffffff", font="Helvetica 12")
        resolution_menu.place(x=520, y=310, width=175, height=35)

    def action(self, value):
        reduce_picture = False
        img = self.original_image

        filter_name, option_name = value

        # update the current dictionary
        for key, value in self.filters.items():
            if key == filter_name:
                self.filters[key] = option_name

        for key, value in self.filters.items():
            if key == "filter" and value != "":
                img = img.filter(value)

            if key == "blur" and value != "":
                img = img.filter(ImageFilter.BoxBlur(value))

            if key == "grayscale" and value:
                img = img.convert('L')

            if key == "rotate" and value != "":
                img = img.rotate(value)

            if key == "resolution" and value != "":
                img = img.reduce(value)

            if key == "resize":
                if value != "":
                    width, height = value
                    img = img.resize(value)
                    self.display_width_height["text"] = f"{width}x{height}"
                    reduce_picture = True
                else:
                    self.display_width_height["text"] = f"{self.width}x{self.height}"

        self.canvas.delete("all")
        self.loadImage(img, reduce_picture)

    def uploadButtonAction(self):
        try:
            file_name = time.strftime("%Y%m%d-%H%M%S")
            ext = (self.image_details['type']).lower()
            self.updated_image.save(f"uploaded_images/{file_name}.{ext}")

            insert_value = {
                "FILE_NAME": f"{file_name}.{ext}",
                "DIMENSION": self.display_width_height.cget("text"),
                "FILTER": str(self.filters),
                "IMAGE": f"uploaded_images/{file_name}.{ext}"
            }
            db.insert(insert_value)
            messagebox.showinfo("Upload", "Image has been uploaded successfully")
        except:
            messagebox.showerror("Error", "Failed to upload the image")

    # download the current canvas image to the local file location
    def downloadButtonAction(self):
        try:
            file_name = time.strftime("%Y%m%d-%H%M%S")
            ext = (self.image_details['type']).lower()
            downloads_path = str(Path.home() / "Downloads")
            self.updated_image.save(f"{downloads_path}/{file_name}.{ext}")
            messagebox.showinfo("Saved", "Image has been saved successfully")
        except:
            messagebox.showerror("Error", "Failed to save the image")

    def resetButtonAction(self):
        SecondWindow(self.root, self.image_details)

    # back to home page
    def backToHomePage(self):
        for widgets in self.root.winfo_children():
            widgets.destroy()
        FirstWindow(self.root)

    def viewHistoryButtonAction(self):
        for widgets in self.root.winfo_children():
            widgets.destroy()
        ThirdWindow(self.root, self.image_details)

    def grayscaleButtonAction(self):
        if not self.grayscale_added:
            self.grayscale_added = True
        else:
            self.grayscale_added = False
        self.action(("grayscale", self.grayscale_added))

    def loadImage(self, img, reduce_picture=False):
        self.updated_image = img

        if not reduce_picture:
            img = img.resize((500, 500), Image.LANCZOS)
            self.width = 500
            self.height = 500

        img = ImageTk.PhotoImage(img)
        self.canvas = Canvas(self.root, width=500, height=500, highlightbackground="#000", highlightthickness=1)
        self.image_container = self.canvas.create_image(0, 0, anchor=NW, image=img)
        self.canvas.image = img
        self.canvas.place(x=15, y=15, width=500, height=500)

    def filterSelect(self, event):
        match event:
            case "CONTOUR":
                value = CONTOUR
            case "DETAIL":
                value = DETAIL
            case "EDGE_ENHANCE":
                value = EDGE_ENHANCE
            case "FIND_EDGES":
                value = FIND_EDGES
            case "SHARPEN":
                value = SHARPEN
            case _:
                value = ""

        self.action(("filter", value))

    def resizeSelect(self, event):
        if event != "Select Resize":
            value = int(event.split("%")[0])
            width = int(self.width - ((value / 100) * self.width))
            height = int(self.height - ((value / 100) * self.height))

            self.action(("resize", (width, height)))
        else:
            self.action(("resize", ""))

    # get executed when the user select blur level
    def blurSelect(self, event):
        match event:
            case "Low":
                value = 5
            case "Medium":
                value = 10
            case "High":
                value = 15
            case _:
                value = ""

        self.action(("blur", value))

    # get executed when the user choose rotate option
    def rotateSelect(self, event):
        match event:
            case "Rotate Right 90":
                value = -90
            case "Rotate Left 90":
                value = 90
            case "Rotate 180":
                value = 180
            case _:
                value = ""

        self.action(("rotate", value))

    # get executed when the user choose resolution adjustment option
    def resolutionSelect(self, event):
        match event:
            case "Medium":
                value = 4
            case "Low":
                value = 8
            case _:
                value = ""

        self.action(("resolution", value))


# Third Window class
class ThirdWindow:
    def __init__(self, root, image_details):
        self.root = root
        self.image_details = image_details

        # define columns
        columns = ('sn', 'id', 'file_name', 'dimension', 'uploaded_at')

        # Using treeview widget style
        style = Style()
        style.configure('Treeview', rowheight=50)  # increase height
        self.tree = Treeview(self.root, columns=columns, show='headings')

        # define headings
        self.tree.heading('sn', text='SN')
        self.tree.column('sn', minwidth=0, width=60, anchor='center')

        self.tree.heading('id', text='ID')
        self.tree.column('id', minwidth=0, width=60, anchor='center')

        self.tree.heading('file_name', text='File Name')
        self.tree.column('file_name', minwidth=0, width=180, anchor='center')

        self.tree.heading('dimension', text='Dimension')
        self.tree.column('dimension', minwidth=0, width=120, anchor='center')

        self.tree.heading('uploaded_at', text='Uploaded At')
        self.tree.column('uploaded_at', minwidth=0, width=150, anchor='center')

        self.tree.place(x=20, y=50, width=660, height=630)

        back_button_image = PhotoImage(file='./icons/back.png')
        back_button = Button(self.root, text='Back', justify="center", font="Helvetica 12", bg="#28a745",
                             fg="#ffffff", command=self.backButtonAction, image=back_button_image, compound=LEFT)
        back_button.image = back_button_image
        back_button.place(x=20, y=10, width=120, height=30)

        home_button_image = PhotoImage(file='./icons/home.png')
        home_button = Button(self.root, text='Home', justify="center", font="Helvetica 12", bg="#28a745",
                             fg="#ffffff", command=self.homeButtonAction, image=home_button_image, compound=LEFT)
        home_button.image = home_button_image
        home_button.place(x=560, y=10, width=120, height=30)

        download_button = Button(self.root, text='Download', justify='center', font="Helvetica 12", bg="#28a745",
                                 fg="#ffffff", command=self.downloadSelectedAction)
        download_button.place(x=250, y=10, width=115, height=30)

        remove_button = Button(self.root, text='Remove', justify='center', font="Helvetica 12", bg="#28a745",
                               fg="#ffffff", command=self.deleteSelectedAction)
        remove_button.place(x=380, y=10, width=100, height=30)

        tree_data = []
        count = 1
        image_paths = []
        fetched_data = db.fetch()
        for data in fetched_data:
            image_paths.append(data["IMAGE"])
            tree_data.append(
                (count, data["ID"], data["FILE_NAME"], data["DIMENSION"], data["CREATED_AT"]))
            count = count + 1

        # add data to the treeview
        for record in tree_data:
            self.tree.insert("", "end", values=record)

    # back button action from the third window
    def backButtonAction(self):
        for widgets in self.root.winfo_children():
            widgets.destroy()
        SecondWindow(self.root, self.image_details)

    # home button action from the third window
    def homeButtonAction(self):
        for widgets in self.root.winfo_children():
            widgets.destroy()
        FirstWindow(self.root)

    # delete the selected image from the list
    def deleteSelectedAction(self):
        try:
            selected_row = self.tree.focus()
            details = self.tree.item(selected_row)
            image_id = int(details["values"][1])
            db.delete(image_id)
            messagebox.showinfo("Delete Successfully", "Selected Image has been deleted successfully")
            for widgets in self.root.winfo_children():
                widgets.destroy()
            ThirdWindow(self.root, self.image_details)
        except IndexError:
            messagebox.showinfo("Error", "Please first make the selection")

    # download the selected image from the list
    def downloadSelectedAction(self):
        try:
            selected_row = self.tree.focus()
            details = self.tree.item(selected_row)
            image_name = details["values"][2]

            source = f"uploaded_images/{image_name}"
            destination = str(Path.home() / "Downloads")+"/"+image_name

            shutil.copy(source, destination)
            messagebox.showinfo("Download Success", "Image has been downloaded successfully")
        except IndexError:
            messagebox.showinfo("Error", "Please first make the selection")
