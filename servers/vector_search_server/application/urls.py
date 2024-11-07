from django.urls import path
from . import views


urlpatterns = [
    path('vectorstore/search/', views.search, name='search'),
    path('vectorstore/get_nodes/', views.get_nodes, name='get_nodes'),
    path('s3filemanager/upload_folders/', views.upload_folders, name='upload_folders'),
    path('s3filemanager/download_files/', views.download_files, name='download_files'),
    path('s3filemanager/list_files/', views.list_files, name='list_files'),
    path('s3filemanager/update_prefix/', views.update_prefix, name='update_prefix'),
    path('s3filemanager/empty_prefix/', views.empty_prefix, name='empty_prefix'),
]
