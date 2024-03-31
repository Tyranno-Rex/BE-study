from flask import Flask, request, jsonify
import oracledb

app = Flask(__name__)

class OracleDBConnecter:
    def __init__(self):
        # 변수 초기화
        self.user = None
        self.password = None
        self.dsn = None
        self.config_dir = None
        self.wallet_location = None
        self.wallet_password = None
        self.connection = None

        # 파일을 읽기 모드('r')로 열기
        with open("/home/oracle/private/database/password", 'r') as file:
            # 파일의 각 줄에 대해 반복
            lines = file.readlines()
            # 각 변수에 값을 할당
            self.user = lines[0].strip()
            self.password = lines[1].strip()
            self.dsn = lines[2].strip()
            self.config_dir = lines[3].strip()
            self.wallet_location = lines[4].strip()
            self.wallet_password = lines[5].strip()

        # db 연결
        self.connection = oracledb.connect(
            user=self.user,
            password=self.password,
            dsn=self.dsn,
            config_dir=self.config_dir,
            wallet_location=self.wallet_location,
            wallet_password=self.wallet_password
        )

    def get_connection(self):
        return self.connection
    
    def execute_query(self, query):
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
        return result

db_connector = OracleDBConnecter()

@app.route('/execute_query', methods=['GET'])
def execute_query():
    data = request.get_json()
    query = data['query']
    result = db_connector.execute_query(query)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
