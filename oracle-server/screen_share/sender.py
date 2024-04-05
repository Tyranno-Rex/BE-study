from vidstream import StreamingServer
import threading

# receiver = StreamingServer('127.0.0.1', 9999)

receiver = StreamingServer('0.0.0.0', 9999)
t = threading.Thread(target=receiver.start_server)
t.start()

while input("") != 'STOP':
    continue

receiver.stop_server()
