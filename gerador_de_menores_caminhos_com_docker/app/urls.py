from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("gera_menores_caminhos_cliente", views.gera_menores_caminhos_cliente, name="gera_menores_caminhos_cliente")
]