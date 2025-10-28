import json
import os
import pika
import time

def main():
    host = os.getenv("RABBITMQ_HOST", "rabbitmq")
    queue = os.getenv("QUEUE_NAME", "mensagens")

    for attempt in range(1, 21):
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
            break
        except Exception as e:
            print(f"Aguardando RabbitMQ (tentativa {attempt}/20): {e}")
            time.sleep(2)
    else:
        raise RuntimeError("Não foi possível conectar ao RabbitMQ.")

    channel = connection.channel()
    channel.queue_declare(queue=queue, durable=True)

    def callback(ch, method, properties, body):
        data = json.loads(body)
        print(f"Consumer recebeu: {data}")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=queue, on_message_callback=callback)

    print(f"Consumer ouvindo a fila '{queue}'. CTRL+C para sair.")
    try:
        channel.start_consuming()
    finally:
        if connection and connection.is_open:
            connection.close()

if __name__ == "__main__":
    main()