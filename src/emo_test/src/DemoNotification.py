from Tkinter import *
import time


class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.create_widgets()
        self.label = Label(self, text="", width=10)
        self.label.config(font=("Helvetica bold", 40))
        self.label.config(pady=100)
        self.label.pack()
        self.remaining = 0
        self.countdown(2)

    def create_widgets(self):
        self.winfo_toplevel().title("Experiment Notification")
        w = Text()
        w.tag_configure("center", justify="center")
        w.insert(INSERT, "The Experiment is about to begin! Ready? \n \n Go!")
        w.config(font=("Arial bold", 40))
        w.config(pady=150)
        w.tag_add("center", "1.0", "end")
        w.pack()

    def countdown(self, remaining=None):
        if remaining is not None:
            self.remaining = remaining

        if self.remaining <= 0:
            self.label.configure(text="time's up!")
        else:
            self.label.configure(text="%d" % self.remaining)
            self.remaining = self.remaining - 1
            self.after(1000, self.countdown)


def show_experiment_notification():
    root = Tk()
    root.attributes("-fullscreen", True)
    root.geometry('{}x{}'.format(600, 200))
    app = Application(master=root)
    root.after(2000, lambda: root.destroy())  # Destroy the widget after 30 seconds
    app.mainloop()


# show_experiment_notification()

