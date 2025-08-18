from django.urls import path
from . import views

app_name = 'utilizadores'

urlpatterns = [
    path('', views.utilizador_list, name='utilizador_list'),
    path('<int:pk>/', views.utilizador_detail, name='utilizador_detail'),
    path('create/', views.utilizador_create, name='utilizador_create'),
    path('update/<int:pk>/', views.utilizador_update, name='utilizador_update'),
    path('delete/<int:pk>/', views.utilizador_delete, name='utilizador_delete'),
]