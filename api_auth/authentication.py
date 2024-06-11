from datetime import datetime, timedelta, timezone
import base64
import json
import logging
import os
import uuid

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from jwt import PyJWKClient, decode, exceptions as jwt_exceptions
import jwt
import requests

from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from rest_framework import authentication
from rest_framework import exceptions as drf_exceptions



def generate_jwt_token(user_id='1', private_key_path=settings.PRIVATE_KEY_PATH, algorithm=settings.ALGORITHM, kid=settings.KID):

    with open(private_key_path, 'rb') as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
            backend=default_backend()
        )
    
    current_time = datetime.now(timezone.utc)
    payload = {
        "exp": current_time + timedelta(minutes=60),
        "nbf": current_time,
        "jti": str(uuid.uuid4()),
        "user_id": user_id,
        "token_type": "access",
    }
    
    headers = {"kid": kid}
    token = jwt.encode(payload, private_key, algorithm=algorithm, headers=headers)
    
    return token


def retrieve_oauth_token(oauth_setting=settings.AUTH_CONFIG["S2S"]["sign"]):
    credential = "{0}:{1}".format(oauth_setting["CLIENT_ID"], oauth_setting["SECRET"])
    credential = base64.b64encode(credential.encode("utf-8"))
    headers = {
        'Authorization': 'Basic {}'.format(credential.decode('utf8')),
        'Content-Type': 'application/x-www-form-urlencoded;',
        'Accept': 'application/json, text/plain, */*',
        'Access-Control-Allow-Origin': '*',
    }
    params = {
        "grant_type": "client_credentials",
        "organization_token": oauth_setting["ORGANIZATION_TOKEN"],
    }

    response = requests.post(url=oauth_setting["URL"], data=params, headers=headers, timeout=10)

    token_access_response = json.loads(response.content)

    # Store expiry time 
    expiry_time = datetime.now(timezone.utc) + timedelta(seconds=token_access_response.get("expires_in"))
    token_access_response["expiry_time"] = expiry_time.isoformat()

    # Store token informations
    access_token = token_access_response.get("access_token")
    oauth_token_path = os.path.join(settings.KEYS_DIR, 'oauth_token.json')
    with open(oauth_token_path, 'w') as f:
        json.dump(token_access_response, f, indent=4)

    return access_token


def is_access_token_valid(token_access_data: dict) -> bool:
    current_time_utc = datetime.now(timezone.utc)
    token_expiry_time = token_access_data.get("expiry_time")
    return current_time_utc < datetime.fromisoformat(token_expiry_time)

def generate_signature(auth_config: dict, request=None) -> dict:
    """
    Generate request header
    ---
    Parameters:
    - auth_config (dict): should pass settings.AUTH_CONFIG[""]
    - request (dict): The request data

    Returns:
    - header (dict): the configured header
    """

    header = {
        "Accept": "application/json"
    }

    if auth_config["type"] == "JWK":
        token = generate_jwt_token(
            user_id='1',
            private_key_path=settings.PRIVATE_KEY_PATH,
            algorithm=settings.ALGORITHM,
            kid=settings.KID,
        )
        header["Authorization"] = token

    elif auth_config["type"] == "OAUTH":
        # RETRIEVE TOKEN FILE
        oauth_token_path = os.path.join(settings.KEYS_DIR, 'oauth_token.json')
        try:
            with open(oauth_token_path, 'r', encoding='utf-8') as token_file:
                token_access_data = json.load(token_file)

            # TEST TOKEN VALIDITY
            if not is_access_token_valid(token_access_data):
                token = retrieve_oauth_token(oauth_setting=settings.AUTH_CONFIG["S2S"]["sign"])
            else:
                token = token_access_data.get("access_token")

            # GENERATE OAUTH HEADER
            header["Authorization"] = 'Bearer ' + token
        except FileNotFoundError:
            logging.error("Token file %s not found. Generating a new token.", oauth_token_path)
            token = retrieve_oauth_token(oauth_setting=settings.AUTH_CONFIG["S2S"]["sign"])
            header["Authorization"] = f'Bearer {token}'

    elif auth_config["type"] is None:
        return request.headers

    return header



class CustomJWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_header = authentication.get_authorization_header(request).split()
        if not auth_header or auth_header[0].lower() != b'bearer':
            return None

        if len(auth_header) != 2:
            raise drf_exceptions.AuthenticationFailed('Invalid token header.')

        try:
            token = auth_header[1].decode('utf-8')
        except UnicodeError:
            raise drf_exceptions.AuthenticationFailed('Invalid token header.')

        # Iterate over the JWKS URLs
        jwks_urls = {
            'C2S' : settings.AUTH_CONFIG['C2S']["auth"]["link"],
            'S2S' : settings.AUTH_CONFIG['S2S']["auth"]["link"],
            'S2S_INTERNAL' : settings.AUTH_CONFIG['S2S_INTERNAL']["link"]
        }
        for jwks_url in jwks_urls.values():
            is_decoded, user = self.try_decode_token(token, jwks_url)
            if is_decoded:
                return (user, token)

        # If decoding fails for all JWKS URLs
        raise drf_exceptions.AuthenticationFailed('Unable to verify the token with any provided JWKS URLs.')

    def try_decode_token(self, token, jwks_url):
        jwks_client = PyJWKClient(jwks_url)
        try:
            signing_key = jwks_client.get_signing_key_from_jwt(token)
            decoded_token = decode(
                token,
                signing_key.key,
                algorithms=["RS256"],
                options={"verify_aud": False}
            )
            return True, AnonymousUser()
        except jwt_exceptions.InvalidTokenError as e:
            return False, None

        except jwt_exceptions.PyJWKClientError as e:
            return False, None