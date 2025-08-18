from django.urls import path
from . import views

app_name = 'emprestimos'

urlpatterns = [
    path('', views.emprestimo_list, name='emprestimo_list'),
    path('<int:pk>/', views.emprestimo_detail, name='emprestimo_detail'),
    path('create/', views.emprestimo_create, name='emprestimo_create'),
    path('update/<int:pk>/', views.emprestimo_update, name='emprestimo_update'),
    path('delete/<int:pk>/', views.emprestimo_delete, name='emprestimo_delete'),
]