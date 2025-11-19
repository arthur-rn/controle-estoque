from django.shortcuts import get_object_or_404, render, redirect
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
            return redirect('listar_produtos')

    else:
        form = ProdutoForm()
    
    return render(request, 'criar_produto.html', {'form': form})
    
def editar_produto(request, id):
    produto = Produto.objects.get(id=id)
    if request.method == "POST":
        form = ProdutoForm(request.POST, instance=produto)
        if form.is_valid():
            form.save()
            return redirect('listar_produtos')
    else:
        form = ProdutoForm(instance=produto)
    return render(request, "editar_produto.html", {"form": form, "edit": True})

def excluir_produto(request, id):
    produto = get_object_or_404(Produto, id=id)
    if request.method == "POST":
        produto.delete()
    return redirect('listar_produtos')