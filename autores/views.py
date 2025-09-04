from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from .forms import AutorForm
from .models import Autor

def is_bibliotecario_ou_admin(user):
    return (
        user.is_superuser or
        user.groups.filter(name='bibliotecario').exists() or
        user.groups.filter(name='admin').exists()
    )

@login_required
def autor_list(request):
    if not is_bibliotecario_ou_admin(request.user):
        return render(request, '404.html', status=404)
    autores = Autor.objects.all()
    return render(request, 'autores/list.html', {'autores': autores})

@login_required
def autor_detail(request, pk):
    if not is_bibliotecario_ou_admin(request.user):
        return render(request, '404.html', status=404)
    autor = get_object_or_404(Autor, pk=pk)
    return render(request, 'autores/detail.html', {'autor': autor})

@login_required
def autor_create(request):
    if not is_bibliotecario_ou_admin(request.user):
        return render(request, '404.html', status=404)
    if request.method == 'POST':
        form = AutorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('autores:autor_list')
    else:
        form = AutorForm()
    return render(request, 'autores/create.html', {'form': form})

@login_required
def autor_update(request, pk):
    if not is_bibliotecario_ou_admin(request.user):
        return render(request, '404.html', status=404)
    autor = get_object_or_404(Autor, pk=pk)
    if request.method == 'POST':
        form = AutorForm(request.POST, instance=autor)
        if form.is_valid():
            form.save()
            return redirect('autores:autor_list')
    else:
        form = AutorForm(instance=autor)
    return render(request, 'autores/update.html', {'form': form})

@login_required
def autor_delete(request, pk):
    if not is_bibliotecario_ou_admin(request.user):
        return render(request, '404.html', status=404)
    autor = get_object_or_404(Autor, pk=pk)
    if request.method == 'POST':
        autor.delete()
        return redirect('autores:autor_list')
    return render(request, 'autores/delete.html', {'autor': autor})