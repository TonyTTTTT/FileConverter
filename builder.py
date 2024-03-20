import abc
import tkinter as tk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
import pdfplumber
from converter import *
from dragndrop_listbox import DragDropListbox


class Builder(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'build') and
                callable(subclass.build))

    def __init__(self, window):
        self.window = window
        self.frame2 = self.window.winfo_children()[1]
        self.frame3 = self.window.winfo_children()[2]

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
        self.list_label = None
        self.filenames = ''
        self.filenames_tkVar = tk.StringVar()
        self.list_label_tkVar = tk.StringVar()
        self.saved_filename_inputbox_label = None
        self.saved_filename_inputbox = None

    @abc.abstractmethod
    def select_file(self):
        return NotImplementedError

    @abc.abstractmethod
    def build_selecting_components(self):
        return NotImplementedError

    def build_list_label(self):
        if self.list_label is None:
            self.list_label = tk.Label(self.frame2, textvariable=self.list_label_tkVar)
            self.list_label.pack(expand=True)

    def build_set_save_path_btn(self):
        if self.set_save_path_button is None:
            self.set_save_path_button = tk.Button(
                self.frame3,
                text='Select a Path to save',
                command=self.set_save_path
            )
        self.set_save_path_button.pack(expand=True)

    def build_convert_btn(self):
        if self.convert_button is None:
            self.convert_button = tk.Button(
                self.frame3,
                text='convert',
                command=self.convert
            )
        self.convert_button.pack(expand=True)

    def show_filename(self):
        if self.filename_label is None:
            self.filename_label = tk.Label(self.frame2, textvariable=self.filenames_tkVar, wraplength=200)
        self.filename_label.pack(expand=True)
        self.filenames_tkVar.set(self.filenames)

    def if_file_selected(self):
        if self.filenames == '':
            showinfo(title='Error', message='No file selected!')
            return False
        else:
            self.show_filename()
            return True

    def set_save_path(self):
        self.save_path = fd.askdirectory(
            title='Choose a dir',
            initialdir='./', )

        if self.save_path == '':
            showinfo(title='Error', message='No path selected!')
        else:
            self.show_save_path()
            self.build_convert_btn()

    def show_save_path(self):
        if self.save_path_label is None:
            self.save_path_label = tk.Label(self.frame3, textvariable=self.save_path_tkVar, wraplength=200)
        self.save_path_label.pack(expand=True)
        self.save_path_tkVar.set(self.save_path)

    @abc.abstractmethod
    def convert(self):
        raise NotImplementedError

    @staticmethod
    def check_converted(success):
        if success:
            showinfo(title='Complete', message='Success convert!')
        else:
            showinfo(title='Error', message='Convert Failed!')


class PDFBuilder(Builder):
    def select_file(self):
        filetypes = (
            ('pdf files', '*.pdf'),
            ('All files', '*.*')
        )

        self.filenames = fd.askopenfilename(
            title='Select one pdf file',
            initialdir='./',
            filetypes=filetypes)

        if self.if_file_selected():
            self.build_selecting_components()

            pdf_file = pdfplumber.open(self.filenames)
            total_pages = len(pdf_file.pages)

            self.update_list(total_pages)
            self.build_img_type_menu()

    def build_selecting_components(self):
        self.build_list_label()
        self.list_label_tkVar.set('Pages:')

        if self.list is None:
            self.list = tk.Listbox(self.frame2, selectmode='multiple', font=16)
        self.list.pack(expand=True)

        self.build_set_save_path_btn()

    def convert(self):
        converter = PDFConverter()
        success = converter.convert(self.filenames, self.save_path, self.list.curselection(), self.img_type.get())

        self.check_converted(success)

    def update_list(self, total_pages):
        self.list.delete(0, tk.END)
        for i in range(1, total_pages + 1):
            self.list.insert(i, i)

    def build_img_type_menu(self):
        img_types = ['jpg', 'png']
        if self.img_type_menu is None:
            self.img_type_menu = tk.OptionMenu(self.frame2, self.img_type, *img_types)
            self.img_type.set(img_types[0])
        self.img_type_menu.pack(expand=True)


class IMGBuilder(Builder):
    def select_file(self):
        filetypes = (
            ('img files', '*.jpg *.png'),
            ('All files', '*.*')
        )

        self.filenames = fd.askopenfilenames(
            title='Select one or multiple img file',
            initialdir='./',
            filetypes=filetypes)

        if self.if_file_selected():
            self.build_selecting_components()

            self.update_list()
            self.build_saved_filename_inputbox()

    def build_selecting_components(self):
        self.build_list_label()
        self.list_label_tkVar.set('Pages arrange:')

        if self.list is None:
            self.list = DragDropListbox(self.frame2, selectmode='multiple', font=16)
        self.list.pack(expand=True)

        self.build_set_save_path_btn()

    def convert(self):
        converter = IMGConverter()
        success = converter.convert(self.filenames, self.save_path, self.list.get(0, tk.END),
                                    self.saved_filename_inputbox.get())

        self.check_converted(success)

    def update_list(self):
        self.list.delete(0, tk.END)
        for i in range(0, len(self.filenames)):
            filename = os.path.split(self.filenames[i])[1]
            self.list.insert(i, filename)

    def build_saved_filename_inputbox(self):
        if self.saved_filename_inputbox_label is None:
            self.saved_filename_inputbox_label = tk.Label(self.frame2, text='saved filename:')
        self.saved_filename_inputbox_label.pack(expand=True)

        if self.saved_filename_inputbox is None:
            self.saved_filename_inputbox = tk.Entry(self.frame2)
            self.saved_filename_inputbox.insert(0, 'IMGs')
        self.saved_filename_inputbox.pack(expand=True)
