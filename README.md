# DB_ARCHIVE

## sqlite를 이용해 바이너리 파일을 저장 및 복원 합니다.

---
## Main Syntax

> ## python main.py -? -?
---

> ## START : python main.py --s or --sd
>> ### --s : 해당 폴더안의 있는 모든 폴더를 순회하여 파일을 검사합니다
>> ### --sd : 해당 폴더안의 있는 파일만 검사합니다
---
> ## 인덱스 또는 확장자를 입력해주세요 :
>> ### 다음과 같은 키워드를 제공합니다
>>> ### Number1-Number2 : 해당인덱스에 시작 숫자부터 끝 숫자까지 저장합니다
>>> ### Number1, Number2, Number3 : 단일 숫자를 여러번 지정할 수 있습니다
>>> ### extension1, extension2 .. : 단일 또는 여러 확장자를 지정할 수 있습니다
---
> ## OUT : python main.py Syntax path option
>> ## Syntax
>> ### --o : option Number1 Number2 ... 
>> ### --oe :  option extension1 extension2 ...
>> ### --oi :option Number1-Number2
>> ### --of :option Filename
>> ### --oa 

>> ## Example
>> ### python main.py --o 1 2 3
>> ### python main.py --oe PDF PNG 
>> ### python main.py --oi 1-10
>> ### python main.py --of try
>> ### python main.py --oa
---

> # view : python main.py --v
>> ## Filter
>> ## --ext extension
>> ## --name File_name

>> ## Example
>> ### python main.py --v --ext pdf
>> ### python main.py --v --name try
---
> ## Db_Clean : python main.py --clean