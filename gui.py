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
        self.filename_tkVar = tk.StringVar()
        self.page_num = None
        self.save_path = None
        self.save_path_tkVar = tk.StringVar()
        self.img_type = tk.StringVar()
        self.img_type_menu = None
        self.filename_label = None
        self.list = None
        self.set_save_path_button = None
        self.convert_button = None
        self.save_path_label = None
        self.page_label = None

        self.frame1 = tk.Frame(self.window)
        self.frame1.pack(fill='none', expand=True, ipadx=10, ipady=20, padx=20, pady=20)

        self.frame2 = tk.Frame(self.window)
        self.frame2.pack(fill='none', expand=True, ipadx=10, ipady=20, padx=20, pady=20)

        self.frame3 = tk.Frame(self.window)
        self.frame3.pack(fill='none', expand=True, ipadx=10, ipady=20, padx=20, pady=20)

        self.open_button = tk.Button(
            self.frame1,
            text='Select a File',
            command=self.add_file
        )
        self.open_button.pack(expand=True)

        self.window.mainloop()

    def add_file(self):
        filetypes = (
            ('pdf files', '*.pdf'),
            ('All files', '*.*')
        )

        self.filename = fd.askopenfilename(
            title='Open a file',
            initialdir='./',
            filetypes=filetypes)

        if self.filename == '':
            showinfo(title='Error', message='No file selected!')
        else:
            self.show_filename()
            self.create_selecting_components()

            if self.filename.split('.')[1] == 'pdf':
                pdf_file = pdfplumber.open(self.filename)
                total_pages = len(pdf_file.pages)
                self.update_list(total_pages)
                self.create_img_type_menu()

    def show_filename(self):
        if self.filename_label == None:
            self.filename_label = tk.Label(self.frame1, textvariable=self.filename_tkVar, wraplength=200)
            self.filename_label.pack(expand=True)
        self.filename_tkVar.set(self.filename)

    def set_save_path(self):
        self.save_path = fd.askdirectory(
            title='Choose a dir',
            initialdir='./',)

        if self.save_path == '':
            showinfo(title='Error', message='No path selected!')
        else:
            self.show_save_path()
            self.create_convert_btn()

    def show_save_path(self):
        if self.save_path_label == None:
            self.save_path_label = tk.Label(self.frame3, textvariable=self.save_path_tkVar, wraplength=200)
            self.save_path_label.pack(expand=True)
        self.save_path_tkVar.set(self.save_path)

    def create_selecting_components(self):
        if self.page_label == None:
            self.page_label = tk.Label(self.frame2, text='Pages:')
            self.page_label.pack(expand=True)
        if self.list == None:
            self.list = tk.Listbox(self.frame2, selectmode='multiple', font=16)
            self.list.pack(expand=True)

        if self.set_save_path_button == None:
            self.set_save_path_button = tk.Button(
                self.frame3,
                text='Select a Path to save',
                command=self.set_save_path
            )
            self.set_save_path_button.pack(expand=True)

    def update_list(self, total_pages):
        self.list.delete(0, tk.END)
        for i in range(1, total_pages+1):
            self.list.insert(i, i)

    def create_img_type_menu(self):
        img_types = ['jpg', 'png']
        if self.img_type_menu == None:
            self.img_type_menu = tk.OptionMenu(self.frame2, self.img_type, *img_types)
            self.img_type_menu.pack(expand=True)
        self.img_type.set(img_types[0])

    def create_convert_btn(self):
        if self.convert_button == None:
            self.convert_button = tk.Button(
                self.frame3,
                text='convert',
                command=self.convert
            )
            self.convert_button.pack(expand=True)

    def convert(self):
        pdf_converter = PDFConverter()
        success = pdf_converter.convert(self.filename, self.save_path, self.list.curselection(), self.img_type.get())
        if success:
            showinfo(title='Complete', message='Success convert!')
        else:
            showinfo(title='Error', message='Convert Failed!')

if __name__ == '__main__':
    gui = GUI()
