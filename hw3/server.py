import pika
import sys
import time
import json

users_in_rooms = {}

def callback(ch, method, properties, body):
    print(f"Received from Room {method.routing_key} > {body.decode()}")
    data = json.loads(body)

    if data['type'] == 'connect':
        room_id = method.routing_key
        if room_id in users_in_rooms and data['user'] in users_in_rooms[room_id]:

            ch.basic_publish(
                exchange='',
                routing_key=properties.reply_to,
                properties=pika.BasicProperties(
                    correlation_id=properties.correlation_id,  # Echo the correlation_id received from the client
                ),
                body=json.dumps({
                    "type": "connect_response",
                    "user": data['user'],
                    "msg": "Username taken, please try again."
                })
            )


        else:
            if room_id not in users_in_rooms:
                users_in_rooms[room_id] = set()
            users_in_rooms[room_id].add(data["user"])


            ch.basic_publish(
                exchange='',
                routing_key=properties.reply_to,
                properties=pika.BasicProperties(
                    correlation_id=properties.correlation_id,  # Echo the correlation_id received from the client
                ),
                body=json.dumps({
                    "type": "connect_response",
                    "user": data['user'],
                    "msg": "OK"
                })
            )
    elif data['type'] == 'disconnect':
        room_id = method.routing_key
        if room_id in users_in_rooms and data['user'] in users_in_rooms[room_id]:
            users_in_rooms[room_id].remove(data['user'])

    sys.stdout.flush()


def main():
    max_retries = 200

    for retry in range(max_retries):
        print(f"Trying to connect to RabbitMQ. Retry # {retry}")
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
            break
        except pika.exceptions.AMQPConnectionError:
            print("Failed to connect to RabbitMQ. Retrying...")
            time.sleep(1)
    else:
        print(f"Failed to connect to RabbitMQ after {max_retries} retries. Quitting...")
        exit(0)
    print("Sucessfully connected to RabbitMQ")

    channel = connection.channel()

    channel.exchange_declare(exchange='chat_rooms', exchange_type='topic', durable=True)

    result = channel.queue_declare('', exclusive=True)
    queue_name = result.method.queue

    channel.queue_bind(exchange='chat_rooms', queue=queue_name, routing_key='#')

    channel.basic_consume(
        queue=queue_name, on_message_callback=callback, auto_ack=True)

    print("Chat server started. Waiting for messages...")
    channel.start_consuming()

if __name__ == '__main__':
    main()
