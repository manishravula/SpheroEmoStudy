from Tkinter import *

# my_intensity = 0
LIKERT_TAGS = ['VERY_LIGHT','LIGHT','MEDIUM','STRONG','VERY_STRONG']
FEELINGS = ['Happy','Sad','Confusion','Other']

class Application(Frame):

    def __init__(self ,logfilename):
        root = Tk()
        root.resizable(width=False, height=False)
        root.geometry('{}x{}'.format(1200, 400))
        Frame.__init__(self)
        self.master = root
        self.pack()
        self.create_widgets()
        self.file = open(logfilename+'.txt','a')
        self.collected_data = []


    def create_widgets(self):

        self.winfo_toplevel().title("Sphero Test Application")
        w = Text(self.master)
        w.tag_configure("center", justify="center")
        w.insert(INSERT, "What emotion do you think the Sphero is expressing right now?")
        w.config(font=("Courier", 15))
        w.tag_add("center", "1.0", "end")
        w.pack()


        self.QUIT = Button(self)
        self.QUIT["text"] = "QUIT THE PROGRAM"
        self.QUIT["fg"] = "red"
        self.QUIT["command"] = self.quit
        self.QUIT.config(height = 5, width = 20)
        # self.QUIT.config(height=200, width=100)
        self.QUIT.pack({"side": "right"})


        class button_callback():
            def __init__(self,callmethod,feeling_name):
                self.feeling_name = feeling_name
                self.call_method= callmethod

            def call_func(self):
                return self.call_method(self.feeling_name)


        for feeling_name in FEELINGS:
            curr_button = Button(self)
            curr_button["text"]=feeling_name
            def new_func():
                return self.create_window(feeling_name)
            obj = button_callback(self.create_window,feeling_name)
            curr_button["command"]= obj.call_func
            curr_button.config(height=5,width=20)
            curr_button.pack({"side": "left"})


    def create_window(self,feeling_name):

        t = Tk()
        self.t = t
        self.master.destroy()
        t.wm_title("Select the Intensity")

        if feeling_name is not "None_of_the_above":
            l = Label(t, text="Ok then, how strong do you think it is expressing the emotion '{}'?".format(feeling_name))
            l.config(font=("Courier", 20))
            l.pack(side="top", fill="both", expand=True, padx=100, pady=100)


            class button_callback():
                def __init__(self,callmethod,fname,intensityval):
                    self.call = callmethod
                    self.fname = fname
                    self.i = intensityval
                def callmethod(self):
                    self.call(self.fname,self.i)


            for intensity_likertTag,intensity_value in zip(LIKERT_TAGS,range(len(LIKERT_TAGS))):
                h1 = Button(t)
                h1["text"] = intensity_likertTag
                h1["fg"] = "red"
                h1.config(height=5, width=20)
                obj = button_callback(self.writeFile,feeling_name,intensity_value)
                h1["command"] = obj.callmethod
                h1.pack({"anchor": "center"})

        else:
            self.collected_data=[3,0]



    def writeFile(self,feeling_name,intensity_value):
        self.file.write("{} {} \n".format(feeling_name,intensity_value))
        self.collected_data = [FEELINGS.index(feeling_name),intensity_value]
        self.t.destroy()



def experiment(logfilename):
    app = Application(logfilename)
    app.mainloop()
    app.file.close()
    return app.collected_data

a = experiment('test')
print(a)