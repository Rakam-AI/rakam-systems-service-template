from django.urls import path
from . import views


urlpatterns = [
    path('llmmanager/call_llm/', views.call_llm, name='call_llm'),
    path('llmmanager/call_llm_stream/', views.call_llm_stream, name='call_llm_stream'),
    path('llmmanager/call_llm_output_json/', views.call_llm_output_json, name='call_llm_output_json'),
    path('raggenerator/rag_generate/', views.rag_generate, name='rag_generate'),
    path('raggenerator/split_query/', views.split_query, name='split_query'),
    path('raggenerator/rag_generate_split_query/', views.rag_generate_split_query, name='rag_generate_split_query'),
    path('s3filemanager/upload_folders/', views.upload_folders, name='upload_folders'),
    path('s3filemanager/download_files/', views.download_files, name='download_files'),
    path('s3filemanager/list_files/', views.list_files, name='list_files'),
    path('s3filemanager/update_prefix/', views.update_prefix, name='update_prefix'),
    path('s3filemanager/empty_prefix/', views.empty_prefix, name='empty_prefix'),
]
