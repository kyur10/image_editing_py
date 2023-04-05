# import the required libraries
from tkinter import *
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageFilter
from PIL.ImageFilter import (
    BLUR, CONTOUR, DETAIL, EDGE_ENHANCE, EDGE_ENHANCE_MORE,
    EMBOSS, FIND_EDGES, SMOOTH, SMOOTH_MORE, SHARPEN
)
from pathlib import Path
from io import BytesIO
import base64
import os


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
        upload_button = Button(root, text="Upload", justify="center", font="Helvetica 14", bg="#28a745",
                               fg="#ffffff", command=self.uploadButtonAction, image=upload_button_image, compound=LEFT)
        upload_button.image = upload_button_image
        upload_button.place(x=20, y=550, width=155, height=30)

        download_button_image = PhotoImage(file='./icons/downloads.png')
        download_button = Button(root, text="Download", justify="center", font="Helvetica 14", bg="#28a745",
                                 fg="#ffffff", command=self.downloadButtonAction, image=download_button_image,
                                 compound=LEFT)
        download_button.image = download_button_image
        download_button.place(x=350, y=550, width=158, height=30)

        reset_button_image = PhotoImage(file='./icons/reset.png')
        reset_button = Button(root, text="Reset", justify="center", font="Helvetica 14", bg="#28a745",
                              fg="#ffffff", command=self.resetButtonAction, image=reset_button_image, compound=LEFT)
        reset_button.image = reset_button_image
        reset_button.place(x=20, y=630, width=153, height=30)

        view_history_button_image = PhotoImage(file='./icons/history.png')
        view_history_button = Button(root, text="View History", justify="center", font="Helvetica 14", bg="#28a745",
                                     fg="#ffffff", command=self.viewHistoryButtonAction,
                                     image=view_history_button_image, compound=LEFT)
        view_history_button.image = view_history_button_image
        view_history_button.place(x=350, y=630, width=157, height=30)

        add_filter_label = StringVar(root)
        add_filter_options = ["Select filter", "CONTOUR", "DETAIL", "EDGE_ENHANCE", "FIND_EDGES", "SHARPEN"]
        add_filter_label.set(add_filter_options[0])  # default value
        add_filter_menu = OptionMenu(root, add_filter_label, *add_filter_options, command=self.filterSelect)
        add_filter_menu.config(bg="#28a745", fg="#ffffff", font="Helvetica 14")
        add_filter_menu.place(x=530, y=10, width=230, height=35)

        add_resize_label = StringVar(root)
        add_resize_options = ["Select resize option", "10%", "50%", "60%", "80%"]
        add_resize_label.set(add_resize_options[0])  # default value
        add_resize_menu = OptionMenu(root, add_resize_label, *add_resize_options, command=self.resizeSelect)
        add_resize_menu.config(bg="#28a745", fg="#ffffff", font="Helvetica 14")
        add_resize_menu.place(x=530, y=65, width=230, height=35)

        self.display_width_height = Label(root, text=f"{self.width}x{self.height}", background=self.root_bg_color,
                                          font="Helvetica 12",
                                          justify="left", anchor="w")
        self.display_width_height.place(x=530, y=95, width=296, height=25)

        grayscale_button = Button(root, text="Grayscale", justify="center", font="Helvetica 14", bg="#28a745",
                                  fg="#ffffff", command=self.grayscaleButtonAction)
        grayscale_button.place(x=530, y=130, width=230, height=30)

        blur_label = StringVar(root)
        options = ["Select blur option", "Low", "Medium", "High"]
        blur_label.set(options[0])  # default value
        blur_menu = OptionMenu(root, blur_label, *options, command=self.blurSelect)
        blur_menu.config(bg="#28a745", fg="#ffffff", font="Helvetica 14")
        blur_menu.place(x=530, y=190, width=230, height=35)

        rotate_label = StringVar(root)
        options = ["Select rotate option", "Rotate Right 90", "Rotate Left 90", "Rotate 180", "Flip Vertical",
                   "Flip Horizontal"]
        rotate_label.set(options[0])  # default value
        rotate_menu = OptionMenu(root, rotate_label, *options, command=self.rotateSelect)
        rotate_menu.config(bg="#28a745", fg="#ffffff", font="Helvetica 14")
        rotate_menu.place(x=530, y=250, width=230, height=35)

        resolution_label = StringVar(root)
        options = ["Select resolution option", "Medium", "Low"]
        resolution_label.set(options[0])  # default value
        resolution_menu = OptionMenu(root, resolution_label, *options, command=self.resolutionSelect)
        resolution_menu.config(bg="#28a745", fg="#ffffff", font="Helvetica 14")
        resolution_menu.place(x=530, y=310, width=230, height=35)

    def action(self, value):
        img = self.original_image

        filter_name = list(value.items())[0][0]
        option_name = list(value.items())[0][1]

        for key, value in self.filters.items():
            if key == filter_name:
                self.filters[key] = option_name

        for key, value in self.filters.items():
            if key == "filter" and value != "Select filter":
                img = img.filter(value)

            elif key == "blur" and value != "Select blur option":
                img = img.filter(value)
                # img = img.filter(value)


    def uploadButtonAction(self):
        print("command")

    # download the current canvas image to the local file location
    def downloadButtonAction(self):
        try:
            imgdata = base64.b64decode(self.current_image_base64)
            image_name = os.path.splitext(self.image_details['name'])[0]
            filename = f"images/{image_name}.{self.image_details['type']}"
            with open(filename, 'wb') as f:
                f.write(imgdata)
            messagebox.showinfo("Saved", "Image has been saved successfully")
        except:
            messagebox.showerror("Error", "Failed to save the image")

    def resetButtonAction(self):
        SecondWindow(root, self.image_details)

    @staticmethod
    def viewHistoryButtonAction():
        print('test')

    def grayscaleButtonAction(self):
        if not self.grayscale_added:
            self.grayscale_added = True
            img = self.updated_image.convert('L')
        else:
            self.grayscale_added = False
            img = self.original_image
        self.canvas.delete("all")
        self.loadImage(img)

    def loadImage(self, img, reduce_picture=False):
        self.updated_image = img

        if not reduce_picture:
            img = img.resize((500, 500), Image.LANCZOS)
            self.width = 500
            self.height = 500

        # convert the image to base64
        im_file = BytesIO()
        image_ext = ((self.image_details['name']).split(".")[1]).upper()
        if image_ext == 'JPG':
            image_ext = "JPEG"
        img.save(im_file, format=image_ext)
        im_bytes = im_file.getvalue()  # im_bytes: image in binary format.
        im_b64 = base64.b64encode(im_bytes)
        self.current_image_base64 = im_b64

        img = ImageTk.PhotoImage(img)
        self.canvas = Canvas(root, width=500, height=500, highlightbackground="#000", highlightthickness=1)
        self.image_container = self.canvas.create_image(0, 0, anchor=NW, image=img)
        self.canvas.image = img
        self.canvas.place(x=15, y=15, width=500, height=500)

    def filterSelect(self, event):
        self.action({"filter": event})
        match event:
            case "CONTOUR":
                img = self.updated_image.filter(CONTOUR)
            case "DETAIL":
                img = self.updated_image.filter(DETAIL)
            case "EDGE_ENHANCE":
                img = self.updated_image.filter(EDGE_ENHANCE)
            case "FIND_EDGES":
                img = self.updated_image.filter(FIND_EDGES)
            case "SHARPEN":
                img = self.updated_image.filter(SHARPEN)
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
            img = self.updated_image.resize((width, height))
            if width < 500 and height < 500:
                reduce_picture = True
        else:
            self.display_width_height["text"] = f"{self.width}x{self.height}"
            img = self.original_image

        self.canvas.delete("all")
        self.loadImage(img, reduce_picture)

    # get executed when the user select blur level
    def blurSelect(self, event):
        self.action({"blur": event})
        match event:
            case "Low":
                img = self.updated_image.filter(ImageFilter.BoxBlur(5))
            case "Medium":
                img = self.updated_image.filter(ImageFilter.BoxBlur(10))
            case "High":
                img = self.updated_image.filter(ImageFilter.BoxBlur(15))
            case _:
                img = self.original_image

        self.canvas.delete("all")
        self.loadImage(img)

    # get executed when the user choose rotate option
    def rotateSelect(self, event):
        self.action({"rotate": event})

        match event:
            case "Rotate Right 90":
                img = self.updated_image.rotate(-90, expand=True)
            case "Rotate Left 90":
                img = self.updated_image.rotate(90, expand=True)
            case "Rotate 180":
                img = self.updated_image.rotate(180)
            case "Flip Vertical":
                img = self.updated_image.transpose(Image.FLIP_TOP_BOTTOM)
            case "Flip Horizontal":
                img = self.updated_image.transpose(Image.FLIP_LEFT_RIGHT)
            case _:
                img = self.original_image

        self.canvas.delete("all")
        self.loadImage(img)

    # get executed when the user choose resolution adjustment option
    def resolutionSelect(self, event):
        self.action({"resolution": event})
        match event:
            case "Medium":
                img = self.updated_image.reduce(4)  # reduce image resolution by 4 times
            case "Low":
                img = self.updated_image.reduce(8)  # reduce image resolution by 8 times
            case _:
                img = self.original_image

        self.canvas.delete("all")
        self.loadImage(img)


if __name__ == "__main__":
    root = Tk()
    app = FirstWindow(root)
    root.mainloop()
