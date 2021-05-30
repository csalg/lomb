from flask_jwt_extended import get_jwt_identity

from api.texts.domain.entities import UserCredentials


def get_credentials():
    jwt_identity = get_jwt_identity()
    return UserCredentials(jwt_identity['username'], jwt_identity['role'], jwt_identity['groups'])

def get_username():
    return get_jwt_identity()['username']
