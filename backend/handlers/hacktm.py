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
from models.RMQModels import AlgorithmExchangeMessage
from aiohttp import web

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
        img_id = str(uuid.uuid4())
        img.save(img_path)

        xray_doc = {
            'id':  img_id,
            'time': date.today().strftime("%Y-%m-%d"),
            'path': img_path
        }

        await self.db_connection.save_to_db('segmentation_entries', xray_doc)

        message = AlgorithmExchangeMessage(img_path=img_path, id=img_id)
        await rmq.publish_message(exchange_name='leaf_segmentation_exchange', message=message.get_json(), env=self.env)

        return {
            'bbox_image': 'url',
            'black_image': 'url',
            'leaf_class':""
        }
    def json_response(body, **kwargs):
        kwargs['body'] = json.dumps(body or kwargs['body'], default=datetime_converter).encode(
            'utf-8')  # TODO: this fails on empty query results
        kwargs['content_type'] = 'text/json'
        return web.Response(**kwargs)

    async def retrieve_latest_nfts(self,request):
        nfts_answer = []
        nfts = await self.db_connection.find('nfts', {'id':{'$exists':True}})
        async for doc in nfts:
            doc['_id'] = str(doc['_id'])
            nfts_answer.append(doc)
        return json_response(nfts_answer)

    # def detect_tree():
    #     in {
    #         'image': 'base64'
    #     }

    #     return {
    #         'coord_copac': [x1, y1, x2, y2],
    #         'coord_om': [x1, y1, x2, y2],
    #         'bbox_image': 'url'
    #     }

    # def generate_nft():
    #     in {
    #         'geolocation':
    #         'tree_type': 
    #         'tree_age': 
    #     }

    #     // calculate  co2_absorbtion
    #     // generate+save image
    #     // create contract
    #     // insert into db

    #     // nft
    #     {
    #         'id': ,
    #         'username': ,
    #         'nft_image': ,
    #         'forest_name': ,
    #         'price': [
    #             {
    #                 'timestamp': <time>,
    #                 'price': <price>
    #             }
    #         ]
    #         'creation_time': ,
    #         'co2_absorbtion': ,
    #     }

    #     return {
    #         'nft_image': 'url',
    #         'nft_hast': ,
    #         'co2_absorbtion'
    #     }

        # message = PreprocessExchange(user=username, xray_path=image_path, id=xray_id, token=token,
        #                                      study_time=current_time, isCron=True)
        # await rmq.publish_message(exchange_name=self.PREPROCESS_EXCHANGE, message=message.get_json(),
        #                             env=self.env)