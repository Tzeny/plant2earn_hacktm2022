from models.Users import User
from utils import json_response, check_jwt, encrypt_string
from bson import json_util
import jwt
from handlers.handler import Handler
from json import JSONDecodeError
from datetime import datetime, timedelta
import logging
from settings import config

logger = logging.getLogger('aiohttp')

JWT_SECRET = config['jwt']['JWT_SECRET']
JWT_ALGORITHM = 'HS256'
JWT_EXP_DELTA_SECONDS = float(config['jwt']['JWT_EXP_DELTA_SECONDS'])

whitelist = ['login', 'register', 'doc', 'ws', 'partner', 'mail-confirmation', '']


class AccountHandler(Handler):
    def __init__(self, env, backend_type, db_connection):
        super(AccountHandler, self).__init__(env, db_connection)
        self.backend_type = backend_type

        # normal for pacs
        # index at which to split the request for login
        # different on cloud vs pacs
        self.index = 3

    async def auth_middleware(self, app, handler):
        async def middleware(request):
            if request.method == 'OPTIONS':
                return await handler(request)
            jwt_token = request.headers.get('Authorization', None)
            # TODO check with await for security to verify JWT
            if not check_jwt(jwt_token):
                return json_response({'message': 'Token is invalid'}, status=400)
            # spliting for request route
            logger.debug(f'Request URL {request.url}')
            url_part = str(request.url).split('/')[self.index]
            if '?' in url_part:
                url_part = url_part.split('?')[0]
            if url_part in whitelist or jwt_token:
                return await handler(request)
            else:
                return json_response({"message": "You don't have access to this resource"}, status=405)

        return middleware

    async def login(self, request):
        try:
            post_data = await request.json()
            username = post_data['username']
            password = post_data['password']
        except (KeyError, JSONDecodeError) as e:
            return json_response({'message': 'Please provide a proper json body!'}, status=400)

        document = await self.db_connection.find_one('users',
                                                     {'username': username, 'password': encrypt_string(password)})
        try:
            logger.info(document)
            logger.info(json.dumps(document, default=json_util.default))
            user_data = json.loads(json.dumps(document, default=json_util.default))
            user = User(**user_data)
        except (KeyError, TypeError) as e:
            logger.info(e)
            logger.info('Bad Request! User ' + username + ' tried to log in.')
            return json_response({'message': 'Wrong username or password'}, status=401)

        payload = {
            'user_id': user._id,
            'username': username,
            'exp': datetime.utcnow() + timedelta(seconds=JWT_EXP_DELTA_SECONDS)
        }
        jwt_token = jwt.encode(payload, JWT_SECRET, JWT_ALGORITHM)
        logger.info(f'User {username} logged in.')
        user_info = {
            'auth_token': jwt_token.decode('utf-8'),
            'expires_in': JWT_EXP_DELTA_SECONDS,
            'username': username,
            'name': user_data['name'],
        }
        return json_response(user_info)

    async def register(self, request):
        post_data = await request.json()
        name = post_data['name']
        email = post_data['email']
        password = post_data['password']
        profession = post_data['profession']
        university = post_data['university']
        country = post_data['country']
        contact_number = post_data['contact_number']
        document = await self.db_connection.find_one('users', {'username': email})
        if document is None:
            document = {
                'name': name,
                'username': email,
                'password': encrypt_string(password),
                'profession': profession,
                'country': country,
                'contact_number': contact_number,
                'limit': 10,
                'mail_confirmation': False,
                'role': ['upload']
            }
            if profession == 'Student':
                document['university'] = university
                document['role'].append('learn')
                document['role'].append('history')
            _id = await self.db_connection.save_to_db('users', document)
            return \
                json_response({
                    'message': 'User registered!'
                })
        else:
            return \
                json_response({
                    'message': 'User already registered!'
                }, status=400)
