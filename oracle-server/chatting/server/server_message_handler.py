import server_function as sf
import json

def message_handler(client, clients, message, room_list, nicknames):
        print("msg: {}".format(message.decode('ascii')))
        
        # 파일 전송 처리
        if message.decode('ascii').find('file') != -1:
            sf.receive_file(client)

        # 클라이언트에게 파일 전송
        if message.decode('ascii').find('send') != -1:
            msg = message.decode('ascii').split('send ')[1]
            # msg -> eusneos: send  1111 2222
            recevier = msg.split(' ')[0]
            filename = msg.split(' ')[1]
            print("receiver: {}, filename: {}".format(recevier, filename))
            sf.send_file(recevier, clients, nicknames, filename)


        # 쿼리 진행
        if message.decode('ascii').find('query') != -1:
            # sql 뒤에 오는 문장은 sql 쿼리로 인식
            query = message.decode('ascii').split('query ')[1]
            result = json.dumps(sf.send_query(query))
            sf.broadcast_all(clients, result.encode('ascii'))
        
        # 방 생성
        if message.decode('ascii').find('room') != -1:
            # room 뒤에 오는 문장은 방 이름으로 인식
            room = message.decode('ascii').split('room ')[1]
            # 룸 리스트는 딕셔너리를 원소로 갖는 리스트
            if not any(r["room"] == room for r in room_list):
                room = {"room": room, "clients": []}
                if not any(client in room["clients"] for client in clients):
                    room["clients"].append(client)
                    room_list.append(room)
                    sf.broadcast_all(clients, "Room {} is created!\n".format(room).encode('ascii'))
                else:
                    sf.broadcast_all(clients, "You are already in room {}!\n".format(room).encode('ascii'))
            else:
                sf.broadcast_all(clients, "Room {} is already created!\n".format(room).encode('ascii'))
        
        # 방 참여
        if message.decode('ascii').find('join') != -1:
            room = message.decode('ascii').split('join ')[1]
            for r in room_list:
                if (r["room"] == room):
                    r["clients"].append(client)
                    sf.broadcast_in_room("Someone joined room {}!\n".format(room).encode('ascii'), r)
                    break
        
        # 방 나가기
        if message.decode('ascii').find('leave') != -1:
            room = message.decode('ascii').split('leave ')[1]
            for r in room_list:
                if (r["room"] == room):
                    r["clients"].remove(client)
                    sf.broadcast_in_room("Someone left room {}!\n".format(room).encode('ascii'), r)
                    break
        
        # 방 대화
        if message.decode('ascii').find('talk') != -1:
            nickname = nicknames[clients.index(client)]
            msg = message.decode('ascii').split('talk ')[1]
            msg = "{}: {}".format(nickname, msg)
            for r in room_list:
                if (client in r["clients"]):
                    sf.broadcast_in_room(msg.encode('ascii'), r)