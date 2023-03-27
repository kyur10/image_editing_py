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

        GLabel_735=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        GLabel_735["font"] = ft
        GLabel_735["fg"] = "#333333"
        GLabel_735["justify"] = "center"
        GLabel_735["text"] = "label"
        GLabel_735.place(x=15,y=15,width=500,height=500)

        GButton_208=tk.Button(root)
        GButton_208["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times',size=10)
        GButton_208["font"] = ft
        GButton_208["fg"] = "#000000"
        GButton_208["justify"] = "center"
        GButton_208["text"] = "Upload"
        GButton_208.place(x=20,y=550,width=155,height=30)
        GButton_208["command"] = self.GButton_208_command

        GButton_228=tk.Button(root)
        GButton_228["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times',size=10)
        GButton_228["font"] = ft
        GButton_228["fg"] = "#000000"
        GButton_228["justify"] = "center"
        GButton_228["text"] = "Download"
        GButton_228.place(x=350,y=550,width=158,height=30)
        GButton_228["command"] = self.GButton_228_command

        GButton_843=tk.Button(root)
        GButton_843["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times',size=10)
        GButton_843["font"] = ft
        GButton_843["fg"] = "#000000"
        GButton_843["justify"] = "center"
        GButton_843["text"] = "Reset"
        GButton_843.place(x=20,y=630,width=153,height=30)
        GButton_843["command"] = self.GButton_843_command

        GButton_39=tk.Button(root)
        GButton_39["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times',size=10)
        GButton_39["font"] = ft
        GButton_39["fg"] = "#000000"
        GButton_39["justify"] = "center"
        GButton_39["text"] = "View History"
        GButton_39.place(x=350,y=630,width=157,height=30)
        GButton_39["command"] = self.GButton_39_command

        GLabel_595=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        GLabel_595["font"] = ft
        GLabel_595["fg"] = "#333333"
        GLabel_595["justify"] = "center"
        GLabel_595["text"] = "label"
        GLabel_595.place(x=530,y=10,width=143,height=30)

    def GButton_208_command(self):
        print("command")


    def GButton_228_command(self):
        print("command")


    def GButton_843_command(self):
        print("command")


    def GButton_39_command(self):
        print("command")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
