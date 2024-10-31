from django.urls import path

from application import views

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


urlpatterns = [
    path("internal/process_from_directory/", views.process_from_directory, name="process_from_directory"),
    path("external/vector_store/search/", views.search_vector_store, name="search_vector_store"),
    path("internal/vector_store/get_nodes/", views.get_nodes, name="get_nodes"),
    path("external/vs_manager/build_from_directory/", views.vs_manager_build, name="vs_manager_build"),
    path("external/vs_manager/add_from_directory/", views.vs_manager_add_files, name="vs_manager_add"),
    path("external/rag_generate/", views.rag_generation, name="rag_generation"),
    
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]





