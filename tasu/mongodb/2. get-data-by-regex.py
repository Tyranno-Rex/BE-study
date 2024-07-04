import pymongo

# MongoDB 연결 정보
mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
db = mongo_client["bike_rental"]  # 데이터베이스 이름
collection = db["rental_stations"]  # 컬렉션 이름

# query = {'name': {'$regex': '목련'}}
query = {'name': {'$regex': '시청'}}
cursor = collection.find(query)

for document in cursor:
    print(document)
