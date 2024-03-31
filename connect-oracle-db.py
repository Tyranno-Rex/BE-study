# Oracle DB에 연결
import oracledb

# 변수 초기화
user = None
password = None
dsn = None
config_dir = None
wallet_location = None
wallet_password = None

# 파일을 읽기 모드('r')로 열기
with open("/home/oracle-db/private/password/oracle-db-connect-password", 'r') as file:
    # 파일의 각 줄에 대해 반복
    lines = file.readlines()
    # 각 변수에 값을 할당
    user = lines[0].strip()
    password = lines[1].strip()
    dsn = lines[2].strip()
    config_dir = lines[3].strip()
    wallet_location = lines[4].strip()
    wallet_password = lines[5].strip()
print(user, password, dsn, config_dir, wallet_location, wallet_password)


# Oracle DB에 연결
connection = oracledb.connect(
    user=user,
    password=password,
    dsn=dsn,
    config_dir=config_dir,
    wallet_location=wallet_location,
    wallet_password=wallet_password
)
             

def get_ungenerated_titles(table_name):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM {}".format(table_name))
        titles = cursor.fetchall()
    return titles

print(get_ungenerated_titles("ADMIN.\"Class\""))