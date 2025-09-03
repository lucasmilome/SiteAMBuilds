from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('categorias/<str:tipoDeProduto>/<int:pk>/', views.detail, name='detail'),
    path('categorias/<str:tipoDeProduto>/', views.category, name='category'),
]