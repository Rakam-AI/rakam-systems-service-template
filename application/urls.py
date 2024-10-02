from django.urls import path

from application import views

urlpatterns = [
    path("test-response/", views.test_response, name="generate_response"),
    # path("dummy-endpoint/", views.dummy_endpoint, name="dummy_endpoint"),
]
