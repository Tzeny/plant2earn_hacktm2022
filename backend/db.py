from pymongo import MongoClient
import hashlib

def encrypt_string(hash_string):
    sha_signature = \
        hashlib.sha256(hash_string.encode()).hexdigest()
    return sha_signature

class DB:
    def __init__(self, config):
        self.mongo_uri = config['database']['uri']

        self.JWT_SECRET = config['jwt']['JWT_SECRET']
        self.JWT_ALGORITHM = 'HS256'
        self.JWT_EXP_DELTA_SECONDS = float(config['jwt']['JWT_EXP_DELTA_SECONDS'])

    def login(self, username, password):
        with MongoClient(self.mongo_uri) as client:
            document = client.xvision.find_one('users', {'username': username, 'password': encrypt_string(password)})

            jwt_token = jwt.encode(payload, self.JWT_SECRET, self.JWT_ALGORITHM)
            logger.info(f'User {username} logged in.')
            user_info = {
                'auth_token': jwt_token.decode('utf-8'),
                'expires_in': self.JWT_EXP_DELTA_SECONDS,
                'username': username,
                'name': user_data['name'],
                'limit': user_data['limit'],
                'role': user_data['role']
            }
            return json_response(user_info)

    def 