import os
import requests
import server_function as sf

def broadcast_all(clients, message):
    for client in clients:
        client.send(message)

def broadcast_in_room(message, room):
    for client in room["clients"]:
        client.send(message)

def send_query(query):
    url = "http://158.180.80.199:5000/execute_query"
    data = {'query': query}
    response = requests.get(url, json=data)
    if (response.status_code == 200):
        return response.json()
    else:
        return {"error": "Failed to execute query"}

def receive_file(client):
    try:
        client.send('READY'.encode('ascii'))
        file_size = int(client.recv(1024).decode('ascii'))
        filename = "C:/Users/admin/project/oracle/oracle-server/chatting/server/database/file"
        client.send('OK'.encode('ascii'))
        received_size = 0
        with open(filename, 'wb') as file:
            while received_size < file_size:
                file_data = client.recv(1024)
                received_size += len(file_data)
                file.write(file_data)
        print("File received successfully.")
    except Exception as e:
        print("An error occurred while receiving the file:", e)

def send_file(receiver_nickname, clients, nicknames, filename):
    index = nicknames.index(receiver_nickname)
    receiver = clients[index]
    try:
        receiver.send('FILE RECEIVE READY'.encode('ascii'))
        filename = "C:/Users/admin/project/oracle/oracle-server/chatting/server/database/file"
        
        file_size = os.path.getsize(filename)
        receiver.send(str(file_size).encode('ascii'))
        response = receiver.recv(1024).decode('ascii')
        print("response: ", response)
        if (response == 'OK'):
            with open(filename, 'rb') as file:
                while True:
                    file_data = file.read(1024)
                    print(file_data)
                    if not file_data:
                        break
                    receiver.sendall(file_data)
            print("File sent successfully.")
        else:
            print("An error occurred while sending the file.")
    except FileNotFoundError:
        print("File not found.")
    except Exception as e:
        print("An error occurred while sending the file:", e)


def screen_share(client, clients, nicknames, room_list):
    try:
        # client.send('SS READY'.encode('ascii'))
        laddr = client.getsockname()
        ip = laddr[0]
        port = 9999
        print("ip: {} port: {}".format(ip, port))
    
        for room in room_list:
            if client in room["clients"]:
                for c in room["clients"]:
                    if c != client:
                        c.send('SS START'.encode('ascii'))
                        c.send(str(ip).encode('ascii'))
                break
    except Exception as e:
        print("An error occurred while sharing the screen:", e)