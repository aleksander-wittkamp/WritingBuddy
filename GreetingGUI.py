from TextManager import TextManager
from tkinter import *
from tkinter import filedialog
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

        self.file_entry = ttk.Entry(mainframe, width=15, textvariable=self.path)
        self.file_entry.grid(column=1, row=2, sticky=(W, E))
        ttk.Button(mainframe, text="Go",
                   command=self.store_file_path).grid(column=1, row=3, sticky=W)

        ttk.Button(mainframe, text="Browse",
                   command=self.get_file_path).grid(column=2, row=2, sticky=W)

        ttk.Label(mainframe, text="Can I get your file path?").grid(column=1, row=1, sticky=W)

        for child in mainframe.winfo_children():
            child.grid_configure(padx=5, pady=5)

        self.file_entry.focus()
        root.bind('<Return>', self.store_file_path)

    def store_file_path(self, *args) -> None:
        self.text_manager = TextManager(self.path.get())
        print(self.text_manager.get_paragraphs())

    def get_file_path(self, *args) -> None:
        self.file_entry.delete(0, END)
        path = filedialog.askopenfilename(initialdir="/", title="Select file",
                                          filetypes=(("docx files", "*.docx"), ("all files", "*.*")))
        self.file_entry.insert(0, path)


if __name__ == "__main__":
    root = Tk()
    greeting_gui = GreetingGUI(root)
    root.mainloop()

