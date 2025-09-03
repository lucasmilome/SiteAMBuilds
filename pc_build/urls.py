from django.urls import path
from . import views

urlpatterns = [
    path('montar_pc', views.pc_build, name='pc_build'),
    path('montar_pc_pecas', views.pecas, name='pc_build_pecas'),
    path('salvar_montagem', views.salvar_montagem , name='salvar_montagem'),
    path('meus_pcs', views.meus_pcs, name='meus_pcs'),
    path('meus_pcs/<int:montagem_id>/', views.montagem_detalhes, name='montagem_detalhes'),
]