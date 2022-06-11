import base64
import utils
import os
import json
from PIL import Image, ImageFile
from settings import config

ImageFile.LOAD_TRUNCATED_IMAGES = True

S3_BUCKET = config['s3']['bucket_name']
FS_PATH = config['fs'].get('file_system_path', config['fs']['file_system_path_default'])


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

    async def save_to_s3(self, data, img_type):
        paths = []
        for index, type in enumerate(img_type):
            img_path, img_bytes = await self.get_file_info(data, type, index)
            paths.append(img_path)
            # await save_file(path=img_path, data=img_bytes)
        return paths

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


class ChestEnsembleResponse(AlgorithmResponse):

    def generate_triage(self, diagnostics):
        level = 1
        for diag in diagnostics:
            if diag['description'] == 'Medium' or diag['description'] == 'High':
                level = max(level, self.screening_classes[diag['type']])
        return level

    def create_message(self, data, message_path=None, is_fetch_request=False):
        message = super(ChestEnsembleResponse, self).create_message(data, ['heatmap', 'original'], is_fetch_request)
        message['diagnostic'] = data['diagnostic']
        message['diagnostic_result'] = self.generate_triage(data['diagnostic'])
        return message

    async def save_to_s3(self, data, img_type):
        return await super(ChestEnsembleResponse, self).save_to_s3(data, ['CheXVisionHeatMap'])


class CheXVisionResponse(AlgorithmResponse):
    def create_message(self, data, message_path=None, is_fetch_request=False):
        message = super(CheXVisionResponse, self).create_message(data, ['heatmap'], is_fetch_request)

        dis_dict = utils.get_treshold()
        result_diagnostic = []
        for category in data['diagnostic']:
            # for category in data:
            dis = category['type']
            percentage = category['percentage']
            dis_description = {
                'type': dis,
                'percentage': percentage
            }
            if float(percentage) > (float(dis_dict[dis]) + self.dis_difference):
                dis_description['description'] = 'High'
            elif float(percentage) > (float(dis_dict[dis])):
                dis_description['description'] = 'Medium'
            else:
                dis_description['description'] = 'Low'
            result_diagnostic.append(dis_description)

        message['diagnostic'] = result_diagnostic
        return message

    async def save_to_s3(self, data, img_type):
        return await super(CheXVisionResponse, self).save_to_s3(data, ['HeatMap'])


class SingleDisease(AlgorithmResponse):
    def create_message(self, data, message_path=None, is_fetch_request=False):
        message = super(SingleDisease, self).create_message(data, message_path, is_fetch_request)
        message['diagnostic'] = data['diagnostic']
        return message

    async def save_to_s3(self, data, img_type):
        return await super(SingleDisease, self).save_to_s3(data, img_type)


class ELAResponse(SingleDisease):
    def create_message(self, data, message_path=None, is_fetch_request=False):
        message = super(ELAResponse, self).create_message(data, [''], is_fetch_request)
        return message

    async def save_to_s3(self, data, img_type):
        pass


class TBCResponse(SingleDisease):
    def create_message(self, data, message_path=None, is_fetch_request=False):
        message = super(TBCResponse, self).create_message(data, ['heatmap'], is_fetch_request)
        return message

    async def save_to_s3(self, data, img_type):
        return await super(TBCResponse, self).save_to_s3(data, ['heatmap'])


class ScreeningResponse(SingleDisease):
    def create_message(self, data, message_path=None, is_fetch_request=False):
        message = super(ScreeningResponse, self).create_message(data, ['original'], is_fetch_request)
        return message

    async def save_to_s3(self, data, img_type):
        return await super(SingleDisease, self).save_to_s3(data, ['original'])


class BeagleNetResponse(AlgorithmResponse):
    def create_message(self, data, message_path=None, is_fetch_request=False):
        if data['ctr_index'] != 0:
            message = super(BeagleNetResponse, self).create_message(data, ['heatmap'], is_fetch_request)
        else:
            message = super(BeagleNetResponse, self).create_message(data, [], is_fetch_request)
        message['ctr_index'] = data['ctr_index']
        return message

    def save_to_mongo(self, data, xray_path):
        doc = super(BeagleNetResponse, self).save_to_mongo(data, xray_path)
        doc['ctr_index'] = data['ctr_index']
        return doc

    async def save_to_s3(self, data, img_type):
        if data['ctr_index'] != 0:
            return await super(BeagleNetResponse, self).save_to_s3(data, ['heatmap'])
        else:
            return 'no-image'


class PugVisionResponse(AlgorithmResponse):
    def create_message(self, data, message_path=None, is_fetch_request=False):
        orig_path = data['heat_path'][0].replace('bone_subtracted', 'processed')
        data['heat_path'].append(orig_path)
        message = super(PugVisionResponse, self).create_message(data,
                                                                ['bone_subtraction', 'bone_suppression', 'original'],
                                                                is_fetch_request)
        # kind of ugly
        # check if field exists
        # only this algorithm for mura xrays
        if data.get('body_part', False) == 'mura':
            message['diagnostic_result'] = 0
            message['original'] = ''
        return message

    async def save_to_s3(self, data, img_type):
        return await super(PugVisionResponse, self).save_to_s3(data, ['Bone_Subtraction', 'Bone_Suppression'])


class MuraResponse(SingleDisease):
    def create_message(self, data, message_path=None, is_fetch_request=False):
        message = super(MuraResponse, self).create_message(data, ['heatmap', 'original'], is_fetch_request)
        message['diagnostic_result'] = 0
        return message

    async def save_to_s3(self, data, img_type):
        return await super(MuraResponse, self).save_to_s3(data, ['Mura', 'Original'])


class RustyAgeResponse(AlgorithmResponse):
    def create_message(self, data, message_path=None, is_fetch_request=False):
        message = super(RustyAgeResponse, self).create_message(data, [], is_fetch_request)
        message['age'] = data['age']
        return message

    async def save_to_s3(self, data, img_type):
        return ''


class CTResponse(AlgorithmResponse):
    async def save_to_s3(self, data, img_type):
        return ''

    def create_message(self, data, message_path=['original'], is_fetch_request=False):
        message = {
            'id': data['id'],
            'answer_type': data['answer_type'],
            'study_time': data['study_time'],
            'number_of_slices': data['number_of_slices'],
            'original_path': data['original_path'],
            'diagnostic': data['diagnostic']
        }

        return message

    # TODO Refactor Code witch CT and XRAY classes
    def save_to_mongo(self, data, xray_path):
        doc = self.create_message(data)
        return doc


class CTHeadClassificationResponse(CTResponse):

    def create_message(self, data, message_path=None, is_fetch_request=False):
        if message_path is None:
            message_path = ['original']
        # TODO update others instances
        message = super(CTHeadClassificationResponse, self).create_message(data)
        message['binary_preds'] = data.get('binary_preds', None)

        message['diagnostic_result'] = 2
        for diagnostic in data['diagnostic']:
            diag_values = data['diagnostic'][diagnostic]
            if diag_values['label'].lower() == 'abnormal':
                message['diagnostic_result'] = 3

        return message


class CTChestClassificationResponse(CTResponse):

    def create_message(self, data, message_path=None, is_fetch_request=False):
        message = super(CTChestClassificationResponse, self).create_message(data)
        if len(data['diagnostic']) > 0:
            message['diagnostic_result'] = 5
        else:
            message['diagnostic_result'] = 2
        # adding special contours field for CT covid
        # for hospitals without contours in data( old structure)
        if 'contours' in data:
            message['contours'] = data['contours']
        return message

    def save_to_mongo(self, data, xray_path):
        doc = super(CTChestClassificationResponse, self).save_to_mongo(data, xray_path)
        if 'contours' in data:
            doc['contours'] = data['contours']
        else:
            doc['contours'] = 'Strange'
        return doc


class CTCOVIDResponse(CTResponse):

    def create_message(self, data, message_path=None, is_fetch_request=False):
        message = super(CTCOVIDResponse, self).create_message(data)
        return message


class CTOtherClassificationResponse(CTResponse):

    def create_message(self, data, message_path=None, is_fetch_request=False):
        message = super(CTOtherClassificationResponse, self).create_message(data)
        message['diagnostic_result'] = 0

        return message
