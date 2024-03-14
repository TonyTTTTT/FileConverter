import tkinter as tk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
import pdfplumber
from converter import *


class GUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Converter")
        # self.window.geometry("300x200")

        self.filename = None
        self.page_num = None
        self.save_path = None
        self.img_type = tk.StringVar()
        self.img_type_menu = None

        self.frame1 = tk.Frame(self.window)
        self.frame1.pack(fill='none', expand=True, ipadx=10, ipady=20, padx=20, pady=20)

        self.frame2 = tk.Frame(self.window)
        self.frame2.pack(fill='none', expand=True, ipadx=10, ipady=20, padx=20, pady=20)

        self.open_button = tk.Button(
            self.frame1,
            text='Select a File',
            command=self.select_file
        )
        self.open_button.pack(expand=True)

        self.list = tk.Listbox(self.frame1, selectmode='multiple', font=16)
        self.list.pack(expand=True)

        self.select_save_path_button = tk.Button(
            self.frame2,
            text='Select a Path to save',
            command=self.select_save_path
        )
        self.select_save_path_button.pack(expand=True)

        self.convert_button = tk.Button(
            self.frame2,
            text='convert',
            command=self.convert
        )
        self.convert_button.pack(expand=True)

        self.window.mainloop()

    def convert(self):
        pdf_converter = PDFConverter()
        pdf_converter.convert(self.filename, self.save_path, self.list.curselection(), self.img_type.get())

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

        if self.filename.split('.')[1] == 'pdf':
            pdf_file = pdfplumber.open(self.filename)
            total_pages = len(pdf_file.pages)
            self.update_list(total_pages)
            self.create_img_type_menu()

    def create_img_type_menu(self):
        if self.img_type_menu != None:
            self.img_type_menu.destroy()

        img_types = ['jpg', 'png']
        self.img_type.set('jpg')
        self.img_type_menu = tk.OptionMenu(self.frame1, self.img_type, *img_types)
        self.img_type_menu.pack(expand=True)

    def update_list(self, total_pages):
        self.list.delete(0, tk.END)
        for i in range(1, total_pages+1):
            self.list.insert(i, i)


if __name__ == '__main__':
    gui = GUI()
