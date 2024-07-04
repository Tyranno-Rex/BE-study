import requests

# url = "http://192.168.3.3:5001/get_video_list"
url = "http://127.0.0.1:5001/get_video_list"
response = requests.get(url)
video_list = response.json()['video_list']
print(video_list)