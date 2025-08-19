import pika
import json
from .config import settings

def publish_notification(user_ids: list[int], title: str, message: str):
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=settings.RABBITMQ_HOST,
            port=settings.RABBITMQ_PORT,
            credentials=pika.PlainCredentials(settings.RABBITMQ_USER, settings.RABBITMQ_PASSWORD),
            connection_attempts=3,
            retry_delay=5
        ))
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
    except Exception as e:
        print(f"Failed to publish notification to RabbitMQ: {e}")
        print(f"Notification would have been sent to users {user_ids}: {title} - {message}")
        # In a production system, you might want to implement a retry mechanism
        # or fallback to another notification method
