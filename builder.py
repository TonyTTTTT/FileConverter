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
            self.refresh_session()
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

    def refresh_session(self):
        for widget in self.frame2.winfo_children():
            widget.pack_forget()
        for widget in self.frame3.winfo_children():
            widget.pack_forget()


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
        self.list_label_tkVar.set('Pages select:')

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
    def __init__(self, window):
        super().__init__(window)
        self.saved_filename_inputbox_label = None
        self.saved_filename_inputbox = None
        self.default_saved_filename = tk.StringVar()

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
            self.build_saved_filename_inputbox()
            self.build_selecting_components()

            self.update_list()

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
            self.saved_filename_inputbox_label = tk.Label(self.frame3, text='saved filename:')
        self.saved_filename_inputbox_label.pack(expand=True)

        if self.saved_filename_inputbox is None:
            self.saved_filename_inputbox = tk.Entry(self.frame3)
            self.saved_filename_inputbox.insert(0, 'IMGs')
        self.saved_filename_inputbox.pack(expand=True)


class CombinerBuilder(IMGBuilder):
    def __init__(self, window):
        super().__init__(window)
        self.insert_pages_menu = None
        self.insert_page = tk.StringVar()
        self.insert_pages_menu_label = None
        self.insert_checkbox = None
        self.insert_is_check = tk.BooleanVar()

    def select_file(self):
        filetypes = (
            ('img files', '*.pdf'),
            ('All files', '*.*')
        )

        self.filenames = fd.askopenfilenames(
            title='Select multiple PDF files',
            initialdir='./',
            filetypes=filetypes)

        if self.if_file_selected():
            self.build_saved_filename_inputbox()
            self.saved_filename_inputbox.delete(0, tk.END)
            self.saved_filename_inputbox.insert(0, 'Combined')

            self.build_selecting_components()
            self.list_label_tkVar.set('PDF files arrange:')

            if len(self.filenames) == 2:
                self.build_insert_checkbox()
            else:
                self.hide_insert_checkbox()
                self.hide_insert_pages_menu()

            self.update_list()

    def if_file_selected(self):
        if len(self.filenames) < 2:
            showinfo(title='Error', message='Please select at least 2 PDF files!')
            self.refresh_session()
            return False
        else:
            self.show_filename()
            return True

    def convert(self):
        converter = PDFCombiner()
        if len(self.filenames) == 2 and self.insert_is_check.get():
            success = converter.convert(self.filenames, self.save_path, self.list.get(0, tk.END),
                          self.saved_filename_inputbox.get(), int(self.insert_page.get()))
        else:
            success = converter.convert(self.filenames, self.save_path, self.list.get(0, tk.END),
                                        self.saved_filename_inputbox.get())

        self.check_converted(success)

    def get_first_PDF_total_pages(self):
        first_pdf_file = self.list.get(0)
        if first_pdf_file in self.filenames[0]:
            first_pdf_file = self.filenames[0]
        else:
            first_pdf_file = self.filenames[1]

        pdf_file = pdfplumber.open(first_pdf_file)
        total_pages = len(pdf_file.pages)
        return total_pages

    def build_insert_checkbox(self):
        if self.insert_checkbox is None:
            self.insert_checkbox = tk.Checkbutton(self.frame2, text='Insert before page:', variable=self.insert_is_check,
                                                  onvalue=1, offvalue=0, command=self.check_insert)
        self.insert_checkbox.pack(expand=True)

    def check_insert(self):
        if self.insert_is_check.get():
            self.build_insert_pages_menu()
            self.list.bind('<Leave>', self.update_insert_pages_menu)
        else:
            self.hide_insert_pages_menu()

    def build_insert_pages_menu(self):
        total_pages = self.get_first_PDF_total_pages()
        pages = [i for i in range(1, total_pages+1)]
        if self.insert_pages_menu is None:
            self.insert_pages_menu = tk.OptionMenu(self.frame2, self.insert_page, *pages)
            self.insert_page.set(pages[0])
        self.insert_pages_menu.pack(expand=True)

    def update_insert_pages_menu(self, *args):
        total_pages = self.get_first_PDF_total_pages()
        pages = [i for i in range(1, total_pages + 1)]

        self.insert_pages_menu['menu'].delete(0, tk.END)

        for page in pages:
            self.insert_pages_menu['menu'].add_command(label=page, command=tk._setit(self.insert_page, page))

    def hide_insert_pages_menu(self):
        if self.insert_pages_menu is not None:
            self.insert_pages_menu.pack_forget()

    def hide_insert_checkbox(self):
        if self.insert_checkbox is not None:
            self.insert_checkbox.pack_forget()