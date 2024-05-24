import os
from tkinter import Tk, messagebox, filedialog, StringVar, Label, Entry, Button
from functools import partial
from mastertester import MasterTester
from typing import *
from const import *


class GUIHandler:
    # TODO: Make the content dependent on the local language
    def __init__(self) -> None:
        self.__root: Tk = Tk()
        self.__root.title('MasterTester')
        self.__root.resizable(False, False)
        self.__root.iconbitmap('icon.ico')

        Label(self.__root, text='MasterTester', font=('Arial', 23)).pack(pady=40, padx=20)
        Label(self.__root, text='Welcome to MasterTester', font=('Arial', 15)).pack(pady=20, padx=20)

        Label(self.__root, text='*.exe file path', font=('Arial', 13)).pack()
        self.__exe_path_var: StringVar = StringVar()
        Button(self.__root, text='Select', command=partial(self.__chooseExeFile,
                                                           self.__exe_path_var,
                                                           'Select .exe file to test',
                                                           [('Executable file', '*exe')])).pack()
        Entry(self.__root, textvariable=self.__exe_path_var, state='disabled', width=40).pack(pady=20)

        Label(self.__root, text='Input files folder path', font=('Arial', 13)).pack()
        self.__in_folder_path: StringVar = StringVar(value=os.path.join(os.getcwd(), 'in'))
        Button(self.__root, text='Select', command=partial(self.__chooseExeFile,
                                                           self.__in_folder_path,
                                                           'Select folder with inputs')).pack()
        Entry(self.__root, textvariable=self.__in_folder_path, state='disabled', width=40).pack(pady=20)

        Label(self.__root, text='Output files folder path', font=('Arial', 13)).pack()
        self.__out_folder_path: StringVar = StringVar(value=os.path.join(os.getcwd(), 'out'))
        Button(self.__root, text='Select', command=partial(self.__chooseExeFile,
                                                           self.__out_folder_path,
                                                           'Select folder with outputs')).pack()
        Entry(self.__root, textvariable=self.__out_folder_path, state='disabled', width=40).pack(pady=20)

        Label(self.__root, text='Results folder path', font=('Arial', 13)).pack()
        self.__results_folder_path: StringVar = StringVar(value=os.path.join(os.getcwd(), 'results'))
        Button(self.__root, text='Select', command=partial(self.__chooseExeFile,
                                                           self.__results_folder_path,
                                                           'Select a folder to save the results')).pack()
        Entry(self.__root, textvariable=self.__results_folder_path, state='disabled', width=40).pack(pady=20)

        Button(self.__root, text='Start testing', font=('Arial', 15), command=self.__startTests).pack(pady=30)

        self.__info: StringVar = StringVar()
        self.__info.trace_add('write', self.__infoCallback)
        Label(self.__root, textvariable=self.__info, font=("Arial", 13)).pack(pady=10)

    def __startTests(self) -> None:
        if len(self.__exe_path_var.get()) == 0:
            self.__showInfo('Path to *.exe file is missing', )
            return
        if len(self.__in_folder_path.get()) == 0:
            self.__showInfo('Folder with inputs is missing', )
            return
        if len(self.__out_folder_path.get()) == 0:
            self.__showInfo('Folder with outputs is missing', )
            return

        if self.__in_folder_path.get() == self.__out_folder_path.get():
            self.__showInfo('Folder with input files and outputs must be different', )
            return

        tester: MasterTester = MasterTester(self.__exe_path_var,
                                            self.__in_folder_path,
                                            self.__out_folder_path,
                                            self.__results_folder_path,
                                            self.__info)

        error_pack: Tuple[int, str] | int = tester.run()
        self.__info.set('')
        self.__root.update()
        if type(error_pack) is int and error_pack == NO_ERROR:
            self.__showInfo('All done!')
        else:
            self.__errorsHandle(error_pack)

    def __errorsHandle(self, error_pack: Tuple[int, str] | int):
        error_code: int
        error_add: str = 'UNDEFINED'

        if type(error_pack) is tuple:
            error_code, error_add = error_pack
        else:
            error_code = error_pack

        if error_code == FILE_NOT_FOUND:
            self.__showError(f'File {error_add} not found')
        elif error_code == PERMISSION_DENIED:
            self.__showError(f'Permission denied to {error_add}')
        elif error_code == WRONG_FILES_NAMES:
            self.__showError(f'Files {error_add} has wrong names')
        elif error_code == NO_TESTS:
            self.__showError('There is no tests to do')
        elif error_code == DIFFERENT_FILES_NUM:
            self.__showError(f'There is different number of *.txt files '
                             f'in {self.__in_folder_path.get()} and {self.__out_folder_path.get()}')
        elif error_code == NO_FILE_DATA:
            self.__showError(f'There is no data in {error_add}')
        elif error_code == DIFFERENT_DATA_NUM:
            self.__showError(f'In {error_add} files, '
                             f'the number of input data does not correspond to the number of output data')
        else:
            self.__showError(f'Unknown error {error_code} {error_add}')

    @staticmethod
    def __showError(message: str) -> None:
        messagebox.showerror('Error', message)

    @staticmethod
    def __showInfo(message: str) -> None:
        messagebox.showinfo('Info', message)

    def __chooseExeFile(self, path_var: StringVar, title: str, file_types: List[Tuple[str, str]] | None = None):
        if file_types is not None:
            path: str = filedialog.askopenfilename(title=title, filetypes=file_types)
        else:
            path: str = filedialog.askdirectory(title=title)

        if len(path) > 0:
            path_var.set(path)
            self.__root.update()

    def __infoCallback(self, *args):
        self.__info.set(self.__info.get())
        self.__root.update()

    def loop(self) -> None:
        self.__root.mainloop()
