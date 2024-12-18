from bibgrafo.grafo_lista_adjacencia import GrafoListaAdjacencia
from bibgrafo.grafo_errors import *

class MGrafo(GrafoListaAdjacencia):

    def menor_caminho_rec(self, caminhos, v_caminho, dic_pi, Vi, caminho = []):
        while True:
            if dic_pi[v_caminho] == None:
                fim = 1
            else:
                fim = len(dic_pi[v_caminho])
            for j in range(fim):
                if j > 0:
                    caminho_rec = caminho[1:]
                    caminho_rec.insert(0, dic_pi[v_caminho][j][1])
                    v_caminho_rec = dic_pi[v_caminho][j][0]
                    self.menor_caminho_rec(caminhos, v_caminho_rec, dic_pi, Vi, caminho_rec)
                    continue
                caminho.insert(0, v_caminho)
                if v_caminho == Vi:
                    break
                caminho.insert(0, dic_pi[v_caminho][j][1])
            if v_caminho == Vi:
                break
            v_caminho = self.acha_v2(caminho[0], v_caminho)
        caminhos.add(tuple(caminho))

    def dijkstra(self, Vi, Vf): 
        dic_alpha, dic_beta, dic_pi = {}, {}, {}
        for i in self.vertices:
            dic_beta[i.rotulo] = float("inf") 
            dic_alpha[i.rotulo] = 0
            dic_pi[i.rotulo] = []
        dic_beta[Vi] = 0
        dic_pi[Vi] = None
        self.dijkstra_rec(Vi,dic_beta, dic_alpha, dic_pi, Vf)
        if dic_pi[Vf] == []:
            raise ImpossivelChegarAoVertice()
        v_caminho = Vf
        caminhos = set()
        self.menor_caminho_rec(caminhos, v_caminho, dic_pi, Vi, []) 
        return caminhos

    def dijkstra_rec(self, V, dic_beta, dic_alpha, dic_pi, Vf):
        dic_alpha[V] = 1
        arestas_sobre_vertice = list(self.arestas_sobre_vertice(V))
        arestas_sobre_vertice.sort()
        for i in arestas_sobre_vertice:
            v2 = self.acha_v2(i, V)
            if dic_beta[V] + self.get_aresta(i).peso == dic_beta[v2]:
                dic_beta[v2] = dic_beta[V] + self.get_aresta(i).peso
                dic_pi[v2].append([V,i])
            elif dic_beta[V] + self.get_aresta(i).peso < dic_beta[v2]:
                dic_beta[v2] = dic_beta[V] + self.get_aresta(i).peso
                dic_pi[v2] = [[V,i]]
        minimo = float("inf")
        prox_v = None
        for i in dic_alpha:
            if dic_alpha[i] == 0:
                if dic_beta[i] < minimo:
                    prox_v = i
                    minimo = dic_beta[i]
        if prox_v == None:
            return
        if prox_v != Vf:
            self.dijkstra_rec(prox_v,dic_beta,dic_alpha, dic_pi, Vf)
             
    def acha_v2(self, i, V):
        if self.arestas[i].v1.rotulo == V:
            v2 = self.arestas[i].v2.rotulo
        else:
            v2 = self.arestas[i].v1.rotulo
        return v2
    
    def arestas_sobre_vertice(self, V):

        if self.existe_rotulo_vertice(V) == False:
            raise VerticeInvalidoError()
        arestas_v = set()
        for i in self.arestas.keys():
            x = self.arestas[i].v1
            y = self.arestas[i].v2
            if str(x) == str(V):
                arestas_v.add(i)
            if str(y) == str(V):
                arestas_v.add(i)
        return arestas_v