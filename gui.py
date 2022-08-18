from Detector import main_app
from create_classifier import train_classifer
from create_dataset import start_capture
from telegrambot import handle
import tkinter as tk
from tkinter import font as tkfont
from tkinter import messagebox,PhotoImage

names = set() #create set object


class MainUI(tk.Tk):

    def __init__(self, *args, **kwargs): #*args (Non-Keyword Arguments) **kwargs (Keyword Arguments)
        tk.Tk.__init__(self, *args, **kwargs)
        global names
        

        #r for read ## with (To close the file automatically)
        with open("namelists.txt", "r") as f: 
            x = f.read()
            z = x.rstrip().split(" ")
            for i in z:
                names.add(i)
        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold")
        self.title("Face Recognition Door Lock") #title name on the frame
        self.resizable(False, False) #size of frame according to user needs
        self.geometry("500x250") #size of the frame
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.active_name = None
        container = tk.Frame(self)
        container.grid(sticky="nsew")
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        for F in (MainPage, FirstPage, SecondPage, ThirdPage, FourthPage, LastPage): 
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame("MainPage")

    def show_frame(self, page_name):
            frame = self.frames[page_name]
            frame.tkraise()

    def on_closing(self):

        if messagebox.askokcancel("Quit", "Are you sure?"):
            global names
            f =  open("namelists.txt", "a+") #a for append (insert at the end)
            for i in names:
                    f.write(i+" ")
            self.destroy()


class MainPage(tk.Frame):

        def __init__(self, parent, controller):
            tk.Frame.__init__(self, parent)
            self.controller = controller
            
            render = PhotoImage(file='mainmenu.png')#need to change new icon
            img = tk.Label(self, image=render)
            img.image = render
            img.grid(row=0, column=1, rowspan=4, sticky="nsew")
            label = tk.Label(self, text="        Main Menu        ", font=self.controller.title_font,fg="#263942")
            label.grid(row=0, sticky="ew")
            
            button1 = tk.Button(self, text="   Add New User  ", fg="#ffffff", bg="#5897ee",command=lambda: self.controller.show_frame("FirstPage"))
            button2 = tk.Button(self, text="   Check a User  ", fg="#ffffff", bg="#5897ee",command=lambda: self.controller.show_frame("SecondPage"))
            button3 = tk.Button(self, text="   Check Log  ", fg="#ffffff", bg="#5897ee",command=lambda: self.controller.show_frame("FourthPage"))
            
            
            button1.grid(row=1, column=0, ipady=3, ipadx=2)
            button2.grid(row=2, column=0, ipady=3, ipadx=2)
            button3.grid(row=3, column=0, ipady=3, ipadx=2)
            


        def on_closing(self):
            if messagebox.askokcancel("Quit", "Are you sure?"):
                global names
                with open("namelists.txt", "w") as f:
                    for i in names:
                        f.write(i + " ")
                self.controller.destroy()


class FirstPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        tk.Label(self, text="Enter the name", fg="#263942", font='Helvetica 14 bold').grid(row=0, column=0, pady=10, padx=5)
        self.user_name = tk.Entry(self, borderwidth=3, bg="lightgrey", font='Helvetica 11')
        self.user_name.grid(row=0, column=1, pady=10, padx=10)
        self.buttoncancel = tk.Button(self, text="Cancel", bg="#ffffff", fg="#263942", command=lambda: controller.show_frame("MainPage"))
        self.buttonnext = tk.Button(self, text="Next", fg="#ffffff", bg="#5897ee", command=self.start_training)
        self.buttoncancel.grid(row=1, column=0, pady=10, ipadx=5, ipady=4)
        self.buttonnext.grid(row=1, column=1, pady=10, ipadx=5, ipady=4)
    
    def start_training(self):
        global names
        if self.user_name.get() == "None":
            messagebox.showerror("Error!!!", "Name cannot be 'None'")
            return
        elif self.user_name.get() in names:
            messagebox.showerror("Error!!!", "User already exists!")
            return
        elif len(self.user_name.get()) == 0:
            messagebox.showerror("Error!!!", "Name cannot be empty!")
            return
        name = self.user_name.get()
        names.add(name)
        self.controller.active_name = name
        self.controller.frames["SecondPage"].refresh_names()
        self.controller.show_frame("ThirdPage")


class SecondPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        global names
        self.controller = controller
        tk.Label(self, text="Select user", fg="#263942", font='Helvetica 14 bold').grid(row=0, column=0, padx=10, pady=10)
        self.buttoncancel = tk.Button(self, text="Cancel", command=lambda: controller.show_frame("MainPage"), bg="#ffffff", fg="#263942")
        self.menuvar = tk.StringVar(self)
        self.dropdown = tk.OptionMenu(self, self.menuvar, *names)
        self.dropdown.config(bg="lightgrey")
        self.dropdown["menu"].config(bg="lightgrey")
        self.buttonnext = tk.Button(self, text="Next", command=self.nextfoo, fg="#ffffff", bg="#5897ee")
        self.dropdown.grid(row=0, column=1, ipadx=8, padx=10, pady=10)
        self.buttoncancel.grid(row=1, ipadx=5, ipady=4, column=0, pady=10)
        self.buttonnext.grid(row=1, ipadx=5, ipady=4, column=1, pady=10)

    def nextfoo(self):
        if self.menuvar.get() == "None":
            messagebox.showerror("ERROR!!!", "Name cannot be 'None'")
            return
        self.controller.active_name = self.menuvar.get()
        self.controller.show_frame("LastPage")

    def refresh_names(self):
        global names
        self.menuvar.set('')
        self.dropdown['menu'].delete(0, 'end')
        for name in names:
            self.dropdown['menu'].add_command(label=name, command=tk._setit(self.menuvar, name))

class ThirdPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.numimglabel = tk.Label(self, text="Number of images captured = 0", font='Helvetica 14 bold', fg="#263942")
        self.numimglabel.grid(row=0, column=0, columnspan=2, sticky="ew", pady=10)
        self.buttoncapture = tk.Button(self, text="Capture Data Set", fg="#ffffff", bg="#16ba73", command=self.captureimage)
        self.buttontrain = tk.Button(self, text="Train the Model", fg="#ffffff", bg="#46c263",command=self.trainmodel)
        self.buttoncapture.grid(row=1, column=0, ipadx=5, ipady=4, padx=10, pady=20)
        self.buttontrain.grid(row=1, column=1, ipadx=5, ipady=4, padx=10, pady=20)

    def captureimage(self):
        self.numimglabel.config(text=str("Captured Images = 0 "))
        messagebox.showinfo("INSTRUCTIONS", "We will capture 100 pictures of your front face. Make sure to take from different range after each 20 images captured.")
        x = start_capture(self.controller.active_name)
        self.controller.num_of_images = x
        self.numimglabel.config(text=str("Number of images captured = "+str(x)))

    def trainmodel(self):
        if self.controller.num_of_images < 101:
            messagebox.showerror("ERROR", "Not enough Data, Capture at least 100 images!")
            return
        train_classifer(self.controller.active_name)
        messagebox.showinfo("SUCCESS", "The dataset model has been successfully trained!")
        self.controller.show_frame("LastPage") #to show face recognition part. can be used at select user

class FourthPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.loglabel = tk.Label(self, text="Check Logs", font='Helvetica 14 bold', fg="#263942")
        self.loglabel.grid(row=0, column=0, columnspan=2, sticky="ew", pady=10)
        self.buttonknown = tk.Button(self, text="Check known log", fg="#ffffff", bg="#16ba73", command=self.on_known)
        self.buttonunknown = tk.Button(self, text="Check unknown log", fg="#ffffff", bg="#f23b2e",command=self.on_unknown)
        self.buttoncancel = tk.Button(self, text="Cancel", bg="#ffffff", fg="#263942", command=lambda: controller.show_frame("MainPage"))
        self.buttonknown.grid(row=1, column=0, ipadx=5, ipady=4, padx=10, pady=20)
        self.buttonunknown.grid(row=1, column=1, ipadx=5, ipady=4, padx=10, pady=20)
        self.buttoncancel.grid (row=1, column=2, ipadx=5, ipady=4, padx=10, pady=20)
        
    def on_known(self):
        f = open("/home/pi/PSM Facial Recognition/knownlogs.log","r")
        for x in f:
            print(x)
        f.close()
    
    def on_unknown(self):
        f = open("/home/pi/PSM Facial Recognition/unknownlogs.log","r")
        for x in f:
            print(x)
        f.close()

class LastPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        render = PhotoImage(file='face.png') #need to change new icon
        img = tk.Label(self, image=render)
        img.image = render
        img.grid(row=0, column=1, rowspan=4, sticky="nsew")

        label = tk.Label(self, text="  Face Recognition  ", font='Terminal 16 bold') #title name
        label.grid(row=0, sticky="ew")
        button1 = tk.Button(self, text="Start Camera", command=self.openwebcam, fg="#ffffff", bg="#5897ee") #button name
        button2 = tk.Button(self, text="Go to Home Page", command=lambda: self.controller.show_frame("MainPage"), bg="#ffffff", fg="#263942")

        #command=lambda used to pass the data to a callback function.
        
        button1.grid(row=1,column=0, sticky="ew", ipadx=5, ipady=4, padx=10, pady=10)
        button2.grid(row=2,column=0, sticky="ew", ipadx=5, ipady=4, padx=10, pady=10)

    def openwebcam(self):
        main_app(self.controller.active_name)
    


app = MainUI()
app.iconphoto(False, tk.PhotoImage(file='icon.ico')) #image at the title
app.mainloop()


