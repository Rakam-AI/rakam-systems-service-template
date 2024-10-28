from django.urls import path

from application import views

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


urlpatterns = [
    path("dataprocessor/", views.dataprocessor, name="dataprocessor"),
    path("vector_store/search/", views.search_vector_store, name="search_vector_store"),
    path("vs_manager/inject/", views.vs_manager_inject, name="vs_manager_inject"),
    path("rag/", views.rag, name="rag"),
    
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]





