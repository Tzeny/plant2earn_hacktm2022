import motor.motor_asyncio
import motor
from models.ResponseTypes import *
import logging

logger = logging.getLogger('aiohttp')

MONGO_PORT = config['mongodb']['port']

class DatabaseConnection:
    # mongo connection
    def __init__(self, env):
        mongo_ip = config['mongodb'].get('ip_' + env, config['mongodb']['ip_default'])
        mongo_url = f"mongodb://{config['mongodb']['user']}:{config['mongodb']['password']}@{mongo_ip}:{MONGO_PORT}"
        client = motor.motor_asyncio.AsyncIOMotorClient(mongo_url)
        self.db = client.plant2win

        logger.info(f"Database connection configured with url: {mongo_url}...")

    async def save_to_db(self, collection, document):
        _id = await self.db[collection].insert_one(document)
        return _id

    async def delete_many(self, collection, query):
        return await self.db[collection].delete_many(query)

    async def find_one(self, collection, query):
        return await self.db[collection].find_one(query)

    def find(self, collection, query):
        return self.db[collection].find(query)

    def find_random(self, collection, query, limit):
        return self.db[collection].aggregate([
            {'$match': query},
            {'$sample': {'size': limit}}
        ])

    async def update_one_array(self, collection, column, document, query):
        return await self.db[collection].update_one(query, {'$push': {column: document}})

    async def update_value(self, collection, column, value, query):
        return await self.db[collection].update_one(query, {'$set': {column: value}})

    async def update_many(self, collection, column, value, query):
        return await self.db[collection].update_many(query, {'$set': {column: value}})

    async def update_multiple_value(self, collection, values, query):
        return await self.db[collection].update_one(query, {'$set': values})
