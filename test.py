from typing import *
from testcase import Testcase


class Test:
    def __init__(self, name: str, in_data: List[str], out_data: List[str]) -> None:
        self.__name: str = name

        self.__passed: bool = False
        self.__testcases: List[Testcase] = list()

        i: int
        in_: str
        out_: str
        for i, in_, out_ in zip(range(len(in_data)), in_data, out_data):
            first_line: str
            main_test: str
            name: str | None = None
            in_split: List[str] = in_.split('\n', 1)

            if len(in_split) > 1:
                first_line, main_test = in_split

                if first_line[0] == first_line[-1] == '%':
                    name = first_line[1:-1]
                    in_ = main_test
                else:
                    name = f"Testcase {i + 1}"

            if name is None:
                name = f"Testcase {i + 1}"

            self.__testcases.append(Testcase(name, in_, out_))

    def passCheck(self) -> None:
        self.__passed = False not in [case.passed for case in self.__testcases]

    @property
    def name(self) -> str:
        return self.__name

    @property
    def passed(self) -> bool:
        return self.__passed

    @property
    def testcases(self) -> List[Testcase]:
        return self.__testcases
