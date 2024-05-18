from django.shortcuts import render, HttpResponse, redirect
import json
import unittest
from gerador_de_menores_caminhos_com_docker.meu_grafo_lista_adj import MGrafo as mg

def index(request, foo = ''):
    context = {'erro' : foo }
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
     
    return redirect('./', foo=erro)
    

def gera_grafo(request):
    try:
        import app.djkistra_cliente as dc
    except:
        return render(request, "app/index.html", {'erro' : 'Não foi possível gerar o grafo por um problema no código enviado'})
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
    except:
        return render(request, "app/index.html", {'erro' : 'Não foi possível criar o grafo por um problema no grafo enviado.'})

    return redirect('./')

def compara(request):
    try:
        for grafo in lista_grafos_global:
            caminhos = grafo[0][1].dijkstra(grafo[1],grafo[2])
            caminho_cliente = (grafo[0][0].meu_dijkstra(grafo[1],grafo[2]))
        for caminho in caminhos:
            if caminho_cliente != caminho:
                return HttpResponse(f'{caminho_cliente} não está entre as soluções possíveis: {caminho}')
    except:
        return render(request, "app/index.html", {'erro' : 'Inconsistência no código ou grafo enviado'})
    return HttpResponse("tudo ok")
  