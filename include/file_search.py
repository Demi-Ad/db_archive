import os
import os.path
from typing import Generator, List, Tuple, Set, Union


class FileSearch:
    """
    폴더를 검사하여 파일들의 경로, 파일들의 확장자를 찾습니다.
    """
    def __init__(self, path: str, deep_search: bool = True) -> None:
        self.path: str = path
        self.flag: bool = deep_search
        self.__setup(self.flag)

    def __setup(self, flag: bool) -> None:
        """
        flag 값의 따라 os.walk 또는 os.listdir 을 실행합니다
        :param flag: true : os.walk, false : os.listdir
        :return: func
        """
        if flag:
            self.files = self.__d_search()
        else:
            self.files = self.__search()

    def __d_search(self) -> Generator:
        """
        폴더의 모든 내용을 검사합니다
        :return: 검사한 파일의 경로
        """
        for (root, _, files) in os.walk(self.path):
            for file in files:
                if file.find('.') != -1 and file.find('.') != 0:
                    yield os.path.join(root, file)

    def __search(self) -> Generator:
        """
        대상 폴더만을 검사합니다
        :return: 검사한 파일의 경로
        """
        for file in os.listdir(self.path):
            if file.find('.') != -1 and file.find('.') != 0:
                if os.path.isfile(os.path.join(self.path, file)):
                    yield os.path.join(self.path, file)

    def out_data(self) -> Tuple[List[List[Union[int, str]]], Set]:
        """
        파일의 경로를 받아 확장자 기준으로 정렬후 반환합니다
        :return: data : 인덱스, 경로 extension = 확장자
        """
        data = []
        temp = []
        extension = set()
        for file in self.files:
            temp.append(file)
            extension.add(file.split('.')[-1])
        temp.sort(key=lambda x: x.split('.')[-1])
        for index, temp_data in enumerate(temp):
            data.append([index, temp_data])

        return data, extension
