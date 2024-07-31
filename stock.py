import pika
import sqlite3
import json


class Stock:
    def __init__(self, callback) -> None:
        self.__host = "localhost"
        self.__port = 5672
        self.__username = "guest"
        self.__password = "guest"
        self.__queue = "data_queue"
        self.__exchange = "stock_exchange"
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

        channel.queue_declare(
            queue=self.__queue,
            durable=True
        )
        channel.basic_consume(
            queue=self.__queue,
            auto_ack=True,
            on_message_callback=self.__callback
        )

        return channel

    def start(self):
        print(f'Listening RabbitMQ on Port 5672')
        self.__channel.start_consuming()


def get_quantity_by_id(item_id, quantity):
    """Search for an item by ID and return its quantity."""
    # Connect to the SQLite database
    conn = sqlite3.connect('stock_data.db')
    cursor = conn.cursor()

    # SQL query to find the item by ID
    query = "SELECT quantity FROM STOCK_DATA WHERE id = ?"
    cursor.execute(query, (item_id,))

    # Fetch one result
    result = cursor.fetchone()
    if result:
        new_quantity = result[0] - quantity
        if new_quantity >= 0:
            # Update the quantity in the database
            update_query = "UPDATE STOCK_DATA SET quantity = ? WHERE id = ?"
            cursor.execute(update_query, (new_quantity, item_id))
            conn.commit()  # Commit the transaction
            conn.close()
            return True  # Indicate success
        else:
            conn.close()
            return False  # Indicate failure due to insufficient quantity


def minha_callback(ch, method, properties, body):
    print(body)

    body_str = body.decode('utf-8')  # Decode the byte string into a string
    body_dict = json.loads(body_str)  # Parse the string as JSON to get a dictionary
    item_id = body_dict['id']
    quantity = body_dict['quantity']
    estoque_ok = get_quantity_by_id(item_id, quantity)
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    evento_resposta = 'estoque_confirmado' if estoque_ok else 'estoque_insuficiente'
    print('Pedido recebido!')
    print('Dados do pedido:' + str(body))
    print('Enviando dados para a fila: ' + evento_resposta)
    channel.basic_publish(exchange="stock_exchange", routing_key=evento_resposta, body=body)


rabitmq_consumer = Stock(minha_callback)
rabitmq_consumer.start()
