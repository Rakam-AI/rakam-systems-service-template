import json

from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.decorators import authentication_classes
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response



@api_view(["GET"])  # Specify allowed methods, e.g., GET
def health_check(request):
    """
    Health check endpoint.
    """
    return Response({"status": "healthy"}, status=200)