from django.urls import path
from . import views

app_name = 'livros'

urlpatterns = [
    path('', views.livro_list, name='livro_list'),
    path('<int:pk>/', views.livro_detail, name='livro_detail'),
    path('create/', views.livro_create, name='livro_create'),
    path('update/<int:pk>/', views.livro_update, name='livro_update'),
    path('delete/<int:pk>/', views.livro_delete, name='livro_delete'),
]