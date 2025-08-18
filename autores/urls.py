from django.urls import path
from . import views

app_name = 'autores'

urlpatterns = [
    path('', views.autor_list, name='autor_list'),
    path('<int:pk>/', views.autor_detail, name='autor_detail'),
    path('create/', views.autor_create, name='autor_create'),
    path('update/<int:pk>/', views.autor_update, name='autor_update'),
    path('delete/<int:pk>/', views.autor_delete, name='autor_delete'),
]