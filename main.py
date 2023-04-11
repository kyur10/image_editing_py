# import the required libraries
from tkinter import Tk
import db
from FirstWindow import FirstWindow

root = Tk()


if __name__ == "__main__":
    # db.insert()
    # db.fetch()
    # db.update()
    # db.delete()
    # data = db.fetch()
    # for i in data:
    #     print(i)
    # db.createTable()

    app = FirstWindow(root)
    root.mainloop()

