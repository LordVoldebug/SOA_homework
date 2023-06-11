import sys
import os

import pika
import threading
import json
import uuid

def read_from_room(room_id, username):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()

    result = channel.queue_declare('', exclusive=True)
    queue_name = result.method.queue

    channel.queue_bind(exchange='chat_rooms', queue=queue_name, routing_key=room_id)

    def callback(ch, method, properties, body):
        msg = json.loads(body)
        sender = msg['user']
        if sender != username and msg['type'] == 'messsage':
            print(f"{msg['user']}: {msg['msg']}")

    channel.basic_consume(
        queue=queue_name, on_message_callback=callback, auto_ack=True)

    channel.start_consuming()

def write_to_room(room_id, username):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()



    while True:
        msg = input()

        if msg == '/disconnect':
            channel.basic_publish(
                exchange='chat_rooms',
                routing_key=room_id,
                body=json.dumps({'type': 'disconnect',
                                 'user': username,
                                 'msg': ""}),
            )
            os._exit(0)

        messsage = {}
        messsage['type'] = 'messsage'
        messsage['user'] = username
        messsage['msg'] = msg


        channel.basic_publish(
            exchange='chat_rooms',
            routing_key=room_id,
            body=json.dumps(messsage),
        )



def connect_to_room(room_id, username):
    connect_message = json.dumps({
        "type": "connect",
        "user": username,
        "msg": ""
    })

    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()

    result = channel.queue_declare('', exclusive=True)
    callback_queue = str(result.method.queue)

    response = None
    corr_id = str(uuid.uuid4())

    def on_response(ch, method, properties, body):
        sys.stdout.flush()

        nonlocal response
        if corr_id == properties.correlation_id:
            response = body

    channel.basic_consume(
        queue=callback_queue, on_message_callback=on_response, auto_ack=True)

    channel.basic_publish(
        exchange='chat_rooms',
        routing_key=room_id,
        properties=pika.BasicProperties(
            reply_to=callback_queue,
            correlation_id=str(corr_id),
        ),
        body=connect_message,
    )


    while response is None:
        connection.process_data_events()


    return json.loads(response)['msg']


if __name__ == '__main__':
    room_id = input("Enter room ID: ")
    while True:
        username = input("Enter your name: ")
        res = connect_to_room(room_id, username)
        if res == "OK":
            print("Username set sucessfully")
            break
        else:
            print(res)


    read_thread = threading.Thread(target=read_from_room, args=(room_id, username))
    write_thread = threading.Thread(target=write_to_room, args=(room_id, username))

    read_thread.start()
    write_thread.start()
