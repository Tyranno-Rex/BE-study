import pymongo

mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
db = mongo_client["bike_rental"]  # 데이터베이스 이름
collection = db["rental_stations"]  # 컬렉션 이름

projection = {"_id": 0, "name": 1, "x_pos": 1, "y_pos": 1, "parking_count": 1} # projection을 통해 필요한 데이터만 가져옴
cursor = collection.find({}, projection)

# 읽어온 데이터 출력
for document in cursor:
    print(document)