# import the required libraries
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk, ImageFilter
from PIL.ImageFilter import (CONTOUR, DETAIL, EDGE_ENHANCE, FIND_EDGES, SHARPEN)
from io import BytesIO
import base64
import os
import db
import time
from ThirdWindow import ThirdWindow


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
        upload_button = Button(self.root, text="Upload", justify="center", font="Helvetica 14", bg="#28a745",
                               fg="#ffffff", command=self.uploadButtonAction, image=upload_button_image, compound=LEFT)
        upload_button.image = upload_button_image
        upload_button.place(x=20, y=550, width=155, height=30)

        download_button_image = PhotoImage(file='./icons/downloads.png')
        download_button = Button(self.root, text="Download", justify="center", font="Helvetica 14", bg="#28a745",
                                 fg="#ffffff", command=self.downloadButtonAction, image=download_button_image,
                                 compound=LEFT)
        download_button.image = download_button_image
        download_button.place(x=350, y=550, width=158, height=30)

        reset_button_image = PhotoImage(file='./icons/reset.png')
        reset_button = Button(self.root, text="Reset", justify="center", font="Helvetica 14", bg="#28a745",
                              fg="#ffffff", command=self.resetButtonAction, image=reset_button_image, compound=LEFT)
        reset_button.image = reset_button_image
        reset_button.place(x=20, y=630, width=153, height=30)

        view_history_button_image = PhotoImage(file='./icons/history.png')
        view_history_button = Button(self.root, text="View History", justify="center", font="Helvetica 14",
                                     bg="#28a745",
                                     fg="#ffffff", command=self.viewHistoryButtonAction,
                                     image=view_history_button_image, compound=LEFT)
        view_history_button.image = view_history_button_image
        view_history_button.place(x=350, y=630, width=157, height=30)

        add_filter_label = StringVar(self.root)
        add_filter_options = ["Select filter", "CONTOUR", "DETAIL", "EDGE_ENHANCE", "FIND_EDGES", "SHARPEN"]
        add_filter_label.set(add_filter_options[0])  # default value
        add_filter_menu = OptionMenu(self.root, add_filter_label, *add_filter_options, command=self.filterSelect)
        add_filter_menu.config(bg="#28a745", fg="#ffffff", font="Helvetica 14")
        add_filter_menu.place(x=530, y=10, width=230, height=35)

        add_resize_label = StringVar(self.root)
        add_resize_options = ["Select resize option", "10%", "50%", "60%", "80%"]
        add_resize_label.set(add_resize_options[0])  # default value
        add_resize_menu = OptionMenu(self.root, add_resize_label, *add_resize_options, command=self.resizeSelect)
        add_resize_menu.config(bg="#28a745", fg="#ffffff", font="Helvetica 14")
        add_resize_menu.place(x=530, y=65, width=230, height=35)

        self.display_width_height = Label(self.root, text=f"{self.width}x{self.height}", background=self.root_bg_color,
                                          font="Helvetica 12",
                                          justify="left", anchor="w")
        self.display_width_height.place(x=530, y=95, width=296, height=25)

        grayscale_button = Button(self.root, text="Grayscale", justify="center", font="Helvetica 14", bg="#28a745",
                                  fg="#ffffff", command=self.grayscaleButtonAction)
        grayscale_button.place(x=530, y=130, width=230, height=30)

        blur_label = StringVar(self.root)
        options = ["Select blur option", "Low", "Medium", "High"]
        blur_label.set(options[0])  # default value
        blur_menu = OptionMenu(root, blur_label, *options, command=self.blurSelect)
        blur_menu.config(bg="#28a745", fg="#ffffff", font="Helvetica 14")
        blur_menu.place(x=530, y=190, width=230, height=35)

        rotate_label = StringVar(self.root)
        options = ["Select rotate option", "Rotate Right 90", "Rotate Left 90", "Rotate 180"]
        rotate_label.set(options[0])  # default value
        rotate_menu = OptionMenu(self.root, rotate_label, *options, command=self.rotateSelect)
        rotate_menu.config(bg="#28a745", fg="#ffffff", font="Helvetica 14")
        rotate_menu.place(x=530, y=250, width=230, height=35)

        resolution_label = StringVar(self.root)
        options = ["Select resolution option", "Medium", "Low"]
        resolution_label.set(options[0])  # default value
        resolution_menu = OptionMenu(self.root, resolution_label, *options, command=self.resolutionSelect)
        resolution_menu.config(bg="#28a745", fg="#ffffff", font="Helvetica 14")
        resolution_menu.place(x=530, y=310, width=230, height=35)

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
            self.updated_image.save(f"uploaded_images/{file_name}.png")

            insert_value = {
                "FILE_NAME": self.image_details['name'],
                "DIMENSION": str(f"{self.width}x{self.height}"),
                "FILTER": str(self.filters),
                "IMAGE": f"uploaded_images/{file_name}.png"
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
            self.updated_image.save(f"downloaded_images/{file_name}.{ext}")

            # imgdata = base64.b64decode(self.current_image_base64)
            # image_name = os.path.splitext(self.image_details['name'])[0]
            # filename = f"images/{image_name}.{self.image_details['type']}"
            # with open(filename, 'wb') as f:
            #     f.write(imgdata)
            messagebox.showinfo("Saved", "Image has been saved successfully")
        except:
            messagebox.showerror("Error", "Failed to save the image")

    def resetButtonAction(self):
        SecondWindow(self.root, self.image_details)

    def viewHistoryButtonAction(self):
        for widgets in self.root.winfo_children():
            widgets.destroy()
        ThirdWindow(self.root)

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

        # convert the image to base64
        # im_file = BytesIO()
        # image_ext = ((self.image_details['name']).split(".")[1]).upper()
        # if image_ext == 'JPG':
        #     image_ext = "JPEG"
        # img.save(im_file, format=image_ext)
        # im_bytes = im_file.getvalue()  # im_bytes: image in binary format.
        # im_b64 = base64.b64encode(im_bytes)
        # self.current_image_base64 = im_b64

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
        if event != "Select resize option":
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
