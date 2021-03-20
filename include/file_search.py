import os
import os.path
from typing import Generator


class FileSearch:
    def __init__(self, path: str, deep_search: bool = True) -> None:
        self.path: str = path
        self.flag: bool = deep_search
        self.__setup(self.flag)

    def __setup(self, flag: bool) -> None:
        if flag:
            self.files = self.__d_search()
        else:
            self.files = self.__search()

    def __d_search(self) -> Generator[str]:
        for (root, path, files) in os.walk(self.path):
            for file in files:
                yield os.path.join(root, file)

    def __search(self) -> Generator[str]:
        for file in os.listdir(self.path):
            if os.path.isfile(os.path.join(self.path, file)):
                yield os.path.join(self.path, file)

    def out_data(self):
        return self.files