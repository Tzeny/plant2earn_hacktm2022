import asyncio
import datetime
import json
import logging
import os
import shutil
import time

logging.basicConfig(level=logging.INFO)

import numpy as np
import torch

from xfastai.attention_heatmap import AttentionHeatmapHandler
from models.AlgorithmsAnswear import TreeClassificationAnswer

torch.set_grad_enabled(False)

# logging.basicConfig(level=logging.DEBUG)

run_type_settings = {
    'model_path': "/TreeClassification/models/best_model.pth",
    'tile_grid_size': [10, 10],
    'target_size': (256, 256),
    'image_read_type': 'skimage',
    'model_type': 'simple_densenet121',
    'attention': False,
}

classes_list = ['sour cherry', 'fig', 'cherry', 'apple', 'birch']


async def process_queue(queue):
    async for message in queue:
        with message.process():
            a = time.time()
            logging.info('Classification Starting analysis' + str(datetime.datetime.now()))

            data = json.loads(message.body)
            img_path = data['img_path']

            logging.info(f"{data['id']} starting analysis...")
            if os.path.isfile(img_path):
                predictions = heatmap_handler.process_image(img_path, '/tmp/meh.jpeg', attention=attention)[0]
                pred_class = classes_list[np.argmax(predictions)]

                message = TreeClassificationAnswer(id=data['id'], tree_class=pred_class)

                await rmq.publish_message(exchange_type='backend_process', message=message.get_json())
                logging.info(f"{data['id']} message sent to rabbitmq, total time: {time.time() - a:.2f}s")
            else:
                logging.info(f"Could not process {data['id']}, file missing from {img_path}...")

if __name__ == "__main__":
    ENV = os.environ.get('ENV', 'default')

    model_path = run_type_settings['model_path']
    target_size = run_type_settings['target_size']
    tile_grid_size = run_type_settings['tile_grid_size']
    image_read_type = run_type_settings['image_read_type']
    model_type = run_type_settings['model_type']
    attention = run_type_settings['attention']

    heatmap_handler = AttentionHeatmapHandler(model_path, classes_list, 'chest_diag', target_size,
                                              use_clahe=True, tile_grid_size=tile_grid_size, image_read_type=image_read_type, model_type=model_type)

    queue_name = f'tree_classification_queue'

    if ENV == 'dev':
        from tqdm import tqdm
        import glob

        input_dir = os.environ['INPUT_DIR']
        output_dir = os.environ['OUTPUT_DIR']

        input_images = [d for d in glob.glob(f'{input_dir}/*') if os.path.isfile(d)]

        for ii in tqdm(input_images):
            predictions = heatmap_handler.process_image(ii, '/tmp/meh.jpeg', attention=attention)[0]
            pred_class = classes_list[np.argmax(predictions)]
            logging.info(f'Predictions {predictions}: {pred_class}')
    else:
        from rabbitmq_connection import RabbitMQHandler

        logging.info('Container running in production mode')
        global rmq

        rmq = RabbitMQHandler(ENV)
        loop = asyncio.get_event_loop()
        consume_queue = loop.run_until_complete(rmq.start_connection(queue_type=queue_name))
        loop.create_task(process_queue(consume_queue))

        loop.run_forever()
