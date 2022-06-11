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

from PIL import Image
from io import BytesIO
import base64
import logging
import json
from multiprocessing import Lock

logger = logging.getLogger('aiohttp')

class HacktmHandler(Handler):
    def __init__(self, env, db_connection):
        super(HacktmHandler, self).__init__(env, db_connection)
        self.env = env
        self.db_connection = db_connection

        self.answer_dict = {}
        self.answer_dict_lock = Lock()

    # async def process_algorithms_queue_thread(self, queue):
    #     logger.info('Listening for message in queue')
    #     async for message in queue:
    #         with message.process():
    #             data = json.loads(message.body)

    #             at = data['answer_type']
    #             # 1, data['id'], bbox_path, leaf_path
    #             if at < 0:
    #                 logger.warn(f'Weird answer type for {data}, skipping')
    #                 continue

    #             with self.answer_dict_lock:
    #                 if data['id'] not in self.answer_dict_lock:
    #                     self.answer_dict_lock[data['id']] = {
    #                         'leaf_segmentation': {}, 
    #                         'tree_classification': {},
    #                         'leaf_classification': {}
    #                     }
    #                 self.answer_dict[data['id']]
                    

    async def segment_leaf(self, request):
        # try:
        #     post_data = await request.json()
        #     image_b64 = post_data['image']
        # except (KeyError, JSONDecodeError) as e:
        #     return json_response({'message': 'Please provide a proper json body!'}, status=400)

        # try:
        #     img = Image.open(BytesIO(base64.b64decode(image_b64['img'])))
        # except:
        #     return json_response({'message': 'Error decoding image'}, status=400)

        try:
            reader = await request.multipart()
            logger.info('Received images...')

            image_uploaded = await reader.next()

            if image_uploaded is None:
                raise ValueError(f'No images in the request')

            # check if file filed exist
            if 'file' not in image_uploaded.name:
                raise AttributeError('Wrong field name for part')

            current_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            request_dir = os.path.join(self.FS_PATH, '/' + current_time + '/')
            img_path = f'{request_dir}/img.jpeg'

            if not os.path.isdir(request_dir):
                os.makedirs(request_dir)

            with open(f'{img_path}', 'wb') as f:
                while True:
                    chunk = await image_uploaded.read_chunk(size=8192)
                    if not chunk:
                        break
                    f.write(chunk)
        except Exception as e:
            logger.exception(f'Error receiving image')
            return json_response({'message': f'Error receiving image: {e}'}, status=400)
        
        img_id = str(uuid.uuid4())

        leaf_doc = {
            'id':  img_id,
            'time': date.today().strftime("%Y-%m-%d"),
            'path': img_path,
        }

        await self.db_connection.save_to_db('segmentation_entries', leaf_doc)

        message = AlgorithmExchangeMessage(img_path=img_path, id=img_id)
        # await rmq.publish_message(exchange_name='leaf_segmentation_exchange', message=message.get_json(), env=self.env)

        # return {
        #     'bbox_image': 'url',
        #     'black_image': 'url',
        #     'leaf_class':
        # }
        return json_response({'message': f'Ok'}, status=200)

    # def detect_tree():
    #     in {
    #         'image': 'base64'
    #     }

    #     return {
    #         'coord_copac': [x1, y1, x2, y2],
    #         'coord_om': [x1, y1, x2, y2],
    #         'bbox_image': 'url'
    #     }

    def generate_nft():
        in {
            'geolocation':
            'tree_type': 
            'tree_age': 
        }

        // calculate  co2_absorbtion
        // generate+save image
        // create contract
        // insert into db

        // nft
        {
            'id': ,
            'username': , + username address ETH + semnatura dinamica
            'nft_image': ,
            'ipfs_url': ,
            'forest_name': ,
            'price': [
                {
                    'timestamp': <time>,
                    'price': <price>
                }
            ]
            'creation_time': ,
            'co2_absorbtion': ,
        }

        return {
            'nft_image': 'url',
            'nft_hast': ,
            'co2_absorbtion'
        }

        message = PreprocessExchange(user=username, xray_path=image_path, id=xray_id, token=token,
                                             study_time=current_time, isCron=True)
        await rmq.publish_message(exchange_name=self.PREPROCESS_EXCHANGE, message=message.get_json(),
                                    env=self.env)