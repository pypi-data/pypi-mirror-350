import pika
from shared_architecture.config.config_loader import config_loader


RABBITMQ_HOST = config_loader.get("RABBITMQ_HOST", "localhost")
RABBITMQ_PORT = int(config_loader.get("RABBITMQ_PORT", 5672))
RABBITMQ_USER = config_loader.get("RABBITMQ_USER", "guest")
RABBITMQ_PASSWORD = config_loader.get("RABBITMQ_PASSWORD", "guest")
RABBITMQ_VHOST = config_loader.get("RABBITMQ_VHOST", "/")


class RabbitMQClient:
    def __init__(self):
        credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
        parameters = pika.ConnectionParameters(
            host=RABBITMQ_HOST,
            port=RABBITMQ_PORT,
            virtual_host=RABBITMQ_VHOST,
            credentials=credentials,
            heartbeat=600,
            blocked_connection_timeout=300
        )
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()

    def declare_queue(self, queue_name):
        self.channel.queue_declare(queue=queue_name, durable=True)

    def publish(self, queue_name, body):
        self.channel.basic_publish(
            exchange='',
            routing_key=queue_name,
            body=body
        )

    def close(self):
        if self.connection and self.connection.is_open:
            self.connection.close()

    def health_check(self):
        return self.connection.is_open
    
# Singleton pattern
_rabbitmq_client = RabbitMQClient()

def get_rabbitmq_client():
    return _rabbitmq_client
