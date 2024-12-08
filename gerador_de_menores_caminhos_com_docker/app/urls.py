from django.urls import path
from . import views

urlpatterns = [
    path("", views.index),
    path("gera_codigo_cliente", views.gera_codigo_cliente),
    path("gera_grafo", views.gera_grafo),
    path("compara", views.compara)
]