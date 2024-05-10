import pymongo
import folium

# latitude(위도): y_pos, longitude(경도): x_pos
# folium의 입력 순서는 [경도, 위도] 순서이다.

def show_map_with_number(list_latitude, list_longitude, list_count):
    m = folium.Map(location=[36.351112, 127.384806], zoom_start=12)  

    for i in range(len(list_latitude)):
        html = f'<div style="background-color: white; padding: 5px; border-radius: 5px; border: 1px solid black; font-size: 16pt;">{list_count[i]}</div>'
        div_icon = folium.DivIcon(html=html, icon_size=(30,30), icon_anchor=(15,15))
        folium.Marker([list_longitude[i], list_latitude[i]], 
                        popup=f'Number: {list_count[i]}',  
                        icon=div_icon
                        ).add_to(m)
        
    m.save('./tasu/map/map_db/map_with_number(over 3 count).html')

mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
db = mongo_client["bike_rental"]  
collection = db["rental_stations"]  

projection = {"_id": 0, "name": 1, "x_pos": 1, "y_pos": 1, "parking_count": 1} 
cursor = collection.find({}, projection)

list_name = []
list_lat = []
list_lon = []
list_count = []

for document in cursor:
    count = document['parking_count']
    if count < 3:
        continue
    list_name.append(document['name'])
    list_lat.append(document['y_pos'])
    list_lon.append(document['x_pos'])
    list_count.append(document['parking_count'])

show_map_with_number(list_lat, list_lon, list_count)
