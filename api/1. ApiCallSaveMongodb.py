# URL : https://bikeapp.tashu.or.kr:50041/v1/openapi/station
# Header Key : api-token
# Key Value : 발급받은 인증키 입력
# 호출방식 : GET
# 데이터유형 : JSON

import json
import pymongo
import requests
import datetime
import os

# MongoDB 연결 정보
mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
db = mongo_client["bike_rental"]  # 데이터베이스 이름

date = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M")
collection = db["rental_stations_" + date]  # 컬렉션 이름

with open(r'C:\Users\\admin\project\\tasu\\private-data\\tasu_api_key.json', 'r') as f:
    api_keys = json.load(f)

tasu_api_key = api_keys["tasu_api_key"]
url = "https://bikeapp.tashu.or.kr:50041/v1/openapi/station"
headers = {
    "api-token": tasu_api_key
}
response = requests.get(url, headers=headers)
data = response.json()

# MongoDB에 데이터 저장
stations = data["results"]
collection.insert_many(stations)

print("데이터가 MongoDB에 성공적으로 저장되었습니다.")
