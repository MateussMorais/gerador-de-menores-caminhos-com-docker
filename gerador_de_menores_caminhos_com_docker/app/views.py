from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
import json, os, importlib
from app.meu_grafo_lista_adj import MGrafo as mg

def index(request):
    return render(request, "app/index.html") 


# Função que gera o código digitado pelo cliente
def gera_codigo_cliente(request):

    # Verifica se já existe algum código enviado pelo cliente. Caso sim, o apaga.
    if os.path.exists('app/djkistra_cliente.py'):
        os.remove(os.getcwd() + "/app/djkistra_cliente.py")
    
    arquivo = request.FILES.get("codigo") # Recebe o código enviado pelo usuário pela requisição
    path = os.path.join(settings.BASE_DIR, "app") # Declara o caminho que deve ser criado o arquivo 
    FileSystemStorage(location=path).save("djkistra_cliente.py", arquivo) # Cria o arquivo com o código digitado pelo usuário
    return redirect('./') # Retorna para a rota base
    
# Função que gera o grafo de listas de adjacêcias digitado pelo cliente
def gera_grafo(request):
    mensagem = ''

    # Tenta importar o código do cliente e recarregar a importação para não ser usado o código de importações antigas
    try:
        import app.djkistra_cliente as dc
        importlib.reload(dc)
    except Exception as error: # Caso não seja possível fazer a importação, dispara um erro de que o código não foi enviado
        mensagem = error
    else: 
        # Declaração da lista global que guardará os nomes dos grafos enviados pelo cliente
        global lista_nomes
        lista_nomes = []
        try:
            # Coleta os grafos enviados e os coloca em um dicionário
            texto = request.POST.get("grafo") 
            dic_grafos = json.loads(texto)
            
            lista_grafos = [] # lista que guardará os objetos dos grafos enviados pelo cliente
            
            for nome_grafo in dic_grafos:
                lista_nomes.append(nome_grafo) # adiciona o nome do grafo à lista de nomes
                
                # Instancia os grafos da classe criada pelo cliente e da classe criada por mim 
                cliente_grafo_obj = dc.MeuGrafo()
                m_grafo_obj = mg()

                # Cria os vértices nos dois grafos
                for vertice in dic_grafos[nome_grafo]["vertices"]:
                    cliente_grafo_obj.adiciona_vertice(vertice)
                    m_grafo_obj.adiciona_vertice(vertice)
                
                #Cria as arestas nos dois grafos
                for rotulo_aresta in dic_grafos[nome_grafo]["arestas"]:
                    aresta = dic_grafos[nome_grafo]["arestas"][rotulo_aresta]
                    vertice_inicial = dic_grafos[nome_grafo]["arestas"][rotulo_aresta][0]
                    vertice_final = dic_grafos[nome_grafo]["arestas"][rotulo_aresta][1]
                    try:
                        peso = aresta[2]
                    except:
                        peso = 1
                    cliente_grafo_obj.adiciona_aresta(rotulo_aresta, vertice_inicial, vertice_final, peso)
                    m_grafo_obj.adiciona_aresta(rotulo_aresta, vertice_inicial, vertice_final, peso)
                
                # Cria uma lista com o nome do grafo enviado pelo cliente, contendo dois objetos da classe MGrafo(implementada por mim) e MeuGrafo(implementada pelo cliente)
                globals()[nome_grafo] = [cliente_grafo_obj, m_grafo_obj]

                # Adiciona na matriz com os grafos uma lista com nome, vértice inicial e final que o usuário quer que seja executado o algoritmo de Dijkstra
                lista_grafos.append([globals()[nome_grafo], dic_grafos[nome_grafo]["vertice_inicial"], dic_grafos[nome_grafo]["vertice_final"]])

            # Cria uma lista global e insere a lista_grafos nela
            global lista_grafos_global
            lista_grafos_global = lista_grafos
        
        # Trata os erros
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
            # Separa da lista os objetos e os vértices iniciais e finais para cada par de objeto
            m_grafo_obj = grafo[0][1]
            cliente_grafo_obj = grafo[0][0]
            vertice_inicial = grafo[1]
            vertice_final = grafo[2]

        
            caminhos_possiveis = m_grafo_obj.dijkstra(vertice_inicial,vertice_final) # Coleta todos os caminhos mínimos possíveis
            caminho_cliente = cliente_grafo_obj.meu_dijkstra(vertice_inicial,vertice_final) # Executa o algoritmo de dijkstra do cliente 

            # Verifica se a resposta obtida pelo cliente está nas respostas possíveis
            if caminho_cliente not in caminhos_possiveis:
                resposta[lista_nomes[index]] = {
                    'caminho_cliente' :caminho_cliente, 
                    'caminhos': caminhos_possiveis, 
                    'situacao': 'erro'
                    } 
            else:
                resposta[lista_nomes[index]] = {
                    'caminho_cliente' :caminho_cliente, 
                    'caminhos': caminhos_possiveis, 
                    'situacao': 'ok'
                    }
            index+=1

    # Trata os erros
    except NameError as error:
        mensagem = 'Envie um grafo' 
    except Exception as error:
        mensagem = error
    if mensagem != None:
        messages.error(request, mensagem)
    context = {
        'respostas' : resposta
    }
    # Renderiza a página index.html, com as informações que devem ser apresentadas.
    return render(request, "app/index.html", context)