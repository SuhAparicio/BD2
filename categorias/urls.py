from django.urls import path
from . import views

app_name = 'categorias'

urlpatterns = [
    path('', views.categoria_list, name='categoria_list'),
    path('<int:id_categoria>/', views.categoria_detail, name='categoria_detail'),
    path('create/', views.categoria_create, name='categoria_create'),
    path('update/<int:id_categoria>/', views.categoria_update, name='categoria_update'),
    path('delete/<int:id_categoria>/', views.categoria_delete, name='categoria_delete'),
]