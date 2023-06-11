import grpc
import threading
import os

import chat_pb2
import chat_pb2_grpc

def send_message(stub, room_number, user):
    while True:
        message = input()
        try:
            if message.rstrip() == '/quit':
                print("Closing connection and quitting...")
                stub.Quit(chat_pb2.QuitRequest(room_number=room_number, user=user))  # Send a quit message to server
                os._exit(0)
            if message.rstrip() == '/list':
                user_list = stub.ListActiveUsers(chat_pb2.RoomNumber(room_number=int(room_number)))
                print("Active users: " + ", ".join(user_list.user))
                continue
            stub.SendMessage(chat_pb2.Message(room_number=room_number, user=user, text=message))
        except grpc.RpcError as e:
            print(f"\nError: {e.details()}\n")

def receive_messages(stub, room_number, user):
    for message in stub.ReceiveMessages(chat_pb2.JoinRequest(room_number=room_number, user=user)):
        print(f"{message.user}: {message.text}")

def run():
    while True:
        server_address = input("Enter the server address (leave blank for 'localhost:50051'): ").rstrip()
        if server_address == "":
            server_address = 'localhost:50051'

        try:
            channel = grpc.insecure_channel(server_address)
            stub = chat_pb2_grpc.ChatStub(channel)
            print(f"Connected to server at {server_address}")
            break
        except:
            print(f"Failed to connect to server at {server_address}. Please try again.")

    while True:
        room_number = input("Enter room number: ")
        if room_number.isdigit():
            room_status = stub.CheckRoom(chat_pb2.RoomNumber(room_number=int(room_number)))
            if room_status.is_filled:
                print("Room is filled. Please try again.")
                continue
            else:
                break
        else:
            print("Room number must be a number. Please try again.")

    while True:
        user = input("Enter your name: ")
        username_status = stub.CheckUsername(chat_pb2.Username(room_number=int(room_number), username=user))
        if username_status.is_taken:
            print("Username is already taken. Please try again.")
        else:
            break

    print()
    print(f"Welcome, {user}!")
    print("You can now start sending messages.")
    print("Enter '/quit' to disconnect from the chat room.")
    print("Enter '/list' to view the list of active users.")
    print()

    try:
        threading.Thread(target=send_message, args=(stub, int(room_number), user)).start()
        receive_messages(stub, int(room_number), user)
    except grpc.RpcError as e:
        print(f"\nError: {e.details()}\n")


if __name__ == '__main__':
    run()
