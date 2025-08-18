from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import LivroForm
from .models import Livro

@login_required
def livro_list(request):
    livros = Livro.objects.all()
    return render(request, 'livros/list.html', {'livros': livros})

@login_required
def livro_detail(request, pk):
    livro = get_object_or_404(Livro, pk=pk)
    return render(request, 'livros/detail.html', {'livro': livro})

@login_required
def livro_create(request):
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
    livro = get_object_or_404(Livro, pk=pk)
    if request.method == 'POST':
        livro.delete()
        return redirect('livros:livro_list')
    return render(request, 'livros/delete.html', {'livro': livro})