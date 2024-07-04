from flask import Response, request
import cv2, os
from server_main import *

def generate_frames(video_path):
    video = cv2.VideoCapture(video_path)
    while True:
        success, frame = video.read()
        if not success:
            break
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# 동영상 이름도 받아 올거임
@app.route('/video_feed')
def video_feed():
    video_name = request.args.get('video_name')
    video_path = 'C:/Users/admin/project/oracle/oracle-server/h264/database/' + video_name
    return Response(generate_frames(video_path), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/get_frame_count')
def get_frame_count():
    video_name = request.args.get('video_name')
    video_path = 'C:/Users/admin/project/oracle/oracle-server/h264/database/' + video_name
    video = cv2.VideoCapture(video_path)
    frame_count = video.get(cv2.CAP_PROP_FPS)
    return {'frame_count': frame_count}

@app.route('/get_video_list')
def get_video_list():
    video_list = os.listdir('C:/Users/admin/project/oracle/oracle-server/h264/database')
    return {'video_list': video_list}
