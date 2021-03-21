"""
created by demi
"""
import datetime
import os.path
import re
import sys
from sqlite3 import Binary
from typing import List, Union

from config import db_path
from include.db_access import DbSelect, DbWriter, DbOutPut, DbSetUp
from include.file_search import FileSearch


def data2db(datas: List[str]):  # 데이터를 DB에 삽입
    now = datetime.datetime.today().strftime("%Y-%m-%d %H:%M")
    for data in datas:
        file = data.split('\\')[-1]
        file_name, file_extension = file.split('.')
        with open(data, 'rb') as blob:
            blob_data = blob.read()
            DbWriter(db_path).insert(file_name, file_extension, Binary(blob_data), now)


def converter(data: List, out_path: str, flag: bool = False):
    if flag:
        for i in data:
            with open(os.path.join(out_path, i[0] + '.' + i[1]), 'wb') as file:
                file.write(i[2])
    else:
        for i in data:
            for j in i:
                with open(os.path.join(out_path, j[0] + '.' + j[1]), 'wb') as file:
                    file.write(j[2])


def db2data(out_path: str, trigger: Union[int, List[str]], sig: Union[List[str], str, int] = None):
    d_out = DbOutPut(db_path)

    if trigger == 1:
        data = d_out.out(sig)
        converter(data, out_path, True)

    if trigger == 2:
        data = d_out.extension_out(sig)
        converter(data, out_path)

    if trigger == 3:
        data = d_out.file_name_out(sig)
        converter(data, out_path)

    if trigger == 4:
        num1, num2 = map(int, sig[0].split('-'))
        data = d_out.index_out(num1, num2)
        converter(data, out_path)

    if trigger == 5:
        data = d_out.all_out()
        converter(data, out_path, True)


def choice_data(path: str, flag: bool) -> List[Union[int, str]]:
    data, extension = FileSearch(path, flag).out_data()
    temp = []

    for index, file in data:
        print(index, file)
        temp.append(file)

    print('extension : ', end='')

    for ext in extension:
        print(ext, end=' ')

    print()

    while True:
        answer_1 = input("인덱스 또는 확장자를 입력해주세요 : ")
        if re.search('-', answer_1):  # 인덱스 선택
            num1, num2 = map(int, answer_1.split('-'))
            if num1 >= num2:
                print("첫번째 인덱스는 두번째 인덱스보다 작아야합니다")
                pass
            else:
                temp = temp[num1:num2 + 1]
                return temp

        elif re.match('[a-z]+', answer_1):  # 확장자 선택
            if len(answer_1.split(', ')) == 1:
                temp = [i for i in temp if i.split('.')[-1] == answer_1]
                return temp
            else:
                data_temp = []
                keyword = answer_1.split(', ')
                for file in temp:
                    for key in keyword:
                        if file.split('.')[-1] == key:
                            data_temp.append(file)
                if len(data_temp) == 0:
                    print("올바른 확장자를 입력하세요")
                    break
                else:
                    return data_temp

        elif re.match('[0-9]+', answer_1):  # 인덱스 단일 선택
            out_data = []
            if len(answer_1) > 1:
                choose = answer_1.split(' ')
                for i in enumerate(temp):
                    for j in choose:
                        if i[0] == int(j):
                            out_data.append(i[1])

            else:
                for i in enumerate(temp):
                    if i[0] == int(answer_1):
                        out_data.append(i[1])

            return out_data

        elif answer_1 == "":  # 전체 선택
            return temp




def etc():
    pass


def main(search_range: bool = True):
    path = input('경로를 입력해주세요 : ')
    if search_range:
        data = choice_data(path, flag=True)
    else:
        data = choice_data(path, flag=False)
    data2db(data)


if __name__ == '__main__':
    argv = sys.argv
    if len(argv) >= 2:

        if argv[1] == "--s":
            main(search_range=True)
        elif argv[1] == "--sd":
            main(search_range=False)

        elif argv[1] == "--help":
            etc()

        elif argv[1] == "--v":
            if len(argv) >= 4:
                if argv[2] == "--ext":
                    DbSelect(db_path).select(argv[3], extension=True)
                elif argv[2] == "--name":
                    DbSelect(db_path).select(argv[3], file_name=True)
                else:
                    print("ERROR !!")
            else:
                DbSelect(db_path).select()

        elif argv[1] == "--o":  # out
            db2data(argv[2], sig=argv[3:], trigger=1)
        elif argv[1] == "--oe":  # extension out
            db2data(argv[2], sig=argv[3:], trigger=2)
        elif argv[1] == "--of":  # filename out
            db2data(argv[2], sig=argv[3:], trigger=3)
        elif argv[1] == "--oi":  # index out
            db2data(argv[2], sig=argv[3:], trigger=4)
        elif argv[1] == "--oa":
            db2data(argv[2], trigger=5)

        elif argv[1] == "--clean":
            while True:
                answer = input("Are You Sure? y/n[n] : ")
                if answer.upper() == "Y":
                    DbSetUp(db_path).clear()
                    break
                else:
                    break
    else:
        main()
