from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
import json, os, importlib
from gerador_de_menores_caminhos_com_docker.meu_grafo_lista_adj import MGrafo as mg

PATH = os.getcwd() + "\\app\\djkistra_cliente.py"

def index(request):
    return render(request, "app/index.html") 


def gera_codigo_cliente(request):
    if os.path.exists('app/djkistra_cliente.py'):
        os.remove(PATH)
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
    else:
        global lista_nomes
        lista_nomes = []
        try:
            texto = request.POST.get("grafo")
            dic_grafo = json.loads(texto)
            lista_grafos = []
            for grafo in dic_grafo:
                lista_nomes.append(grafo)
                cliente = dc.MeuGrafo()
                meu = mg()
                for vertice in dic_grafo[grafo]["vertices"]:
                    cliente.adiciona_vertice(vertice)
                    meu.adiciona_vertice(vertice)
                for aresta in dic_grafo[grafo]["arestas"]:
                    try:
                        peso = dic_grafo[grafo]["arestas"][aresta][2]
                    except:
                        peso = 1
                    cliente.adiciona_aresta(aresta, dic_grafo[grafo]["arestas"][aresta][0], dic_grafo[grafo]["arestas"][aresta][1], peso)
                    meu.adiciona_aresta(aresta, dic_grafo[grafo]["arestas"][aresta][0], dic_grafo[grafo]["arestas"][aresta][1], peso)
                globals()[grafo] = [cliente, meu]
                lista_grafos.append([globals()[grafo], dic_grafo[grafo]["vertice_inicial"], dic_grafo[grafo]["vertice_final"]])

            global lista_grafos_global
            lista_grafos_global = lista_grafos
        except json.JSONDecodeError as error:
            mensagem =  'Erro no envio do grafo: ' + str(error)
        except Exception as error:
            mensagem = error
    
    messages.error(request, mensagem)
    return redirect('./')

def compara(request):
    mensagem = None
    resposta = {}
    try:
        index = 0
        for grafo in lista_grafos_global:
            caminhos = grafo[0][1].dijkstra(grafo[1],grafo[2])
            print(grafo[0][1])
            caminho_cliente = (grafo[0][0].meu_dijkstra(grafo[1],grafo[2]))
            if caminho_cliente not in caminhos:
                resposta[lista_nomes[index]] = {'caminho_cliente' :caminho_cliente, 'caminhos': caminhos, 'situacao': 'erro'}
            else:
                resposta[lista_nomes[index]] = {'caminho_cliente' :caminho_cliente, 'caminhos': caminhos, 'situacao': 'ok'}
            index+=1
    except NameError as error:
        mensagem = 'Envie um grafo' 
    except Exception as error:
        mensagem = error
    if mensagem != None:
        messages.error(request, mensagem)
    context = {
        'respostas' : resposta
    }
    return render(request, "app/index.html", context)