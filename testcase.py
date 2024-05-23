class Testcase:
    def __init__(self, name: str, in_data: str, out_data: str) -> None:
        self.__name: str = name
        self.__in_data: str = in_data
        self.__out_data: str = out_data

        self.__actual_out: str = str()
        self.__passed: bool = False

    @property
    def name(self) -> str:
        return self.__name

    @property
    def in_data(self) -> str:
        return self.__in_data

    @property
    def out_data(self) -> str:
        return self.__out_data

    @property
    def actual_out(self) -> str:
        return self.__actual_out

    @actual_out.setter
    def actual_out(self, actual_out: str) -> None:
        self.__actual_out = actual_out
        self.__passed = self.__out_data == self.__actual_out

    @property
    def passed(self) -> bool:
        return self.__passed