


from flask import Flask

# Flask 애플리케이션을 생성합니다.
app = Flask(__name__)

# 루트 경로("/")에 대한 핸들러를 정의합니다.

class Server:
    def __init__(self):
        # 서버를 실행합니다.
        app.run(host="0.0.0.0", port=5000)


# 서버를 실행합니다.
if __name__ == "__main__":
    server = Server()
