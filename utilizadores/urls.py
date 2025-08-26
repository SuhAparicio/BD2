from django.urls import path
from . import views

app_name = 'utilizadores'

urlpatterns = [
    path('', views.utilizador_list, name='utilizador_list'),
    path('create/', views.utilizador_create, name='utilizador_create'),
    path('<str:pk>/', views.utilizador_detail, name='utilizador_detail'),
    path('update/<str:pk>/', views.utilizador_update, name='utilizador_update'),
    path('delete/<str:pk>/', views.utilizador_delete, name='utilizador_delete'),
]