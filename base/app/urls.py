from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('projects/', views.list_projects),
    path('clients/<int:id>/projects', views.create_project),
    path('clients/<int:id>', views.get_put_delete_client),
    path('clients/', views.get_post_clients),

]
