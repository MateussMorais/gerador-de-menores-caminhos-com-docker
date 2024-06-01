from django.shortcuts import render, HttpResponse, redirect
from django.urls import reverse
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
import json, os, importlib
from gerador_de_menores_caminhos_com_docker.meu_grafo_lista_adj import MGrafo as mg

PATH = os.getcwd() + "\\app\\djkistra_cliente.py"

def index(request, erro = ''):
    context = {'erro' : erro}
    return render(request, "app/index.html", context) 


def gera_codigo_cliente(request):
    arquivo = request.FILES.get("codigo")
    path = os.path.join(settings.BASE_DIR, "app")
    FileSystemStorage(location=path).save("djkistra_cliente.py", arquivo)
    return redirect('./')
    

def gera_grafo(request):
    mensagem = ''
    try:
        import app.djkistra_cliente as dc
        importlib.reload(dc)
    except Exception as error:
        mensagem = error
        os.remove(PATH)
    else:
        try:
            texto = request.POST.get("grafo")
            dic_grafo = json.loads(texto)
            lista_grafos = []
            for grafo in dic_grafo:
                cliente = dc.MeuGrafo()
                meu = mg()
                for vertice in dic_grafo[grafo]["vertices"]:
                    cliente.adiciona_vertice(vertice)
                    meu.adiciona_vertice(vertice)
                for aresta in dic_grafo[grafo]["arestas"]:
                    try:
                        peso = aresta[2]
                    except:
                        peso = 1
                    cliente.adiciona_aresta(aresta, dic_grafo[grafo]["arestas"][aresta][0], dic_grafo[grafo]["arestas"][aresta][1], peso)
                    meu.adiciona_aresta(aresta, dic_grafo[grafo]["arestas"][aresta][0], dic_grafo[grafo]["arestas"][aresta][1], peso)
                globals()[grafo] = [cliente, meu]
                lista_grafos.append([globals()[grafo], dic_grafo[grafo]["vertice_inicial"], dic_grafo[grafo]["vertice_final"]])

            global lista_grafos_global
            lista_grafos_global = lista_grafos
        except Exception as error:
            mensagem = error
            os.remove(PATH)
    
    messages.error(request, mensagem)
    return redirect('./')

def compara(request):
    mensagem = 'tudo ok'
    try:
        for grafo in lista_grafos_global:
            caminhos = grafo[0][1].dijkstra(grafo[1],grafo[2])
            caminho_cliente = (grafo[0][0].meu_dijkstra(grafo[1],grafo[2]))
        for caminho in caminhos:
            if caminho_cliente != caminho:
                mensagem = (f'{caminho_cliente} não está entre as soluções possíveis: {caminhos}')
    except NameError as error:
        mensagem = 'Envie um grafo'
    except Exception as error:
        mensagem = error
    os.remove(PATH)
    print(mensagem)
    messages.error(request, mensagem)
    return redirect('./')