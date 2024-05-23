from typing import *
import os
import subprocess

from test import Test
from gui_handler import GUIHandler


class MasterTester:
    def __init__(self) -> None:
        self.__gui_handler = GUIHandler()
        self.__file_selected: str = self.__gui_handler.chooseExeFile()

        if self.__file_selected == "":
            self.__gui_handler.showError("No file selected")

        self.__in_files: List[str] = list()
        self.__out_files: List[str] = list()

        self.__tests: List[Test] = list()

        self.__getInOutFilesNames()
        self.__validateFiles()

    def run(self) -> None:
        self.__doTests()
        self.printResults()

    def __getProgramOutput(self, data: str) -> str:
        result: subprocess.CompletedProcess[str] = subprocess.run([self.__file_selected],
                                                                  input=data,
                                                                  text=True,
                                                                  capture_output=True)

        return result.stdout

    def __getFileData(self, file_path: str) -> str:
        try:
            with open(file_path) as file:
                return file.read()
        except FileNotFoundError as e:
            self.__gui_handler.showError(f'Cannot find {e.filename}')
        except PermissionError as e:
            self.__gui_handler.showError(f'Permission denied to file {e.filename}')

    def __getInOutFilesNames(self) -> None:
        try:
            self.__in_files = os.listdir('in')
            self.__out_files = os.listdir('out')
        except FileNotFoundError as e:
            self.__gui_handler.showError(f'Cannot find folder {e.filename}')
        except PermissionError as e:
            self.__gui_handler.showError(f'Permission denied to folder {e.filename}')

    def __validateFiles(self) -> None:
        if len(self.__in_files) == 0:
            self.__gui_handler.showError('There are no tests to do')
        elif len(self.__in_files) != len(self.__out_files):
            self.__gui_handler.showError("There are different amounts of files in the 'in' and 'out' folders")

        in_file: str
        out_file: str
        for in_file, out_file in zip(self.__in_files, self.__out_files):
            in_file_data: List[str] = self.__getFileData(os.path.join("in", in_file)).split('\n\n')
            out_file_data: List[str] = self.__getFileData(os.path.join("out", out_file)).split('\n\n')

            if len(in_file_data) == 0:
                answer: bool = self.__gui_handler.askOkCancel(f"There is no input data in {in_file}. "
                                                              f"'ok' for continue and exclude this test, "
                                                              f"'cancel' for stop testing")
                if answer:
                    continue
                else:
                    exit(1)

            if len(out_file_data) == 0:
                answer: bool = self.__gui_handler.askOkCancel(f"There is no output data in {in_file}. "
                                                              f"'ok' for continue and exclude this test, "
                                                              f"'cancel' for stop testing")
                if answer:
                    continue
                else:
                    exit(1)

            if len(in_file_data) != len(out_file_data):
                answer: bool = self.__gui_handler.askOkCancel(f"In the input {in_file_data} and output file "
                                                              f"{out_file_data}, there is a different amount of data. "
                                                              f"'ok' for continue and exclude this test, 'cancel' "
                                                              f"for stop testing")
                if answer:
                    continue
                else:
                    exit(1)

            name: str = in_file.split('.')[0].replace("_in", "")

            self.__tests.append(Test(name, in_file_data, out_file_data))

    def __doTests(self) -> None:
        test: Test
        for test in self.__tests:
            for testcase in test.testcases:
                testcase.actual_out = self.__getProgramOutput(testcase.in_data)

    def printResults(self) -> None:
        for test in self.__tests:
            print(f'{test.name} -> {test.passed}')
            for testcase in test.testcases:
                print(f'\t{testcase.name} -> {testcase.passed}')
                print(f'\t\t{testcase.in_data} : {testcase.actual_out} : {testcase.out_data}')
            print()
