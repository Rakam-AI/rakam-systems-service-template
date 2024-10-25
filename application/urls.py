from django.urls import path

from application import views

#  TODO : Add a url path for each view
urlpatterns = [
    path("test-response/", views.test_response, name="generate_response"),
    path("vector_store/search/", views.search_vector_store, name="search_vector_store"),
    path("vs_manager/inject/", views.vs_manager_inject, name="vs_manager_inject"),
    path("rag/", views.rag, name="rag"),
]





