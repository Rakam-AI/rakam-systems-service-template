from django.urls import path
from . import views


urlpatterns = [
    path('dataprocessor/process_from_directory/', views.process_from_directory, name='process_from_directory'),
    path('dataprocessor/process_from_file/', views.process_from_file, name='process_from_file'),
    path('vsmanager/build_from_directory/', views.build_from_directory, name='build_from_directory'),
    path('vsmanager/build_from_file/', views.build_from_file, name='build_from_file'),
    path('vsmanager/add_from_directory/', views.add_from_directory, name='add_from_directory'),
    path('vsmanager/add_from_file/', views.add_from_file, name='add_from_file'),
    path('s3filemanager/upload_folders/', views.upload_folders, name='upload_folders'),
    path('s3filemanager/download_files/', views.download_files, name='download_files'),
    path('s3filemanager/list_files/', views.list_files, name='list_files'),
    path('s3filemanager/update_prefix/', views.update_prefix, name='update_prefix'),
    path('s3filemanager/empty_prefix/', views.empty_prefix, name='empty_prefix'),
]
