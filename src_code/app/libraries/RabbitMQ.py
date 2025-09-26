import pika
import ssl
from app.config.config import settings
import json
from contextlib import contextmanager

# Configurations
RABBIT_HOST = getattr(settings, 'LOG_RMQ_HOST', None)
RABBIT_PORT = getattr(settings, 'LOG_RMQ_PORT', None)
RABBIT_USER = getattr(settings, 'LOG_RMQ_USERNAME', None)
RABBIT_PWD = getattr(settings, 'LOG_RMQ_PASSWORD', None)
QUEUE_NAME = getattr(settings, 'LOG_RMQ_QUEUE_NAME', 'collabgov_elk_log_dev')
RABBIT_REGION = getattr(settings, 'LOG_RMQ_REGION', 'ap-south-1')
LOG_RMQ_SSL_CIPHERS = getattr(settings, 'LOG_RMQ_SSL_CIPHERS', 'ECDHE+AESGCM:!ECDSA')


class RabbitMQPublisher:
    def __init__(self, host=RABBIT_HOST, queue_name=QUEUE_NAME, port=RABBIT_PORT, user=RABBIT_USER, pwd=RABBIT_PWD, ssl_ciphers=LOG_RMQ_SSL_CIPHERS):
        self.host = host
        self.port = port
        self.rmq_username = user
        self.rmq_password = pwd
        self.queue_name = queue_name
        self.ssl_ciphers_txt = ssl_ciphers
        self.pika_conn = None
        self.connection = None
        self.channel = None

    @contextmanager
    def connect(self):
        """Context manager to handle RabbitMQ connection."""
        try:
            ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
            ssl_context.set_ciphers(self.ssl_ciphers_txt)
            url = f"amqps://{self.rmq_username}:{self.rmq_password}@{self.host}:{self.port}"
            parameters = pika.URLParameters(url)
            parameters.ssl_options = pika.SSLOptions(context=ssl_context)
            self.connection = pika.BlockingConnection(parameters)
            self.channel = self.connection.channel()
            # Ensure the queue matches the existing configuration
            self.channel.queue_declare(queue=self.queue_name, durable=True)  # Set durable=True
            yield self.channel
        except Exception as e:
            print(f"Error connecting to RabbitMQ: {e}")
        finally:
            if self.connection:
                self.connection.close()
                print("Connection closed.")

    def publish_message(self, channel, message):
        """Publish a message to the queue."""
        try:
            if not isinstance(message, str):
                message = json.dumps(message)  # Serialize if necessary
            channel.basic_publish(exchange='', routing_key=self.queue_name, body=message)
        except Exception as e:
            print(f"Error publishing message: {e}")


def push_to_rabbitmq(message):
    """Push message to RabbitMQ and handle exceptions gracefully."""
    publisher = RabbitMQPublisher()
    try:
        with publisher.connect() as channel:
            if channel:  # Ensure channel is valid
                publisher.publish_message(channel, message)
    except Exception as e:
        print(f"Ignored error while pushing message to RabbitMQ: {e}")
