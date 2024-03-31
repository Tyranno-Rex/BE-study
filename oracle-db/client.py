import requests

def execute_query(query):
    url = 'http://127.0.0.1:5000/execute_query'
    data = {'query': query}
    response = requests.get(url, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        return {'error': 'Failed to execute query'}

if __name__ == '__main__':
    query = 'SELECT * FROM ADMIN."Class"'  # 이 부분 수정
    result = execute_query(query)
    print(result)
