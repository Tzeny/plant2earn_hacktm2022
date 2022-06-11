import logging
from models.ResponseTypes import *
from universal_analytics import Tracker, AsyncHTTPRequest
from settings import config
import asyncio
import logging

logger = logging.getLogger('aiohttp')


class Handler:
    def __init__(self, env, db_connection):
        self.FS_PATH = config['fs'].get('file_system_path_' + env, config['fs']['file_system_path_default'])
        self.env = env
        self.db_connection = db_connection
        http = AsyncHTTPRequest()
        user_info = 'UA-93881082-2'
        self.tracker = Tracker(user_info, http, client_id=self.env)

    async def send_event(self, category, action, label, headers, check_internet=True):
        if 'Referer' in headers:
            url = headers['Referer']
        else:
            url = 'dummy'
        # if no referer just send metrics to GA
        # Send an event
        if 'localhost' not in str(url):
            if config['internet'].get(self.env, config['internet']['default']):
                logger.debug(f'Sending google analytics event! {category}, {action}, {label}')
                asyncio.create_task(self.tracker.send("event", category, action, label + '_backend'))
