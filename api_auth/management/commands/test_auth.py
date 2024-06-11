import json
import os
import uuid
from datetime import datetime
from datetime import timedelta
from datetime import timezone
from unittest.mock import Mock

import jwt
import requests
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from django.conf import settings
from django.core.management.base import BaseCommand

from api_auth.authentication import generate_signature
from api_auth.authentication import is_access_token_valid
from api_auth.authentication import retrieve_oauth_token


def generate_jwt_token(
    user_id="1",
    private_key_path=settings.TEST_PRIVATE_KEY_PATH,
    algorithm=settings.ALGORITHM,
    kid=settings.TEST_KID,
):
    with open(private_key_path, "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(), password=None, backend=default_backend()
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


def simulate_api_call(token, base_url="http://localhost:8000"):
    headers = {"Authorization": f"Bearer {token}"}
    auth_check_url = f"{base_url}/api/auth/auth-check/"

    auth_response = requests.get(auth_check_url, headers=headers)
    print(f"Auth Check Status Code: {auth_response.status_code}")

    try:
        print(f"Auth Check Response JSON: {auth_response.json()}")

    except ValueError:
        print("Auth Check Response could not be decoded as JSON.")
        print(f"Auth Check Response Content: {auth_response.content}")


def test_health_endpoint(base_url="http://localhost:8000"):
    health_check_url = f"{base_url}/health/"
    health_response = requests.get(health_check_url)
    print(f"Health Check Status Code: {health_response.status_code}")
    try:
        print(f"Health Check Response JSON: {health_response.json()}")
    except ValueError:
        print("Health Check Response could not be decoded as JSON.")
        print(f"Health Check Response Content: {health_response.content}")


def test_jwks_endpoint(jwks_endpoint_url):
    # Send a request to the JWKS endpoint
    jwks_response = requests.get(jwks_endpoint_url)

    # Print the response status code and JSON content
    print(f"JWKS Endpoint Status Code: {jwks_response.status_code}")

    try:
        print(f"JWKS Endpoint Response JSON: {jwks_response.json()}")

    except ValueError:
        print("JWKS Endpoint Response could not be decoded as JSON.")
        print(f"JWKS Endpoint Response Content: {jwks_response.content}")


def simulate_api_call_with_invalid_token(base_url="http://localhost:8000"):
    # Use a clearly invalid token
    invalid_token = "this.is.not.a.valid.token"

    headers = {"Authorization": f"Bearer {invalid_token}"}
    auth_check_url = f"{base_url}/api/auth/auth-check/"

    auth_response = requests.get(auth_check_url, headers=headers)
    print(f"Auth Check with Invalid Token Status Code: {auth_response.status_code}")

    try:
        print(f"Auth Check with Invalid Token Response JSON: {auth_response.json()}")
    except ValueError:
        print("Auth Check with Invalid Token Response could not be decoded as JSON.")
        print(
            f"Auth Check with Invalid Token Response Content: {auth_response.content}"
        )


def test_response_endpoint(base_url="http://localhost:8000", token=None):
    # Define the URL for the response endpoint
    response_endpoint_url = f"{base_url}/api/application/test-response/"

    # Define the JSON payload to send
    json_payload = {
        "testID": "unique_test_id",
    }

    # Define the headers, including the Authorization header with the JWT token
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    # Send a POST request to the response endpoint
    response = requests.post(response_endpoint_url, json=json_payload, headers=headers)

    print(f"Response Endpoint Status Code: {response.status_code}")

    try:
        print(f"Response Endpoint Response JSON: {response.json()}")
    except ValueError:
        print("Response Endpoint Response could not be decoded as JSON.")
        print(f"Response Endpoint Response Content: {response.content}")


class Command(BaseCommand):
    help = "Test authentication with JWT"

    def handle(self, *args, **options):
        # Test the health endpoint
        print("------------------------")
        print("TESTING HEALTH ENDPOINT")
        test_health_endpoint()

        # Test JWKS
        print("------------------------")
        print("TESTING INTERNAL JWKS ENDPOINT")
        test_jwks_endpoint(settings.AUTH_CONFIG["S2S_INTERNAL"]["link"])
        print("------------------------")
        print("TESTING EXTERNAL API JWKS ENDPOINT")
        test_jwks_endpoint(settings.AUTH_CONFIG["S2S"]["auth"]["link"])
        print("------------------------")
        print("TESTING EXTERNAL AUTH JWKS ENDPOINT")
        test_jwks_endpoint(settings.AUTH_CONFIG["C2S"]["auth"]["link"])
        print("------------------------")

        # Generate a JWT token
        print("GENERATING JWT TOKEN")
        token = generate_jwt_token()
        print("------------------------")

        # Test authentication with an invalid token
        print("TESTING AUTHENTICATION WITH INVALID TOKEN")
        simulate_api_call_with_invalid_token()
        print("------------------------")

        # Perform the simulated API call
        print("SIMULATING API CALL")
        simulate_api_call(token)
        print("------------------------")

        # Perform the simulated API call to test the response endpoint
        print("TESTING RESPONSE ENDPOINT")
        test_response_endpoint(token=token)
        print("------------------------")

        # TEST OAUTH TOKEN RETRIEVAL
        print("TESTING OAUTH TOKEN RETRIEVAL")
        token = retrieve_oauth_token(oauth_setting=settings.AUTH_CONFIG["S2S"]["sign"])
        print(f"TOKEN : {token}")
        print("------------------------")

        # TEST ACCESS TOKEN VALIDITY
        oauth_token_path = os.path.join(settings.KEYS_DIR, "oauth_token.json")
        try:
            with open(oauth_token_path, "r") as token_file:
                token_access_data = json.load(token_file)
                validity = is_access_token_valid(token_access_data)
                print(f"TOKEN VALIDITY: {validity}")
        except FileNotFoundError:
            pass

        # TEST GENERATE SIGNATURE
        print("TEST JWK SIGNATURE")
        header = generate_signature(settings.AUTH_CONFIG["C2S"]["auth"])
        print(f"JWK AUTH HEADER: {header}")

        print("TEST OAUTH SIGNATURE")
        header = generate_signature(settings.AUTH_CONFIG["S2S"]["sign"])
        print(f"OAUTH SIGN HEADER: {header}")

        print("TEST NONE SIGNATURE")
        mock_request = Mock()
        mock_request.headers = {
            "Content-Type": "application/json",
            "User-Agent": "TestClient/1.0",
        }
        header = generate_signature(settings.AUTH_CONFIG["C2S"]["sign"], mock_request)
        print(f"NONE SIGN HEADER: {header}")
        print("------------------------")
