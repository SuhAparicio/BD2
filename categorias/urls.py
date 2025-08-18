from django.urls import path
from . import views

app_name = 'categorias'

urlpatterns = [
    path('', views.categoria_list, name='categoria_list'),
    path('<int:pk>/', views.categoria_detail, name='categoria_detail'),
    path('create/', views.categoria_create, name='categoria_create'),
    path('update/<int:pk>/', views.categoria_update, name='categoria_update'),
    path('delete/<int:pk>/', views.categoria_delete, name='categoria_delete'),
]