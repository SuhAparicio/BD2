from django.urls import path
from . import views

app_name = 'requisicoes'

urlpatterns = [
    path('', views.requisicao_list, name='requisicao_list'),
    path('<int:id_requisicao>/', views.requisicao_detail, name='requisicao_detail'),
    path('create/', views.requisicao_create, name='requisicao_create'),
    path('update/<int:id_requisicao>/', views.requisicao_update, name='requisicao_update'),
    path('delete/<int:id_requisicao>/', views.requisicao_delete, name='requisicao_delete'),
    path('devolver/<int:id_requisicao>/', views.requisicao_devolver, name='requisicao_devolver'),
]