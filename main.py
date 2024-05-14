import os
import subprocess
from datetime import datetime
from bs4 import BeautifulSoup
from typing import *
from tkinter import messagebox


def getCppProgramOutput(data: str) -> str:
    result: subprocess.CompletedProcess[str] = subprocess.run(['ConsoleApplication1/x64/Debug/ConsoleApplication1'],
                                                              input=data,
                                                              text=True,
                                                              capture_output=True)

    return result.stdout


def getFileData(file_path: str) -> str:
    try:
        with open(file_path) as file:
            return file.read()
    except FileNotFoundError as e:
        messagebox.showerror('Error', f'Cannot find {e.filename}')
        exit(1)
    except PermissionError as e:
        messagebox.showerror('Error', f'Permission denied to file {e.filename}')
        exit(1)


def getInOutFoldersFilesNames() -> Tuple[List[str], List[str]]:
    try:
        in_files_names: List[str] = os.listdir('in')
        out_files_names: List[str] = os.listdir('out')
    except FileNotFoundError as e:
        messagebox.showerror('Error',
                             f'Cannot find folder {e.filename}')
        exit(1)
    except PermissionError as e:
        messagebox.showerror('Error',
                             f'Permission denied to folder {e.filename}')
        exit(1)

    if len(in_files_names) != len(out_files_names):
        messagebox.showerror('Error',
                             "There are different amounts of files in the 'in' and 'out' folders")
        exit(1)
    elif len(in_files_names) == 0:
        messagebox.showerror('Error',
                             'There are no tests to do')
        exit(1)

    return in_files_names, out_files_names


def prepareSoup() -> BeautifulSoup:
    today: datetime = datetime.now().replace(microsecond=0)
    styles: str = """
    body {
            margin: 0;
        }
        .accordion {
            width: 100vw;
        }
        .accordion-button, .sub-accordion-button {
            background: #f7f7f7;
            border: none;
            width: 100%;
            text-align: left;
            padding: 10px;
            cursor: pointer;
            outline: none;
        }

        .accordion-content, .sub-accordion-content {
            display: none;
            padding: 5px 10px;
        }

        .sub-accordion-content div {
            padding: 5px 0;
            cursor: pointer;
        }
    """
    js_script: str = """
    document.querySelectorAll('.accordion-button, .sub-accordion-button').forEach(button => {
        button.addEventListener('click', function() {
            let content = this.nextElementSibling;
            
            if (content.style.display === "block") {
                content.querySelectorAll(".sub-accordion-content").forEach(function (item) {
                    item.style.display = "none";
                });
                
                content.style.display = "none";
                
            } else {
                content.style.display = "block";
            }
        });
    });
    """

    prepared_content: str = f"""
    <html>
    <head>
        <title>Results {today}</title>
        <style>
        {styles}
        </style>
    </head>
    <body>
        <h1>Results {today}</h1>
        <div class="accordion">
        </div>
        <script>
        {js_script}
        </script>
    </body>
    </html>
    """
    prepared_soup: BeautifulSoup = BeautifulSoup(prepared_content,
                                                 'html.parser')

    return prepared_soup


def doTests() -> None:
    in_files_names: List[str]
    out_files_names: List[str]
    in_files_names, out_files_names = getInOutFoldersFilesNames()

    in_files_names.sort()
    out_files_names.sort()

    # result_html: BeautifulSoup = prepareSoup()

    in_file_name: str
    out_file_name: str
    for in_file_name, out_file_name in zip(in_files_names, out_files_names):
        in_data: str = getFileData(f'in/{in_file_name}')
        out_data: List[str] = getFileData(f'out/{out_file_name}').split('\n\n')

        program_output: str = getCppProgramOutput(in_data)

        in_data: List[str] = in_data.split('\n\n')


def main() -> None:
    instruction: str = "1. The input files should be in the 'in' folder, while the files with the expected output should be in the 'out' folder. The folders should always contain an equal number of files.\n\n" \
                       "2. The names of the corresponding input and output files should differ only by the addition of '_in' and '_out' in their names or not at all.\n\n" \
                       "3. The individual test cases should be separated by a blank line in both the input files and the files with the expected output.\n\n" \
                       "4. The result files appear in the 'results' folder. Their names will be created from part of the input file name and the start time of the test run.\n\n" \
                       "5. Test cases will be numbered starting from 1, unless the input file has the addition %name: nameOfTestCase% before each test case. Only letters and numbers are allowed in test case names.\n\n\n" \
                       "Click 'Yes' if your files are prepared according to the above guidelines, otherwise click 'No'."

    if messagebox.askquestion('Are You prepared?', instruction) == 'yes':
        doTests()


if __name__ == '__main__':
    main()
