import tkinter as tk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
import pdfplumber
from converter import *


class DragDropListbox(tk.Listbox):
    """ A Tkinter listbox with drag'n'drop reordering of entries. """
    def __init__(self, master, **kw):
        kw['selectmode'] = tk.SINGLE
        tk.Listbox.__init__(self, master, kw)
        self.bind('<Button-1>', self.setCurrent)
        self.bind('<B1-Motion>', self.shiftSelection)
        self.curIndex = None

    def setCurrent(self, event):
        self.curIndex = self.nearest(event.y)

    def shiftSelection(self, event):
        i = self.nearest(event.y)
        if i < self.curIndex:
            x = self.get(i)
            self.delete(i)
            self.insert(i+1, x)
            self.curIndex = i
        elif i > self.curIndex:
            x = self.get(i)
            self.delete(i)
            self.insert(i-1, x)
            self.curIndex = i


class GUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Converter")
        # self.window.geometry("300x200")

        self.use_case = tk.StringVar()
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

        self.frame1 = tk.Frame(self.window)
        self.frame1.pack(fill='none', expand=True, ipadx=10, ipady=20, padx=20, pady=20)

        self.frame2 = tk.Frame(self.window)
        self.frame2.pack(fill='none', expand=True, ipadx=10, ipady=20, padx=20, pady=20)

        self.frame3 = tk.Frame(self.window)
        self.frame3.pack(fill='none', expand=True, ipadx=10, ipady=20, padx=20, pady=20)

        self.use_cases = ['pdf2img', 'img2pdf']
        self.use_case_menu = tk.OptionMenu(self.frame1, self.use_case, *self.use_cases, command=self.destroy_components)
        self.use_case_menu.pack(expand=True)
        self.use_case.set(self.use_cases[0])

        self.select_file_button = tk.Button(
            self.frame1,
            text='Select a File',
            command=self.select_file
        )
        self.select_file_button.pack(expand=True)

        self.window.mainloop()

    def destroy_components(self, *args):
        for widget in self.frame2.winfo_children():
            widget.pack_forget()
        for widget in self.frame3.winfo_children():
            widget.pack_forget()
        self.filenames_tkVar.set('')
        self.list = None

    def select_file(self):
        if self.use_case.get() == self.use_cases[0]:
            filetypes = (
                ('pdf files', '*.pdf'),
                ('All files', '*.*')
            )

            self.filenames = fd.askopenfilename(
                title='Select one pdf file',
                initialdir='./',
                filetypes=filetypes)
        elif self.use_case.get() == self.use_cases[1]:
            filetypes = (
                ('img files', '*.jpg *.png'),
                ('All files', '*.*')
            )

            self.filenames = fd.askopenfilenames(
                title='Select one or multiple img file',
                initialdir='./',
                filetypes=filetypes)


        if self.filenames == '':
            showinfo(title='Error', message='No file selected!')
        else:
            self.show_filename()
            self.create_selecting_components()

            if type(self.filenames) == tuple:
                self.update_imgs_list()
                self.create_saved_filename_inputbox()
            elif self.filenames.split('.')[1] == 'pdf':
                pdf_file = pdfplumber.open(self.filenames)
                total_pages = len(pdf_file.pages)
                self.update_pdf_list(total_pages)
                self.create_img_type_menu()

    # def create_add_file_btn(self):


    def show_filename(self):
        if self.filename_label == None:
            self.filename_label = tk.Label(self.frame1, textvariable=self.filenames_tkVar, wraplength=200)
        self.filename_label.pack(expand=True)
        self.filenames_tkVar.set(self.filenames)

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
        if self.list_label == None:
            self.list_label = tk.Label(self.frame2, textvariable=self.list_label_tkVar)
        if self.use_case.get() == self.use_cases[0]:
            self.list_label_tkVar.set('Pages:')
        elif self.use_case.get() == self.use_cases[1]:
            self.list_label_tkVar.set('Pages arrange:')
        self.list_label.pack(expand=True)

        if self.list == None:
            if self.use_case.get() == self.use_cases[0]:
                self.list = tk.Listbox(self.frame2, selectmode='multiple', font=16)
            elif self.use_case.get() == self.use_cases[1]:
                self.list = DragDropListbox(self.frame2, selectmode='multiple', font=16, )
        self.list.pack(expand=True)

        if self.set_save_path_button == None:
            self.set_save_path_button = tk.Button(
                self.frame3,
                text='Select a Path to save',
                command=self.set_save_path
            )
        self.set_save_path_button.pack(expand=True)

    def update_pdf_list(self, total_pages):
        self.list.delete(0, tk.END)
        for i in range(1, total_pages+1):
            self.list.insert(i, i)

    def update_imgs_list(self):
        self.list.delete(0, tk.END)
        for i in range(0, len(self.filenames)):
            filename = os.path.split(self.filenames[i])[1]
            self.list.insert(i, filename)

    def create_saved_filename_inputbox(self):
        self.saved_filename_inputbox_label = tk.Label(self.frame2, text='saved filename:')
        self.saved_filename_inputbox_label.pack(expand=True)
        self.saved_filename_inputbox = tk.Entry(self.frame2)
        self.saved_filename_inputbox.insert(0, 'IMGs')
        self.saved_filename_inputbox.pack(expand=True)

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
        if self.use_case.get() == self.use_cases[0]:
            converter = PDFConverter()
            success = converter.convert(self.filenames, self.save_path, self.list.curselection(), self.img_type.get())
        elif self.use_case.get() == self.use_cases[1]:
            converter = IMGConverter()
            success = converter.convert(self.filenames, self.save_path, self.list.get(0, tk.END), self.saved_filename_inputbox.get())

        if success:
            showinfo(title='Complete', message='Success convert!')
        else:
            showinfo(title='Error', message='Convert Failed!')

if __name__ == '__main__':
    gui = GUI()
