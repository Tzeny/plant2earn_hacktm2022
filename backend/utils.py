import jwt
import json
from settings import config
from aiohttp import web
import logging
import magic
import csv
import hashlib
from bson import json_util
from PIL import Image, ImageFile
import datetime
import numpy as np
import itertools
from paramiko import SSHClient, AutoAddPolicy
from scp import SCPClient
import os
import logging

logger = logging.getLogger('aiohttp')

ImageFile.LOAD_TRUNCATED_IMAGES = True

mime = magic.Magic(mime=True)

JWT_SECRET = config['jwt']['JWT_SECRET']
JWT_ALGORITHM = config['jwt']['JWT_ALGORITHM']
JWT_EXP_DELTA_SECONDS = config['jwt']['JWT_EXP_DELTA_SECONDS']

def make_thumbnail(path):
    logger.debug(f'Path is {path}')
    image = Image.open(path)
    size = (256, 256)
    image.thumbnail(size, Image.ANTIALIAS)
    new_filename = 't_' + path.split('/')[-1]
    new_path = path.replace(path.split('/')[-1], new_filename)
    image.save(new_path, 'PNG')
    return new_path

def web_message(text, status):
    return web.Response(text=text, status=status)

def datetime_converter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()

def json_response(body, **kwargs):
    kwargs['body'] = json.dumps(body or kwargs['body'], default=datetime_converter).encode(
        'utf-8')  # TODO: this fails on empty query results
    kwargs['content_type'] = 'text/json'
    return web.Response(**kwargs)

async def check_jwt(jwt_token):
    try:
        jwt.decode(jwt_token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except (jwt.DecodeError, jwt.ExpiredSignatureError):
        return True
    return False

def encrypt_string(hash_string):
    sha_signature = \
        hashlib.sha256(hash_string.encode()).hexdigest()
    return sha_signature