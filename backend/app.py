import os
from aiohttp import web
import sys
from handlers.account import AccountHandler
from handlers.hacktm import HacktmHandler
from connection.database_connection import DatabaseConnection
import ssl
import aiohttp_cors
from settings import config
from log import create_logging_config

JWT_SECRET = config['jwt']['JWT_SECRET']
JWT_ALGORITHM = 'HS256'
JWT_EXP_DELTA_SECONDS = float(config['jwt']['JWT_EXP_DELTA_SECONDS'])

APP_IP = config['app']['ip']
APP_PORT = config['app']['port']


async def hello(request):
    return web.Response(text="Welcome to the dark side!")


if __name__ == "__main__":

    backend_type = 'cloud'
    place = 'localhost'

    # logger
    aio_logger = create_logging_config('Backend')
    aio_logger.info(f'Starting application with config of backend_type: {backend_type} and place: {place}')

    db_connection = DatabaseConnection(place)

    # Login Handler
    account_handler = AccountHandler(place, backend_type, db_connection)
    hacktm_handler = HacktmHandler(place, db_connection, config)

    api = web.Application()

    # setup server and routes

    api.router.add_route('GET', '/', hello)

    api.router.add_route('POST', '/login', account_handler.login)
    api.router.add_route('POST', '/register', account_handler.register)

    api.router.add_route('POST', '/hacktm/segment_leaf', hacktm_handler.detect_tree)
    api.router.add_route('POST', '/hacktm/detect_tree', hacktm_handler.detect_tree)
    api.router.add_route('GET', '/hacktm/nft/retrieve', hacktm_handler.retrieve_latest_nfts)

    ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    ssl_context.load_cert_chain('nginx/ssl_keys/domain_srv.crt', 'nginx/ssl_keys/domain_srv.key')

    aio_logger.info('Adding ssl context...')

    app = api
    aio_logger.info(f'Application started on ip: {APP_IP} with port: {APP_PORT}...')

    web.run_app(app, host=APP_IP, port=APP_PORT)
