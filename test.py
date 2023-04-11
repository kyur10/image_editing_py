import tkinter as tk
import tkinter.font as tkFont

class App:
    def __init__(self, root):
        #setting title
        root.title("undefined")
        #setting window size
        width=800
        height=800
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        GListBox_95=tk.Listbox(root)
        GListBox_95["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=10)
        GListBox_95["font"] = ft
        GListBox_95["fg"] = "#333333"
        GListBox_95["justify"] = "center"
        GListBox_95.place(x=20,y=20,width=759,height=757)

        GLabel_802=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        GLabel_802["font"] = ft
        GLabel_802["fg"] = "#333333"
        GLabel_802["justify"] = "center"
        GLabel_802["text"] = "SN"
        GLabel_802.place(x=40,y=40,width=51,height=30)

        GLabel_656=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        GLabel_656["font"] = ft
        GLabel_656["fg"] = "#333333"
        GLabel_656["justify"] = "center"
        GLabel_656["text"] = "File Name"
        GLabel_656.place(x=120,y=40,width=70,height=25)

        GLabel_116=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        GLabel_116["font"] = ft
        GLabel_116["fg"] = "#333333"
        GLabel_116["justify"] = "center"
        GLabel_116["text"] = "Dimension"
        GLabel_116.place(x=260,y=40,width=70,height=25)

        GLabel_92=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        GLabel_92["font"] = ft
        GLabel_92["fg"] = "#333333"
        GLabel_92["justify"] = "center"
        GLabel_92["text"] = "Image"
        GLabel_92.place(x=390,y=40,width=70,height=25)

        GLabel_976=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        GLabel_976["font"] = ft
        GLabel_976["fg"] = "#333333"
        GLabel_976["justify"] = "center"
        GLabel_976["text"] = "Uploaded At"
        GLabel_976.place(x=530,y=40,width=70,height=25)

        GLabel_306=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        GLabel_306["font"] = ft
        GLabel_306["fg"] = "#333333"
        GLabel_306["justify"] = "center"
        GLabel_306["text"] = "Action"
        GLabel_306.place(x=680,y=40,width=70,height=25)
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
