from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from .forms import CategoriaForm
from .models import Categoria

def is_bibliotecario_ou_admin(user):
    return (
        user.is_superuser or
        user.groups.filter(name='bibliotecario').exists() or
        user.groups.filter(name='admin').exists()
    )

@login_required
def categoria_list(request):
    if not is_bibliotecario_ou_admin(request.user):
        return render(request, '404.html', status=404)
    categorias = Categoria.objects.all()
    return render(request, 'categorias/list.html', {'categorias': categorias})

@login_required
def categoria_detail(request, pk):
    if not is_bibliotecario_ou_admin(request.user):
        return render(request, '404.html', status=404)
    categoria = get_object_or_404(Categoria, pk=pk)
    return render(request, 'categorias/detail.html', {'categoria': categoria})

@login_required
def categoria_create(request):
    if not is_bibliotecario_ou_admin(request.user):
        return render(request, '404.html', status=404)
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('categorias:categoria_list')
    else:
        form = CategoriaForm()
    return render(request, 'categorias/create.html', {'form': form})

@login_required
def categoria_update(request, pk):
    if not is_bibliotecario_ou_admin(request.user):
        return render(request, '404.html', status=404)
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            return redirect('categorias:categoria_list')
    else:
        form = CategoriaForm(instance=categoria)
    return render(request, 'categorias/update.html', {'form': form})

@login_required
def categoria_delete(request, pk):
    if not is_bibliotecario_ou_admin(request.user):
        return render(request, '404.html', status=404)
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        categoria.delete()
        return redirect('categorias:categoria_list')
    return render(request, 'categorias/delete.html', {'categoria': categoria})