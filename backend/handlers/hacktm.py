import asyncio
import uuid
import aiohttp
import sys
import os
from datetime import date, datetime
from handlers.handler import Handler
from json import JSONDecodeError
from utils import json_response
from connection import rabbitmq_connection as rmq

from PIL import Image
from io import BytesIO
import base64

class HacktmHandler(Handler):
    def __init__(self, env, db_connection):
        super(HacktmHandler, self).__init__(env, db_connection)
        self.env = env
        self.db_connection = db_connection

    async def segment_leaf(self, request):
        try:
            post_data = await request.json()
            image_b64 = post_data['image']
        except (KeyError, JSONDecodeError) as e:
            return json_response({'message': 'Please provide a proper json body!'}, status=400)

        try:
            img = Image.open(BytesIO(base64.b64decode(image_b64['img'])))
        except:
            return json_response({'message': 'Error decoding image'}, status=400)

        current_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        request_dir = os.path.join(self.FS_PATH, '/' + current_time + '/')

        if not os.path.isdir(request_dir):
            os.makedirs(request_dir)

        img_path = f'{request_dir}/img.jpeg'
        img.save(img_path)

        xray_doc = {
            'id':  str(uuid.uuid4()),
            'time': date.today().strftime("%Y-%m-%d")
        }

        await self.db_connection.save_to_db('segmentation_entries', xray_doc)

        # message = PreprocessExchange(user=username, xray_path=image_path, id=xray_id, token=token,
        #                                      study_time=current_time, isCron=True)
        # await rmq.publish_message(exchange_name=self.PREPROCESS_EXCHANGE, message=message.get_json(),
        #                             env=self.env)