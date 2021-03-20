import sys
import re
from typing import List, Union, Set, Tuple
import datetime
from include.db_access import DbSelect, DbWriter
from include.file_search import FileSearch
from config import db_path


def data2db(datas: List[str]):  # 데이터를 DB에 삽입
    now = datetime.datetime.today().strftime("%Y-%m-%d %H:%M")
    for data in datas:
        file = data.split('\\')[-1]
        file_name, file_extension = file.split('.')
        with open(data, 'rb') as blob:
            blob_data = blob.readline()
            DbWriter(db_path).insert(file_name, file_extension, blob_data, now)



def db2data():
    pass


def choice_data(path: str, flag: bool = True) -> Union[List[str], str]:
    data, extension = FileSearch(path, flag).out_data()
    temp = []

    for index, file in data:
        print(index, file)
        temp.append(file)
    print(extension)

    while True:
        answer = input("인덱스 또는 확장자를 입력해주세요 : ")
        if re.search('-', answer):  # 인덱스 선택
            num1, num2 = map(int, answer.split('-'))
            if num1 >= num2:
                print("첫번째 인덱스는 두번째 인덱스보다 작아야합니다")
                pass
            else:
                temp = temp[num1:num2 + 1]
                return temp

        elif re.match('[a-z]+', answer):  # 확장자 선택
            if len(answer.split(', ')) == 1:
                temp = [i for i in temp if i.split('.')[-1] == answer]
                return temp
            else:
                data_temp = []
                keyword = answer.split(', ')
                for file in temp:
                    for key in keyword:
                        if file.split('.')[-1] == key:
                            data_temp.append(file)
                if len(data_temp) == 0:
                    print("올바른 확장자를 입력하세요")
                    pass
                else:
                    return data_temp

        elif re.match('[0-9]+', answer):  # 인덱스 단일 선택
            return temp[int(answer)]

        elif answer == "":  # 전체 선택
            return temp

        else:
            print("지원하지 않는 형태입니다")


def select_db():
    pass


def etc():
    pass


def main():
    path = input('경로를 입력해주세요 : ')
    data = choice_data(path)  # TODO : 명령줄 인자 받으면 input 안하기
    data2db(data)


if __name__ == '__main__':
    main()
