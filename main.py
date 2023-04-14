# import the required libraries
from tkinter import Tk
import db
from ImageFilter import FirstWindow

root = Tk()


if __name__ == "__main__":
    # db.createTable()
    app = FirstWindow(root)
    root.mainloop()

