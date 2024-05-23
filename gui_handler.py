from tkinter import Tk, messagebox, filedialog, StringVar, Label


class GUIHandler:
    # TODO: Add showing message by error_code and ask_code. Make the content dependent on the local language
    def __init__(self) -> None:
        self.__root: Tk = Tk("MasterTester")
        self.__info_text: StringVar = StringVar()
        Label(self.__root, textvariable=self.__info_text, font=("Arial", 15)).pack(pady=20)

    def showError(self, message: str) -> None:
        messagebox.showerror('Error', message)
        exit(1)

    def chooseExeFile(self) -> str:
        return filedialog.askopenfilename(title='Select .exe file to test', filetypes=[('Executable file', '*.exe')])

    def askOkCancel(self, ask: str) -> bool:
        return messagebox.askokcancel('No data', ask)

    def loop(self) -> None:
        self.__root.mainloop()

    @property
    def info_text(self) -> str:
        return str(self.__info_text)

    @info_text.setter
    def info_text(self, new_info: str):
        self.__info_text.set(new_info)
        self.__root.update()
