from rest_framework.decorators import api_view
from rest_framework.decorators import authentication_classes
from rest_framework.response import Response

from api_auth.authentication import CustomJWTAuthentication


@api_view(["POST"])
@authentication_classes([CustomJWTAuthentication])
def test_response(request):
    """
    Endpoint that takes a user message as input and returns a response in JSON format.
    """
    # Placeholder response structure
    base_response = {
        "text": "Hey, test test was successful !",
    }

    return Response(base_response, status=200)
