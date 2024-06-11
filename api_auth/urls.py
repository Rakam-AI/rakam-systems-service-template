from django.urls import path

from api_auth import views

urlpatterns = [
    path(".well-known/jwks.json", views.jwks, name="jwks"),
    path("auth-check/", views.auth_check, name="auth_check"),
]
