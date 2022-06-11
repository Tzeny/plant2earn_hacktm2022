import base64
import utils
import os
import json
from PIL import Image, ImageFile
from settings import config

ImageFile.LOAD_TRUNCATED_IMAGES = True

FS_PATH = config['fs'].get('file_system_path', config['fs']['file_system_path_default'])

class AlgorithmExchangeMessage():
    def get_json(self):
        return json.dumps(self.__dict__).encode('utf8')

    def __init__(self, img_path, id):
        self.id = id
        self.img_path = img_path

class AlgorithmResponse:
    def create_message(self, data, message_path=None, is_fetch_request=False):
        message = {
            'heat_id': data['heat_id'],
            'answer_type': data['answer_type'],
            'id': data['id'],
            'study_time': data['study_time'],
            # 'server_path': data['heat_path']
        }
        for index, path in enumerate(message_path):
            new_path = utils.make_thumbnail(data['heat_path'][index])
            with open(str(new_path), "rb") as image_file:
                img_bytes = base64.b64encode(image_file.read())
            os.remove(new_path)

            if is_fetch_request and path == 'original' and data['isUpload'] != 'UPLOAD':
                # if we're just fetching already processed images and need the original dicom file
                # orig path will contain /processed/img.jpeg - remove and replace with dicom counterparts
                message[f"{path}_path"] = f"{'/'.join(data['heat_path'][index].split('/')[:-2])}/dicom/1.dcm"

            else:
                message[path + '_path'] = data['heat_path'][index]

            message[path] = img_bytes.decode('utf-8')
        return message

    def save_to_mongo(self, data, xray_path):
        document = {
            'id': data['id'],
            'user': data['user'],
            'heat_id': data['heat_id'],
            'study_time': data['study_time'],
            'heat_path': xray_path,
            'answer_type': data['answer_type']
        }
        try:
            document['diagnostic'] = data['diagnostic']
            document['screening_percentage'] = data['screening_percentage']
        except KeyError:
            pass
        return document

    async def get_file_info(self, data, img_type, pos=0):
        with open(data['heat_path'][pos], "rb") as image_file:
            img_bytes = image_file.read()

        img_path = utils.create_path(data, type=img_type, folder=config['s3']['xray'])

        return img_path, img_bytes


class ChestAlgorithmResponse(AlgorithmResponse):

    def create_message(self, data, message_path=None, is_fetch_request=False):
        message = super(ChestAlgorithmResponse, self).create_message(data, ['heatmap', 'original'], is_fetch_request)
        message['diagnostic'] = data['diagnostic']
        message['screening_percentage'] = data['screening_percentage']
        return message

    async def save_to_s3(self, data, img_type):
        return await super(ChestAlgorithmResponse, self).save_to_s3(data, ['HeatMap', 'Original'])