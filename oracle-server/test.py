import os

def getFileSize(file):
    return os.path.getsize(file)

def getFileData(file_t):
    with open(file_t, 'rb') as file:  # 인코딩 인자 제거
        data = b""  # 이진 데이터로 저장
        for line in file:
            data += line
    return data

file_size = getFileSize("/home/oracle/oracle-server/text.txt")
print(file_size)
print(getFileData("/home/oracle/oracle-server/text.txt"))
