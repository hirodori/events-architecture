from typing import Dict
import pika
import json

class Order:
    def __init__(self) -> None:
        self.__host = "localhost"
        self.__port = 5672
        self.__username = "guest"
        self.__password = "guest"
        self.__exchange = ""
        self.__routing_key = "data_queue"
        self.__channel = self.__create_channel()

    def __create_channel(self):
        connection_parameters = pika.ConnectionParameters(
            host=self.__host,
            port=self.__port,
            credentials=pika.PlainCredentials(
                username=self.__username,
                password=self.__password
            )
        )

        channel = pika.BlockingConnection(connection_parameters).channel()
        return channel

    def send_message(self, body: Dict):
        print('Sending message: '+ str(body))
        self.__channel.basic_publish(
            exchange=self.__exchange,
            routing_key=self.__routing_key,
            body=json.dumps(body),
            properties=pika.BasicProperties(
                delivery_mode=2
            )
        )

#order = {'id': 123, 'description':'HarryPotter', 'quantity':5}
#rabbitmq_publisher = Order()
#rabbitmq_publisher.send_message(order)
