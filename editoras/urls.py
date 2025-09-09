from django.urls import path
from . import views

app_name = 'editoras'

urlpatterns = [
    path('', views.editora_list, name='editora_list'),
    path('nova/', views.editora_create, name='editora_create'),
    path('<int:id_editora>/', views.editora_detail, name='editora_detail'),
    path('<int:id_editora>/editar/', views.editora_update, name='editora_update'),
    path('<int:id_editora>/eliminar/', views.editora_delete, name='editora_delete'),
]