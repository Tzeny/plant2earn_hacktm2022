import numpy as np
import torch
from PIL import ImageFile

ImageFile.LOAD_TRUNCATED_IMAGES = True
from torchvision.transforms import ToTensor, ToPILImage
import logging
import collections

from fastai.vision.transform import get_transforms, crop_pad

from fastai.vision import TfmPixel
import albumentations as A
from albumentations import CLAHE
from fastai.vision import pil2tensor

toTensor = ToTensor()
toPIL = ToPILImage()

imagenet_stats = ([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
imagenet_mean = torch.Tensor(imagenet_stats[0])
imagenet_std = torch.Tensor(imagenet_stats[1])


def normalize(image, mean, std):
    "Normalize `x` with `mean` and `std`."
    # print(f'Normalize image shape: {image.shape}, mean shape: {mean.shape}, std shape: {std.shape}')
    if len(image.shape) == 3:
        return (image.float() - mean[..., None, None]) / std[..., None, None]
    elif len(image.shape) == 4:
        return (image.float() - mean[None, ..., None, None]) / std[None, ..., None, None]
    else:
        raise ValueError(len(image.shape))


def denormalize(image, mean, std):
    "Denormalize `x` with `mean` and `std`."
    return image.cpu().float() * std[..., None, None] + mean[..., None, None]


# helper funcion for albumentations
def tensor2np(x):
    np_image = x.data.cpu().permute(1, 2, 0).numpy()
    np_image = (np_image * 255).astype(np.uint8)

    return np_image


# helper funcion for albumentations
def tensor2np(x):
    np_image = x.cpu().permute(1, 2, 0).numpy()
    np_image = (np_image * 255).astype(np.uint8)

    return np_image


# helper funcion for albumentations
def alb_tfm2fastai(alb_tfm):
    def _alb_transformer(x):
        # tensor to numpy
        np_image = tensor2np(x)

        # apply albumentations
        transformed = alb_tfm(image=np_image)['image']

        # back to tensor
        tensor_image = pil2tensor(transformed, np.float32)
        tensor_image.div_(255)

        return tensor_image

    return TfmPixel(_alb_transformer)()


def get_clahe_transform(clip_limit=(2, 2), tile_grid_size = [8, 8]):
    valid_tfms = get_transforms(do_flip=False, max_rotate=0, max_zoom=0, max_lighting=0, max_warp=0, p_affine=0,
                                p_lighting=0,
                                xtra_tfms=[alb_tfm2fastai(A.Compose([CLAHE(always_apply=True, clip_limit=(2, 2), tile_grid_size=tile_grid_size)]))])

    return valid_tfms[0][1:]


def prediction_transformation(x, operating_point):
    return np.where(x < operating_point, x / (2 * operating_point), 1 - (1 - x) / (2 * (1 - operating_point)))


def pretrain_model_from_path(model, path):
    logging.info(f'Loading old model from {path}')
    old_model_dict = torch.load(path, map_location='cpu')

    if not isinstance(old_model_dict, collections.OrderedDict):
        try:
            old_model_dict = old_model_dict.state_dict()
        except:
            old_model_dict = old_model_dict['model']

    if 'model' in old_model_dict:
        old_model_dict = old_model_dict['model']

    model_dict = model.state_dict()

    pretrained_state = {k: v for k, v in old_model_dict.items() if k in model_dict and v.size() == model_dict[k].size()}

    # incearca si cu replace in caz ca are prefixul ala ciudat
    if len(pretrained_state) == 0:
        pretrained_state = {k.replace("0.0", "features"): v for k, v in old_model_dict.items() if
                            k.replace("0.0", "features") in model_dict and v.size() == model_dict[
                                k.replace("0.0", "features")].size()}

    logging.debug(f'Old model dict has {len(pretrained_state.keys())} keys')

    logging.info(f'Keys updated: {len(pretrained_state.keys())} / {len(model_dict.keys())}')

    logging.info(f'Keys left out: {set(model_dict.keys()) - set(pretrained_state.keys())}')

    print(f'Keys updated: {len(pretrained_state.keys())} / {len(model_dict.keys())}')
    model_dict.update(pretrained_state)
    model.load_state_dict(model_dict)

    return model
