import asyncio
import datetime
import enum
import json
import logging
import os
import time
import pickle

import torch

from SegmentationHandler import SegmentationHandler
from models.AlgorithmsAnswear import SegmentationAnswer

import pandas as pd
import glob

torch.set_grad_enabled(False)

model_path = "/Segmentation/models/model.pth"

async def process_queue(queue):
    async for message in queue:
        with message.process():
            logging.info('Segmentation Starting analysis' + str(datetime.datetime.now()))

            data = json.loads(message.body)
            img_path = data['img_path']
            output_basepath = f'{output_dir}/{os.path.basename(img_path)}'

            logging.info(f"{data['id']} starting analysis...")
            if os.path.isfile(img_path):
                # predict on image
                bbox_path = f'{output_basepath}_1.jpeg'
                leaf_path = f'{output_basepath}_2.jpeg'
                heatmap_handler.segment_leaf(img_path, bbox_path, leaf_path)

                logging.info(f"{data['id']} finishing analysis...")

                message = SegmentationAnswer(data['id'], bbox_path, leaf_path)
                await rmq.publish_message(exchange_type='ai_algorithms_response', message=message.get_json())

                logging.debug(f"{data['id']} message sent to rabbitmq...")
            else:
                logging.info(f"Could not process {data['id']}, file missing from {img_path}...")


if __name__ == "__main__":
    from rabbitmq_connection import RabbitMQHandler

    global rmq
    ENV = os.environ['ENV']

    heatmap_handler = SegmentationHandler(model_path)

    queue_name = f'leaf_segmentation_exchange'

    if ENV == 'dev':
        from tqdm import tqdm
        input_dir = os.environ['INPUT_DIR']
        output_dir = os.environ['OUTPUT_DIR']

        input_images = [d for d in glob.glob(f'{input_dir}/*') if os.path.isfile(d)]

        for ii in tqdm(input_images):
            output_basepath = f'{output_dir}/{os.path.basename(ii)}'
            heatmap_handler.segment_leaf(ii, f'{output_basepath}_1.jpeg', f'{output_basepath}_2.jpeg')
    else:
        rmq = RabbitMQHandler(ENV)
        loop = asyncio.get_event_loop()
        consume_queue = loop.run_until_complete(rmq.start_connection(queue_type=queue_name))
        loop.create_task(process_queue(consume_queue))

        loop.run_forever()
