import pymongo
import folium
import numpy as np
from sklearn.cluster import AgglomerativeClustering

# latitude(위도): y_pos, longitude(경도): x_pos
# folium의 입력 순서는 [경도, 위도] 순서이다.

def show_map_with_clusters(list_latitude, list_longitude, list_count, cluster_labels):
    m = folium.Map(location=[36.351112, 127.384806], zoom_start=12)
    unique_labels = np.unique(cluster_labels)
        
    colors = ['blue', 'green', 'red', 'purple', 'orange', 'darkred', 'lightred', 'beige', 'darkblue', 
            'darkgreen', 'cadetblue', 'darkpurple', 'white', 'pink', 'lightblue', 'lightgreen', 
            'gray', 'black', 'lightgray', 'lightyellow', 'yellow', 'lightorange', 'darkorange',
            'darkyellow', 'darkpink', 'darkbeige', 'darkcadetblue', 'darkgray', 'darklightblue', 'darklightgreen',
            'lightcoral', 'lightcyan', 'lightgoldenrodyellow', 'lightpink', 'lightsalmon', 'lightseagreen', 
            'lightskyblue', 'lightslategray', 'lightsteelblue', 'lightyellowgreen', 'lime', 'limegreen', 
            'linen', 'magenta', 'maroon', 'mediumaquamarine', 'mediumblue', 'mediumorchid', 'mediumpurple']
    
    for i, label in enumerate(unique_labels):
        cluster_indices = np.where(cluster_labels == label)[0]
        for index in cluster_indices:
            html = f'<div style="background-color: {colors[i]}; padding: 5px; border-radius: 5px; border: 1px solid black; font-size: 16pt;">{list_count[index]}</div>'
            div_icon = folium.DivIcon(html=html, icon_size=(30, 30), icon_anchor=(15, 15))
            folium.Marker([list_longitude[index], list_latitude[index]],
                          popup=f'Count: {list_count[index]}, Cluster: {label}',
                          icon=div_icon
                          ).add_to(m)

    m.save('./tasu/map/map_db/map_with_clusters.html')

mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
db = mongo_client["bike_rental"]  
collection = db["rental_stations"]  

projection = {"_id": 0, "x_pos": 1, "y_pos": 1, "parking_count": 1} 
cursor = collection.find({}, projection)

list_lat = []
list_lon = []
list_count = []

for document in cursor:
    count = document['parking_count']
    if count > 3:
        continue
    list_lat.append(document['y_pos'])
    list_lon.append(document['x_pos'])
    list_count.append(document['parking_count'])

# Convert latitude and longitude to numpy array
X = np.column_stack((list_lat, list_lon))
X = np.array(X, dtype=np.float64) # Convert to float64 => ValueError: dtype='numeric' is not compatible with arrays of bytes/strings.Convert your data to numeric values explicitly instead.

# ValueError: dtype='numeric' is not compatible with arrays of bytes/strings.Convert your data to numeric values explicitly instead.
clustering = AgglomerativeClustering(n_clusters=49).fit(X)
cluster_labels = clustering.labels_

show_map_with_clusters(list_lat, list_lon, list_count, cluster_labels)

