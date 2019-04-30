from TextManager import TextManager
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
import tkinter as tk


class WritingBuddy(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.switch_frame(GreetingPage)
        self.text_manager = None

    def switch_frame(self, page) -> None:
        new_page = page(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_page


class GreetingPage(tk.Frame):

    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.master = master
        master.title("WritingBuddy")

        mainframe = ttk.Frame(master, padding="6 6 24 24")
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        master.columnconfigure(0, weight=1)
        master.rowconfigure(0, weight=1)

        self.path = StringVar()

        self.file_entry = ttk.Entry(mainframe, width=15, textvariable=self.path)
        self.file_entry.grid(column=1, row=2, sticky=(W, E))
        ttk.Button(mainframe, text="Go",
                   command=self.store_text).grid(column=1, row=3, sticky=W)

        ttk.Button(mainframe, text="Browse",
                   command=self.get_file_path).grid(column=2, row=2, sticky=W)

        ttk.Label(mainframe, text="Where is your story at?").grid(column=1, row=1, sticky=W)

        for child in mainframe.winfo_children():
            child.grid_configure(padx=5, pady=5)

        self.file_entry.focus()
        master.bind('<Return>', self.store_text)

    def store_text(self, *args) -> None:
        self.master.text_manager = TextManager(self.path.get())
        self.master.switch_frame(OptionPage)

    def get_file_path(self, *args) -> None:
        self.file_entry.delete(0, END)
        path = filedialog.askopenfilename(initialdir="/", title="Select file",
                                          filetypes=(("docx files", "*.docx"), ("all files", "*.*")))
        self.file_entry.insert(0, path)


class OptionPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.master = master
        master.title("WritingBuddy")

        mainframe = ttk.Frame(master, padding="12 12 24 24")
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        master.columnconfigure(0, weight=1)
        master.rowconfigure(0, weight=1)

        self.output = ""

        ttk.Label(mainframe, text="What can I help you with?").grid(column=1, row=1, sticky=W)
        ttk.Button(mainframe, text="Make me a word cloud",
                   command=self.master.text_manager.show_word_cloud).grid(column=1, row=2, sticky=W)
        ttk.Button(mainframe, text="Tell what words I use the most",
                   command=self.get_common_words).grid(column=1, row=3, sticky=W)
        ttk.Button(mainframe, text="Let me pick a different story",
                   command=self.switch_docs).\
            grid(column=1, row=4, sticky=W)

        ttk.Label(mainframe, text=self.output).grid(column=1, row=5, sticky=W)

    def get_common_words(self):
        self.output = self.master.text_manager.get_common_words

    def switch_docs(self):
        self.master.switch_frame(GreetingPage)


if __name__ == "__main__":
    buddy = WritingBuddy()
    buddy.mainloop()
