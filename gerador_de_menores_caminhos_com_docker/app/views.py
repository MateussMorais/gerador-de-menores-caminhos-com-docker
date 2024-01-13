from django.shortcuts import render, HttpResponse
import os
import json
import gerador_de_menores_caminhos_com_docker.meu_grafo_lista_adj as mg
import app.djkistra_cliente as dc

def index(request):
    context = {

    }
    return render(request, "app/index.html", context) 

def gera_menores_caminhos_cliente(request):
    codigo = request.POST.get("codigo")
    grafo = request.POST.get("grafo")
    gera_codigo_cliente(codigo)
    lista_grafos = gera_grafo(grafo)  
    for grafo in lista_grafos:
        caminhos = grafo.dijkstra_cliente("A","E")
    return HttpResponse(caminhos)


def gera_codigo_cliente(texto):
    if os.path.isfile("./app/djkistra_cliente.py"):
        os.remove("./app/djkistra_cliente.py")
    arquivo = open("./app/djkistra_cliente.py", "x")
    arquivo.write(texto)
    arquivo.close()
    return

def gera_grafo(texto):
    dic_grafo = json.loads(texto)
    lista_grafos = []
    for grafo in dic_grafo:
        globals()[grafo] = dc.MeuGrafoCliente()
        for vertice in dic_grafo[grafo]["vertices"]:
            globals()[grafo].adiciona_vertice(vertice)
        for aresta in dic_grafo[grafo]["arestas"]:
            try:
                peso = aresta[2]
            except:
                peso = 1
            globals()[grafo].adiciona_aresta(aresta, dic_grafo[grafo]["arestas"][aresta][0], dic_grafo[grafo]["arestas"][aresta][1], peso)
        lista_grafos.append(globals()[grafo])


    return lista_grafos   