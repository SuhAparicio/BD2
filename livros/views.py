from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from .forms import LivroForm
from .models import Livro

def is_bibliotecario_ou_admin(user):
    return (
        user.is_superuser or
        user.groups.filter(name='bibliotecario').exists() or
        user.groups.filter(name='admin').exists()
    )

@login_required
def livro_list(request):
    livros = Livro.objects.all()
    is_membro = request.user.groups.filter(name='membro').exists()
    return render(request, 'livros/list.html', {'livros': livros, 'is_membro': is_membro})

@login_required
def livro_detail(request, pk):
    livro = get_object_or_404(Livro, pk=pk)
    return render(request, 'livros/detail.html', {'livro': livro})

@login_required
def livro_create(request):
    if not is_bibliotecario_ou_admin(request.user):
        return render(request, '404.html', status=404)
    if request.method == 'POST':
        form = LivroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('livros:livro_list')
    else:
        form = LivroForm()
    return render(request, 'livros/create.html', {'form': form})

@login_required
def livro_update(request, pk):
    if not is_bibliotecario_ou_admin(request.user):
        return render(request, '404.html', status=404)
    livro = get_object_or_404(Livro, pk=pk)
    if request.method == 'POST':
        form = LivroForm(request.POST, instance=livro)
        if form.is_valid():
            form.save()
            return redirect('livros:livro_list')
    else:
        form = LivroForm(instance=livro)
    return render(request, 'livros/update.html', {'form': form})

@login_required
def livro_delete(request, pk):
    if not is_bibliotecario_ou_admin(request.user):
        return render(request, '404.html', status=404)
    livro = get_object_or_404(Livro, pk=pk)
    if request.method == 'POST':
        livro.delete()
        return redirect('livros:livro_list')
    return render(request, 'livros/delete.html', {'livro': livro})