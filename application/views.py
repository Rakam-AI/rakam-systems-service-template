from rest_framework.decorators import api_view
from rest_framework.decorators import authentication_classes
from rest_framework.response import Response
from application.engine import components

#  TODO : Add a view for each call_ or non _ functions in the 4 components

@api_view(["POST", "GET"])
def test_response(request):
    """
    Endpoint that takes a user message as input and returns a response in JSON format.
    """
    # Placeholder response structure
    base_response = {
        "text": "Hey, this a test for response!",
    }
    # base_response = components.VS.call_main()

    return Response(base_response, status=200)

@api_view(["POST", "GET"])
def search_vector_store(request):
    """
    Endpoint that takes a user message as input and returns a response in JSON format.
    """
    # Placeholder response structure
    base_response = {
        "query": "Hey, test test was successful !",
    }
    base_response = components.VS.test()
    return Response(base_response, status=200)

@api_view(["POST", "GET"])
def vs_manager_inject(request):
    """
    Endpoint that takes a user message as input and returns a response in JSON format.
    """
    # Placeholder response structure
    # base_response = {
    #     "query": "Hey, test for vs_manager!",
    # }
    base_response = components.VSManager.test()
    return Response(base_response, status=200)

@api_view(["POST", "GET"])
def rag(request):
    """
    Endpoint that takes a user message as input and returns a response in JSON format.
    """
    # Placeholder response structure
    # base_response = {
    #     "query": "Hey, test for vs_manager!",
    # }
    base_response = components.ragGen.test()
    return Response(base_response, status=200)


