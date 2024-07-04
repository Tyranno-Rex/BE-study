import pymongo
import folium
import numpy as np
from sklearn.cluster import AgglomerativeClustering

# latitude(위도): y_pos, longitude(경도): x_pos
# folium의 입력 순서는 [경도, 위도] 순서이다.

def show_map_with_clusters(list_latitude, list_longitude, list_count, cluster_labels_over_3, list_latitude_under_3, list_longitude_under_3, list_count_under_3, cluster_labels_under_3):
    m = folium.Map(location=[36.351112, 127.384806], zoom_start=12)
    unique_labels_over_3 = np.unique(cluster_labels_over_3)
    unique_labels_under_3 = np.unique(cluster_labels_under_3)

    for i, label in enumerate(unique_labels_over_3):
        colors_blue = [
            '#0000FF', '#0000CD', '#00008B', '#000080', '#191970', '#1E90FF', '#4169E1', '#6495ED', '#4682B4', '#87CEEB',
            '#87CEFA', '#00BFFF', '#1E90FF', '#ADD8E6', '#B0E0E6', '#5F9EA0', '#B0C4DE', '#AFEEEE', '#87CEEB', '#87CEFA',
            '#00BFFF', '#1E90FF', '#ADD8E6', '#B0E0E6', '#5F9EA0', '#B0C4DE', '#AFEEEE', '#87CEEB', '#87CEFA', '#00BFFF',
            '#1E90FF', '#ADD8E6', '#B0E0E6', '#5F9EA0', '#B0C4DE', '#AFEEEE', '#87CEEB', '#87CEFA', '#00BFFF', '#1E90FF',
            '#ADD8E6', '#B0E0E6', '#5F9EA0', '#B0C4DE', '#AFEEEE', '#87CEEB', '#87CEFA', '#00BFFF', '#1E90FF', '#ADD8E6'
        ]

        cluster_indices = np.where(cluster_labels_over_3 == label)[0]
        for index in cluster_indices:
            html = f'<div style="background-color: {colors_blue[i]}; padding: 5px; border-radius: 5px; border: 1px solid black; font-size: 16pt;">{list_count[index]}</div>'
            div_icon = folium.DivIcon(html=html, icon_size=(30, 30), icon_anchor=(15, 15))
            folium.Marker([list_longitude[index], list_latitude[index]],
                          popup=f'Count: {list_count[index]}, Cluster: {label}',
                          icon=div_icon
                          ).add_to(m)

    for i, label in enumerate(unique_labels_under_3):
        colors_red = [
            '#FF0000', '#CD0000', '#8B0000', '#800000', '#8B4513', '#A52A2A', '#B22222', '#DC143C', '#CD5C5C', '#F08080',
            '#E9967A', '#FA8072', '#FFA07A', '#FF7F50', '#FF6347', '#FF4500', '#FF0000', '#CD0000', '#8B0000', '#800000',
            '#8B4513', '#A52A2A', '#B22222', '#DC143C', '#CD5C5C', '#F08080', '#E9967A', '#FA8072', '#FFA07A', '#FF7F50',
            '#FF6347', '#FF4500', '#FF0000', '#CD0000', '#8B0000', '#800000', '#8B4513', '#A52A2A', '#B22222', '#DC143C',
            '#CD5C5C', '#F08080', '#E9967A', '#FA8072', '#FFA07A', '#FF7F50', '#FF6347', '#FF4500'
        ]

        cluster_indices = np.where(cluster_labels_under_3 == label)[0]
        for index in cluster_indices:
            html = f'<div style="background-color: {colors_red[i]}; padding: 5px; border-radius: 5px; border: 1px solid black; font-size: 16pt;">{list_count_under_3[index]}</div>'
            div_icon = folium.DivIcon(html=html, icon_size=(30, 30), icon_anchor=(15, 15))
            folium.Marker([list_longitude_under_3[index], list_latitude_under_3[index]],
                          popup=f'Count: {list_count_under_3[index]}, Cluster: {label}',
                          icon=div_icon
                          ).add_to(m)



    m.save('./tasu/map/map_db/map_with_clusters.html')

mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
db = mongo_client["bike_rental"]  
collection = db["rental_stations"]  

projection = {"_id": 0, "x_pos": 1, "y_pos": 1, "parking_count": 1} 
cursor = collection.find({}, projection)

over_3_list_lat = []
over_3_list_lon = []
over_3_list_count = []

under_3_list_lat = []
under_3_list_lon = []
under_3_list_count = []


for document in cursor:
    count = document['parking_count']
    if count >= 1:
        over_3_list_lat.append(document['y_pos'])
        over_3_list_lon.append(document['x_pos'])
        over_3_list_count.append(document['parking_count'])
    else:
        under_3_list_lat.append(document['y_pos'])
        under_3_list_lon.append(document['x_pos'])
        under_3_list_count.append(document['parking_count'])

X_over_3 = np.column_stack((over_3_list_lat, over_3_list_lon))
X_over_3 = np.array(X_over_3, dtype=np.float64) 
clustering_over_3 = AgglomerativeClustering(n_clusters=49).fit(X_over_3)
cluster_labels_over_3 = clustering_over_3.labels_

X_under_3 = np.column_stack((under_3_list_lat, under_3_list_lon))
X_under_3 = np.array(X_under_3, dtype=np.float64)
clustering_under_3 = AgglomerativeClustering(n_clusters=45).fit(X_under_3)
cluster_labels_under_3 = clustering_under_3.labels_

whole_cluster_labels = np.concatenate((cluster_labels_over_3, cluster_labels_under_3), axis=0)

show_map_with_clusters(over_3_list_lat, over_3_list_lon, over_3_list_count, cluster_labels_over_3, \
                        under_3_list_lat, under_3_list_lon, under_3_list_count, cluster_labels_under_3)

