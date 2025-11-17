from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Produto
from .forms import ProdutoForm

# Create your views here.
def home_view(request):
    return render(request, "home.html")

def listar_produtos(request):
    produtos = Produto.objects.all()
    return render(request, 'listar_produtos.html', {'produtos': produtos})

def criar_produto(request):
    
    if request.method == "POST":
        form = ProdutoForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('home')

    else:
        form = ProdutoForm()
    
    return render(request, 'criar_produto.html', {'form': form})
    
def editar_produto(request):
    HttpResponse('Produto Editado')