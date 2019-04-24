from WritingBuddy.TextManager import TextManager
from tkinter import *
from tkinter import ttk


class GreetingGUI:

    def __init__(self, master):
        self.text_manager = None
        self.master = master
        master.title("WritingBuddy")

        mainframe = ttk.Frame(root, padding="3 3 12 12")
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        self.path = StringVar()

        file_entry = ttk.Entry(mainframe, width=35, textvariable=self.path)
        file_entry.grid(column=2, row=1, sticky=(W, E))
        ttk.Button(mainframe, text="Go",
                   command=self.store_file_path).grid(column=3, row=1, sticky=W)

        ttk.Label(mainframe, text="Can I get your file path?").grid(column=1, row=1, sticky=W)

        for child in mainframe.winfo_children():
            child.grid_configure(padx=5, pady=5)

        file_entry.focus()
        root.bind('<Return>', self.store_file_path)

    def store_file_path(self, *args) -> None:
        self.text_manager = TextManager(self.path.get())
        print(self.text_manager.get_paragraphs())


if __name__ == "__main__":
    root = Tk()
    greeting_gui = GreetingGUI(root)
    root.mainloop()

