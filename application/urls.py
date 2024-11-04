from django.urls import path

from application import views

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


urlpatterns = [
    path("external/process_from_directory/", views.process_from_directory, name="process_from_directory"),
    path("external/process_from_file/", views.process_from_file, name="process_from_file"),

    path("external/vector_store/search/", views.search_vector_store, name="search_vector_store"),
    path("internal/vector_store/get_nodes/", views.get_nodes, name="get_nodes"),

    path("external/vs_manager/build_from_directory/", views.vs_manager_build_from_directory, name="vs_manager_build_from_directory"),
    path("external/vs_manager/build_from_file/", views.vs_manager_build_from_file, name="vs_manager_build_from_file"),
    path("external/vs_manager/add_from_directory/", views.vs_manager_add_from_directory, name="vs_manager_add_from_directory"),
    path("external/vs_manager/add_from_file/", views.vs_manager_add_from_file, name="vs_manager_add_from_file"),

    path("external/rag_generate/", views.rag_generation, name="rag_generation"),
    path("internal/split_query/", views.rag_generation_split_query, name="split_query"),
    path("external/rag_generate_splitQuery/", views.rag_generation_split_query_response, name="rag_generation_split_query"),
    
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]





