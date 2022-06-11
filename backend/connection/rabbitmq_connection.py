from aio_pika import connect, Message, DeliveryMode, ExchangeType
from settings import config
import logging


# log = logging.getLogger(__name__)
#
async def init_channel(env):
    connection_link = \
        str(config['RabbitMQ']['user']) + ":" + str(config['RabbitMQ']['password']) + \
        '@' + str(config['RabbitMQ'].get('ip_' + env, config['RabbitMQ']['ip_default']) + '/')

    connection = await connect("amqp://" + connection_link)
    channel = await connection.channel()
    return channel


async def init(env, queue_name):
    channel = await init_channel(env)
    logging.info('Established connection to rabbitMQ.')
    await channel.set_qos(prefetch_count=1)
    return await channel.declare_queue(queue_name, durable=True, auto_delete=False)


async def publish_message(exchange_name, message=None, env=None):
    channel = await init_channel(env)
    message = Message(message)
    exchange = await channel.declare_exchange(
        exchange_name,
        ExchangeType.FANOUT,
        durable=True
    )

    await exchange.publish(message, routing_key='extract_png')