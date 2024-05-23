import time
from typing import *
import os
import subprocess

from test import Test
from testcase import Testcase
from HTMLGenerator import HTMLGenerator
from tkinter import StringVar
from const import *
from bs4 import BeautifulSoup, Tag
from datetime import datetime


class MasterTester:
    def __init__(self,
                 exe_path: StringVar,
                 in_folder_path: StringVar,
                 out_folder_path: StringVar,
                 result_folder_path: StringVar,
                 info: StringVar) -> None:

        self.__exe_path: str = exe_path.get()
        self.__in_folder_path: str = in_folder_path.get()
        self.__out_folder_path: str = out_folder_path.get()
        self.__result_folder_path: str = result_folder_path.get()
        self.__info: StringVar = info

        self.__in_files: List[str] = list()
        self.__out_files: List[str] = list()

        self.__tests: List[Test] = list()

    def run(self) -> int:
        error_pack: int | Tuple[int, str] = self.__getInOutFilesNames()
        if (type(error_pack) is int and error_pack != NO_ERROR) or type(error_pack) is tuple:
            return error_pack

        error_pack = self.__validateFiles()
        if (type(error_pack) is int and error_pack != NO_ERROR) or type(error_pack) is tuple:
            return error_pack

        try:
            if not os.path.exists(self.__result_folder_path):
                os.makedirs(self.__result_folder_path)
        except Any:
            raise NotImplemented

        self.__doTests()
        self.__info.set('Generating result file')

        now: datetime = datetime.now().replace(microsecond=0)
        now_str: str = now.strftime('%Y-%m-%d %H-%M-%S')
        bs4_results: BeautifulSoup = HTMLGenerator(self.__tests).generateResults()

        title_tag: Tag = bs4_results.find('title')
        title_tag.string = f'Result {now_str}'

        with open(os.path.join(self.__result_folder_path, f'Result {now_str}.html'), 'w', encoding='utf-8') as file:
            file.write(bs4_results.prettify())

        return NO_ERROR

    def __getProgramOutput(self, data: str) -> str | Tuple[int, str]:
        try:
            result: subprocess.CompletedProcess[str] = subprocess.run([self.__exe_path],
                                                                      input=data,
                                                                      text=True,
                                                                      capture_output=True)
        except PermissionError as e:
            return PERMISSION_DENIED, e.filename

        return result.stdout

    @staticmethod
    def __getFileData(file_path: str) -> str | Tuple[int, str]:
        try:
            with open(file_path) as file:
                return file.read()
        except FileNotFoundError as e:
            return FILE_NOT_FOUND, e.filename
        except PermissionError as e:
            return PERMISSION_DENIED, e.filename

    def __getInOutFilesNames(self) -> int | Tuple[int, str]:
        try:
            self.__in_files = os.listdir(self.__in_folder_path)
            self.__out_files = os.listdir(self.__out_folder_path)
        except FileNotFoundError as e:
            return FILE_NOT_FOUND, e.filename
        except PermissionError as e:
            return PERMISSION_DENIED, e.filename

        self.__in_files = [file for file in self.__in_files if file.split('.')[1] == 'txt']
        self.__out_files = [file for file in self.__out_files if file.split('.')[1] == 'txt']

        self.__in_files.sort()
        self.__out_files.sort()

        return NO_ERROR

    def __validateFiles(self) -> int | Tuple[int, str]:
        self.__info.set('Validating files...')
        
        if len(self.__in_files) == 0:
            return NO_TESTS
        elif len(self.__in_files) != len(self.__out_files):
            return DIFFERENT_FILES_NUM

        in_file: str
        out_file: str
        for in_file, out_file in zip(self.__in_files, self.__out_files):

            if in_file.replace('_in', '') != out_file.replace('_out', ''):
                return WRONG_FILES_NAMES, ' '.join([in_file, out_file])

            in_file_data: List[str] = self.__getFileData(os.path.join(self.__in_folder_path, in_file)).split('\n\n')
            out_file_data: List[str] = self.__getFileData(os.path.join(self.__out_folder_path, out_file)).split('\n\n')

            if len(in_file_data) == 0:
                return NO_FILE_DATA, in_file

            if len(out_file_data) == 0:
                return NO_FILE_DATA, out_file

            if len(in_file_data) != len(out_file_data):
                return DIFFERENT_DATA_NUM, ' '.join([in_file, out_file])

            name: str = in_file.split('.')[0].replace("_in", "")

            self.__tests.append(Test(name, in_file_data, out_file_data))

        return NO_ERROR

    def __doTests(self) -> None:
        test: Test
        for test in self.__tests:

            testcase: Testcase
            for testcase in test.testcases:
                self.__info.set(f'Test: {test.name}\nTestcase: {testcase.name}')

                testcase.actual_out = self.__getProgramOutput(testcase.in_data)

    def __printResults(self) -> None:
        for test in self.__tests:
            print(f'{test.name} -> {test.passed}')
            for testcase in test.testcases:
                print(f'\t{testcase.name} -> {testcase.passed}')
                print(f'\t\t{testcase.in_data} : {testcase.actual_out} : {testcase.out_data}')
            print()
