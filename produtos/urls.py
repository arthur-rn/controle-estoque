from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name="home"),
    path('criar/', views.criar_produto, name='criar_produto'),
    path('listar/', views.listar_produtos, name='listar_produtos'),
    path('editar/<int:id>', views.editar_produto, name='editar_produto'),
    path('excluir/<int:id>', views.excluir_produto, name='excluir_produto'),
]