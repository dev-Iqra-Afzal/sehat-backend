import pika
import json

def publish_notification(user_ids: list[int], title: str, message: str):
    connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq"))
    channel = connection.channel()
    channel.queue_declare(queue="notifications", durable=True)

    payload = {
        "user_ids": user_ids,
        "title": title,
        "message": message
    }
    channel.basic_publish(
        exchange='',
        routing_key='notifications',
        body=json.dumps(payload),
        properties=pika.BasicProperties(
            delivery_mode=2,  # make message persistent
        )
    )

    print("sent: ", payload)
    connection.close()
