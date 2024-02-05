from django.shortcuts import render, HttpResponse, redirect
import json
import unittest
from gerador_de_menores_caminhos_com_docker.meu_grafo_lista_adj import MGrafo as mg

def index(request, erro = ''):
    context = {'erro' : erro }
    print(context['erro'])
    return render(request, "app/index.html", context) 


def gera_codigo_cliente(request):
    texto = request.POST.get("codigo")
    with open("./app/djkistra_cliente.py", "w") as arquivo:
        arquivo.write(texto)
    try:
        import app.djkistra_cliente as dc
        erro = 'Código enviado com sucesso!'
    except:
        erro = 'Existe alguma irregularidade no seu código'
     
    return redirect('./', erro)
    

def gera_grafo(request):
    import app.djkistra_cliente as dc
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

    return redirect('./')

def compara(request):
    for grafo in lista_grafos_global:
        caminhos = grafo[0][1].dijkstra(grafo[1],grafo[2])
        caminho_cliente = (grafo[0][0].meu_dijkstra(grafo[1],grafo[2]))
    for caminho in caminhos:
        if caminho_cliente != caminho:
            return HttpResponse(f'{caminho_cliente} não está entre as soluções possíveis: {caminho}')
    return HttpResponse("tudo ok")
  