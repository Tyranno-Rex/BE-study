from flask import Flask, Response
import cv2

app = Flask(__name__)
video_path = 'C:/Users/admin/project/oracle/oracle-server/h264/output.mp4'

def generate_frames():
    video = cv2.VideoCapture(video_path)
    while True:
        success, frame = video.read()
        if not success:
            break
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)