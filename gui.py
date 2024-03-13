import tkinter as tk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
import pdfplumber
from converter import *


class GUI:
    def __init__(self):
        self.filename = None
        self.page_num = None
        self.save_path = None

        self.window = tk.Tk()
        self.window.title("Converter")
        self.frame = tk.Frame(self.window)
        self.frame.pack(fill='none', expand=True, ipadx=10, ipady=20, padx=20, pady=20)
        # self.window.geometry("300x200")

        self.open_button = tk.Button(
            self.frame,
            text='Select a File',
            command=self.select_file
        )
        self.open_button.pack(expand=True)

        self.list = tk.Listbox(self.frame, selectmode='multiple', font=16)
        self.list.pack(expand=True)

        self.select_save_path_button = tk.Button(
            self.frame,
            text='Select a Path to save',
            command=self.select_save_path
        )
        self.select_save_path_button.pack(expand=True)

        self.convert_button = tk.Button(
            self.frame,
            text='convert',
            command=self.convert
        )
        self.convert_button.pack(expand=True)

        self.window.mainloop()

    def convert(self):
        pdf_converter = PDFConverter()
        pdf_converter.convert(self.filename, self.save_path, self.list.curselection(), 'jpg')

    def select_save_path(self):
        filetypes = (
            ('pdf files', '*.pdf'),
            ('All files', '*.*')
        )

        self.save_path = fd.askdirectory(
            title='Choose a dir',
            initialdir='./',)

        showinfo(
            title='Selected Path',
            message=self.save_path
        )

    def select_file(self):
        filetypes = (
            ('pdf files', '*.pdf'),
            ('All files', '*.*')
        )

        self.filename = fd.askopenfilename(
            title='Open a file',
            initialdir='./',
            filetypes=filetypes)

        showinfo(
            title='Selected File',
            message=self.filename
        )

        pdf_file = pdfplumber.open(self.filename)
        total_pages = len(pdf_file.pages)
        self.update_list(total_pages)

    def update_list(self, total_pages):
        self.list.delete(0, tk.END)
        for i in range(1, total_pages+1):
            self.list.insert(i, i)


if __name__ == '__main__':
    gui = GUI()
