import pika
from flask import Flask, request, render_template_string, flash
from order import Order
import json


class Stockist:
    def __init__(self, callback) -> None:
        self.__host = "localhost"
        self.__port = 5672
        self.__username = "guest"
        self.__password = "guest"
        self.__exchange = "stock_exchange"
        self.__admin_exchange = "admin_exchange"
        self.__queue1 = "estoque_insuficiente"
        self.__queue2 = "B"
        self.__callback = callback
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

        channel.exchange_declare(exchange=self.__exchange, exchange_type='direct')
        channel.exchange_declare(exchange=self.__admin_exchange, exchange_type='direct')

        queue = channel.queue_declare(queue='', exclusive=True)
        queue_name = queue.method.queue

        channel.queue_bind(exchange=self.__exchange, queue=queue_name, routing_key=self.__queue1)
        channel.queue_bind(exchange=self.__admin_exchange, queue=queue_name, routing_key=self.__queue2)

        channel.basic_consume(queue=queue_name, on_message_callback=self.__callback, auto_ack=True)

        return channel

    def start(self):
        print(f'Listening RabbitMQ on Port 5672')
        self.__channel.start_consuming()

def callback(ch, method, properties, body):
    if method.routing_key == "estoque_insuficiente":
        body_str = body.decode('utf-8')
        body_dict = json.loads(body_str)
        item_id = body_dict['id']
        quantity = body_dict['quantity']
        print(f"Não há estoque suficiente para {quantity} do item {item_id}! Necessidade de estoque!")
    elif method.routing_key == "B":
        body_str = body.decode('utf-8')
        print("Mensagem do ADMIN: " + body_str)



rabitmq_consumer = Stockist(callback)
rabitmq_consumer.start()
