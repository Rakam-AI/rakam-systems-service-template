from django.urls import path

from application import views

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


urlpatterns = [
    path("external/data_processor/process_from_directory/", views.process_from_directory, name="process_from_directory"),
    path("external/data_processor/process_from_file/", views.process_from_file, name="process_from_file"),

    path("external/vector_store/search/", views.search_vector_store, name="search_vector_store"),
    path("internal/vector_store/get_nodes/", views.get_nodes, name="get_nodes"),

    path("external/vs_manager/build_from_directory/", views.vs_manager_build_from_directory, name="vs_manager_build_from_directory"),
    path("external/vs_manager/build_from_file/", views.vs_manager_build_from_file, name="vs_manager_build_from_file"),
    path("external/vs_manager/add_from_directory/", views.vs_manager_add_from_directory, name="vs_manager_add_from_directory"),
    path("external/vs_manager/add_from_file/", views.vs_manager_add_from_file, name="vs_manager_add_from_file"),

    path("external/rag_generator/rag_generate/", views.rag_generation, name="rag_generation"),
    path("internal/rag_generator/split_query/", views.rag_generation_split_query, name="split_query"),
    path("external/rag_generator/split_query_generate/", views.rag_generation_split_query_response, name="rag_generation_split_query"),

    path("external/s3_manager/upload_folders/", views.upload_folders, name="upload_folders"),
    path("external/s3_manager/download_files/", views.download_files, name="download_files"),
    path("external/s3_manager/list_files/", views.list_files, name="list_files"),
    path("external/s3_manager/update_prefix/", views.update_prefix, name="update_prefix"),
    path("external/s3_manager/empty_prefix/", views.empty_s3, name="empty_prefix"),

    path("external/llm_connector/call_llm/", views.call_llm, name="call_llm"),
    path("external/llm_connector/call_llm_stream/", views.call_llm_stream, name="call_llm_stream"),
    path("external/llm_connector/call_llm_output_json/", views.call_llm_output_json, name="call_llm_output_json"),

    path("external/sqldb/execute_query/", views.SQLDBexecute_query, name="SQLDB_execute_query"),
    path("external/sqldb/insert_data/", views.SQLDBinsert_data, name="SQLDB_insert_data"),
    path("external/sqldb/update_data/", views.SQLDBupdate_data, name="SQLDB_update_data"),
    path("external/sqldb/delete_data/", views.SQLDBdelete_data, name="SQLDB_delete_data"),
    path("external/sqldb/create_table/", views.SQLDBcreate_table, name="SQLDB_create_table"),
    path("external/sqldb/get_tables/", views.SQLDBshow_tables, name="SQLDB_get_tables"),
    
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]





