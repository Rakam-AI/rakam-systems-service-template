import json

from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.decorators import authentication_classes
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from api_auth.authentication import CustomJWTAuthentication


@api_view(["GET"])  # Specify allowed methods, e.g., GET
def health_check(request):
    """
    Health check endpoint.
    """
    return Response({"status": "healthy"}, status=200)


@api_view(["GET"])
@authentication_classes([CustomJWTAuthentication])
def auth_check(request):
    """
    Authentication test endpoint.
    """
    print(" in AUTH CHECK View ")
    return Response({"status": "success"}, status=200)


@api_view(["GET"])
@permission_classes([AllowAny])  # This view can be accessed without authentication
def jwks(request):
    """
    JWKS endpoint.
    """
    # Build the path to the jwks.json file
    jwks_file_path = settings.JWKS_FILE_PATH

    # Read the JWKS data from the file
    with open(jwks_file_path, "r", encoding="utf-8") as file:
        jwks_data = json.load(
            file
        )  # Use json.load to parse the JSON file directly into a Python dict

    # Set the Content-Type header of the response to application/json
    response = Response(jwks_data, content_type="application/json")
    print("JWKS RESPONSE: ", response)

    return response
