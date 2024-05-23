from tkinter import messagebox
from tkinter import filedialog


class GUIHandler:
    def __init__(self) -> None:
        pass

    def showError(self, message: str) -> None:
        messagebox.showerror("Error", message)
        exit(1)

    def chooseExeFile(self) -> str:
        return filedialog.askopenfilename(title="Select .exe file to test", filetypes=[("Executable file", "*.exe")])

    def askOkCancel(self, ask: str) -> bool:
        return messagebox.askokcancel("No data", ask)

