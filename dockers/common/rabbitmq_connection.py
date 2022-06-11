from aio_pika import connect, Channel, Message, ExchangeType
import configparser
import logging

config = configparser.ConfigParser()
config.read('config.ini')


class RabbitMQHandler:
    channel: Channel

    def __init__(self, ENV):
        self.ENV = ENV
        self.RABBIT_IP = config['RabbitMQ']['ip_' + self.ENV] if 'ip_' + self.ENV in config['RabbitMQ'] else \
            config['RabbitMQ']['ip_default']
        pass

    def on_connection_closed(future):
        try:
            future.result()
        except:
            logging.exception("Oooops...")

    async def start_connection(self, queue_type, add_callback=False):
        connection_link = \
            str(config['RabbitMQ']['user']) + ":" + str(config['RabbitMQ']['password']) + \
            '@' + str(self.RABBIT_IP) + '/'
        connection = await connect("amqp://" + connection_link)
        self.channel = await connection.channel()
        if add_callback:
            connection.add_close_callback(self.on_connection_closed)
        await self.channel.set_qos(prefetch_count=1)
        logging.info(f"Connection to RabbitMQ {queue_type} established!")
        return await self.channel.declare_queue(config['RabbitMQ'][queue_type], durable=True, auto_delete=False)

    async def publish_message(self, exchange_type, message=None):
        exchange_name = config['RabbitMQ'][exchange_type + '_process']
        message = Message(message)
        exchange = await self.channel.declare_exchange(
            exchange_name,
            ExchangeType.FANOUT,
            durable=True
        )

        await exchange.publish(message, routing_key='extract_png')

    async def close_channel(self):
        logging.info(f'Closing RabbitMQ channel')
        await self.channel.close() 
