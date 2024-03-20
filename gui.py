import tkinter as tk
from builder import *


class GUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Converter")
        # self.window.geometry("300x200")

        self.use_case = tk.StringVar()

        self.frame1 = tk.Frame(self.window)
        self.frame1.pack(fill='none', expand=True, ipadx=10, ipady=20, padx=20, pady=20)

        self.frame2 = tk.Frame(self.window)
        self.frame2.pack(fill='none', expand=True, ipadx=10, ipady=20, padx=20, pady=20)

        self.frame3 = tk.Frame(self.window)
        self.frame3.pack(fill='none', expand=True, ipadx=10, ipady=20, padx=20, pady=20)

        self.use_cases = ['pdf2img', 'img2pdf']
        self.use_case_menu = tk.OptionMenu(self.frame1, self.use_case, *self.use_cases, command=self.refresh_session)
        self.use_case_menu.pack(expand=True)
        self.use_case.set(self.use_cases[0])
        self.builder = PDFBuilder(self.window)

        self.select_file_button = tk.Button(
            self.frame1,
            text='Select a File',
            command=self.builder.select_file
        )
        self.select_file_button.pack(expand=True)

        self.window.mainloop()

    def refresh_session(self, *args):
        for widget in self.frame2.winfo_children():
            widget.pack_forget()
        for widget in self.frame3.winfo_children():
            widget.pack_forget()

        if self.use_case.get() == self.use_cases[0]:
            self.builder = PDFBuilder(self.window)
        elif self.use_case.get() == self.use_cases[1]:
            self.builder = IMGBuilder(self.window)

        self.select_file_button.configure(command=self.builder.select_file)


if __name__ == '__main__':
    gui = GUI()
