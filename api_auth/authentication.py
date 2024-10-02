from datetime import datetime, timedelta, timezone
import base64
import json
import logging
import os

import requests

from django.conf import settings

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

    if auth_config["type"] == "OAUTH":
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
            header["organization-token"] = settings.AUTH_CONFIG["S2S"]["sign"]["ORGANIZATION_TOKEN"]
        except FileNotFoundError:
            logging.error("Token file %s not found. Generating a new token.", oauth_token_path)
            token = retrieve_oauth_token(oauth_setting=settings.AUTH_CONFIG["S2S"]["sign"])
            header["Authorization"] = f'Bearer {token}'

    elif auth_config["type"] is None:
        return request.headers

    return header

