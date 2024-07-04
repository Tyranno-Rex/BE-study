import requests
import cv2
import numpy as np


# 영상을 받아오는 함수
def get_stream_frame(url, video_name):
    # URL에서 프레임 받아오기
    print(f"Getting video stream from {url} with video name {video_name}")
    response = requests.get(url, params={'video_name': video_name}, stream=True)
    if response.status_code == 200:
        global bytes
        bytes = bytes()
        for chunk in response.iter_content(chunk_size=1024):
            bytes += chunk
            a = bytes.find(b'\xff\xd8') # JPEG 시작 바이트
            b = bytes.find(b'\xff\xd9') # JPEG 끝 바이트
            if a != -1 and b != -1:
                jpg = bytes[a:b+2] # JPEG 이미지
                bytes = bytes[b+2:] # 다음 프레임을 위해 이미지 끝 바이트 이후부터 저장
                frame = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                yield frame

def get_frame_count(video_name):
    url = "http://192.168.3.3:5001/get_frame_count"
    response = requests.get(url, params={'video_name': video_name})
    frame_count = response.json()['frame_count']
    return frame_count

# 프레임을 받아와서 화면에 출력하는 함수
def show_stream(video_name):
    url_get_video = "http://192.168.3.3:5001/video_feed"
    v_frame = int(get_frame_count(video_name))
    for frame in get_stream_frame(url_get_video, video_name):
        cv2.imshow('Video Stream', frame)
        if cv2.waitKey(v_frame) & 0xFF == ord('q'):
            break

def run_video_stream(video_name):
    # 영상 재생
    show_stream(video_name)
    # OpenCV 창 닫기
    cv2.destroyAllWindows()


while True:
    command = input("Enter command:\n1.list\n2.play\n3.quit\n")

    if command == '1':
        url = "http://192.168.3.3:5001/get_video_list"
        response = requests.get(url)
        video_list = response.json()['video_list']
        
        index = 1
        print("\n====Video List====")
        for v in video_list:
            print(f'{index}. {v}')
            index += 1
        print("==================\n")
    
    elif command == '2':
        url = "http://192.168.3.3:5001/get_video_list"
        response = requests.get(url)
        video_list = response.json()['video_list']
        print(video_list)
        video_name = input("Enter video name: ")
        run_video_stream(video_name)