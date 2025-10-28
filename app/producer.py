import json
import os
import pika


def _connect():
    host = os.getenv("RABBITMQ_HOST", "rabbitmq")
    params = pika.ConnectionParameters(host=host)
    return pika.BlockingConnection(params)


def send_message(message: dict, queue_name: str = "mensagens"):
    connection = None

    try:
        connection = _connect()
        channel = connection.channel()

        channel.queue_declare(queue=queue_name, durable=True)

        channel.basic_publish(
            exchange="",
            routing_key=queue_name,
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=2  
            ),
        )
        print(f"Producer: enviado para '{queue_name}': {message}")
        
    finally:
        if connection and connection.is_open:
            connection.close()