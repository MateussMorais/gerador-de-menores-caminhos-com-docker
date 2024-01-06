from django.shortcuts import render, HttpResponse
import os

def index(request):
    context = {

    }
    return render(request, "app/index.html", context) 

def gera_menores_caminhos_usuario(request):
    codigo = request.POST.get("codigo")
    if os.path.isfile("./gerador_de_menores_caminhos_com_docker/app/arquivo.py"):
        os.remove("./gerador_de_menores_caminhos_com_docker/app/arquivo.py")
    arquivo = open("./gerador_de_menores_caminhos_com_docker/app/arquivo.py", "x")
    arquivo.write(codigo)
    arquivo.close()
    arquivo = open("./gerador_de_menores_caminhos_com_docker/app/arquivo.py", "r")
    programa = (arquivo.read())
    exec(programa)
    arquivo.close()
    return HttpResponse('ok')
