import grpc
from concurrent import futures
import time
import queue
from collections import defaultdict
import random

import chat_pb2
import chat_pb2_grpc

class User:
    def __init__(self, name, queue):
        self.name = name
        self.queue = queue
        self.role = None

class Room:
    def __init__(self):
        self.users = []
        self.game_started = False
        self.enter_messages = []


class ChatServicer(chat_pb2_grpc.ChatServicer):
    def __init__(self):
        self.rooms = defaultdict(Room)
        self.roles = ["policeman", "villager", "villager"]

    def CheckRoom(self, request, context):
        room = self.rooms[request.room_number]
        if len(room.users) >= 3 or room.game_started:
            return chat_pb2.RoomStatus(is_filled=True)
        else:
            return chat_pb2.RoomStatus(is_filled=False)

    def CheckUsername(self, request, context):
        room = self.rooms[request.room_number]
        if any(user.name == request.username for user in room.users):
            return chat_pb2.UsernameStatus(is_taken=True)
        else:
            return chat_pb2.UsernameStatus(is_taken=False)

    def SendMessage(self, request, context):
        room = self.rooms[request.room_number]
        for user in room.users:
            if user.name != request.user:
                user.queue.put(request)
            room.enter_messages.append(request)
        return chat_pb2.Empty()

    def ListActiveUsers(self, request, context):
        return chat_pb2.UserList(user=[user.name for user in self.rooms[request.room_number].users])
    def ReceiveMessages(self, request, context):
        room = self.rooms[request.room_number]
        if room.game_started:
            return
        if len(room.users) >= 3:
            return
        if any(user.name == request.user for user in room.users):
            return
        q = queue.Queue()
        user = User(request.user, q)
        room.users.append(user)
        for message in room.enter_messages:
            q.put(message)
        enter_message = chat_pb2.Message(user="Server", text=f"{request.user} joined the game")
        room.enter_messages.append(enter_message)
        for u in room.users:
            u.queue.put(enter_message)
        if len(room.users) == 3:
            self.start_game(room)
        try:
            while True:
                yield q.get()
        except grpc.RpcError:
            exit_message = chat_pb2.Message(user="Server", text=f"{request.user} left the game")
            room.enter_messages.append(exit_message)
            for u in room.users:
                if u.name != request.user:
                    u.queue.put(exit_message)
        finally:
            room.users[:] = [user for user in room.users if user.name != request.user]

    def Quit(self, request, context):
        room_number = request.room_number
        user = request.user
        room = self.rooms[room_number]

        room.users[:] = [user for user in room.users if user.name != request.user]

        exit_message = chat_pb2.Message(user="Server", text=f"{request.user} left the game")
        room.enter_messages.append(exit_message)
        for u in room.users:
            if u.name != request.user:
                u.queue.put(exit_message)

        return chat_pb2.Empty()

    def start_game(self, room):
        room.game_started = True
        for user in room.users:
            user.queue.put(chat_pb2.Message(user="Server", text=f"Game has started!"))
        roles = self.roles[:]
        random.shuffle(roles)
        for user in room.users:
            user.role = roles.pop()
            user.queue.put(chat_pb2.Message(user="Server", text=f"You are a {user.role}."))

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    chat_pb2_grpc.add_ChatServicer_to_server(ChatServicer(), server)
    print('Starting server. Listening on port 50051.')
    server.add_insecure_port('[::]:50051')
    server.start()

    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()
