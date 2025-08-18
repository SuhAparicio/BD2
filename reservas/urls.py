from django.urls import path
from . import views

app_name = 'reservas'

urlpatterns = [
    path('', views.reserva_list, name='reserva_list'),
    path('create/', views.reserva_create, name='reserva_create'),
    path('<int:pk>/', views.reserva_detail, name='reserva_detail'),
    path('update/<int:pk>/', views.reserva_update, name='reserva_update'),
    path('delete/<int:pk>/', views.reserva_delete, name='reserva_delete'),
]