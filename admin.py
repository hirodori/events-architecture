from typing import Dict
import pika
import json

class Admin:
    def __init__(self) -> None:
        self.__host = "localhost"
        self.__port = 5672
        self.__username = "guest"
        self.__password = "guest"
        self.__exchange = "admin_exchange"
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

    def send_message(self, routing_key,body: Dict):
        print('\nEnviando mensagem: '+ str(body))
        self.__channel.basic_publish(
            exchange=self.__exchange,
            routing_key=routing_key,
            body=json.dumps(body),
            properties=pika.BasicProperties(
                delivery_mode=2
            )
        )

routing_key = input("(A) Notification | (B) Stockist\nPara quem é essa mensagem? ")
message = input("Insira a mensagem que deseja enviar: ")
rabbitmq_publisher = Admin()
rabbitmq_publisher.send_message(routing_key, message)
