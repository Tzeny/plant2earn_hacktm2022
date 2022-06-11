import asyncio
import datetime
import enum
import json
import logging
import os
import time
import pickle

logging.basicConfig(level=logging.INFO)

import torch

from TreeDetectionHandler import TreeDetectionHandler
from models.AlgorithmsAnswear import TreeDetectionAnswer

import pandas as pd
import glob

torch.set_grad_enabled(False)

model_path = "/Segmentation/models/model.pth"

async def process_queue(queue):
    async for message in queue:
        with message.process():
            a = time.time()
            logging.info('Segmentation Starting analysis' + str(datetime.datetime.now()))

            data = json.loads(message.body)
            img_path = data['img_path']

            logging.info(f"{data['id']} starting analysis...")
            if os.path.isfile(img_path):
                # predict on image
                bbox_path = f'{data["output_dir"]}/tree_detection.jpg'

                output = heatmap_handler.detect_tree(img_path, bbox_path)
                message = TreeDetectionAnswer(id=data['id'], bbox_path=bbox_path, coord_om=output['coord_om'], coord_copac=output['coord_copac'])

                await rmq.publish_message(exchange_type='backend_process', message=message.get_json())
                logging.info(f"{data['id']} message sent to rabbitmq, total time: {time.time() - a:.2f}s")
            else:
                logging.info(f"Could not process {data['id']}, file missing from {img_path}...")


if __name__ == "__main__":
    from rabbitmq_connection import RabbitMQHandler

    global rmq
    ENV = os.environ.get('ENV', 'default')

    logging.info(f'Loading handler')
    heatmap_handler = TreeDetectionHandler(model_path)

    queue_name = f'tree_detection_queue'

    if ENV == 'dev':
        from tqdm import tqdm
        import pickle

        input_dir = os.environ['INPUT_DIR']
        output_dir = os.environ['OUTPUT_DIR']

        input_images = [d for d in glob.glob(f'{input_dir}/*') if os.path.isfile(d)]

        for ii in tqdm(input_images):
            output_basepath = f'{output_dir}/{os.path.basename(ii)}'

            output = heatmap_handler.detect_tree(ii, f'{output_basepath}_vis.jpg')
            print(f'Output for {ii}: {output}')
    else:
        logging.info(f'Starting rabbit')
        rmq = RabbitMQHandler(ENV)
        loop = asyncio.get_event_loop()
        consume_queue = loop.run_until_complete(rmq.start_connection(queue_type=queue_name))
        loop.create_task(process_queue(consume_queue))

        loop.run_forever()
