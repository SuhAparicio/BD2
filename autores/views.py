from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import AutorForm
from .models import Autor

@login_required
def autor_list(request):
    autores = Autor.objects.all()
    return render(request, 'autores/list.html', {'autores': autores})

@login_required
def autor_detail(request, pk):
    autor = get_object_or_404(Autor, pk=pk)
    return render(request, 'autores/detail.html', {'autor': autor})

@login_required
def autor_create(request):
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
    autor = get_object_or_404(Autor, pk=pk)
    if request.method == 'POST':
        autor.delete()
        return redirect('autores:autor_list')
    return render(request, 'autores/delete.html', {'autor': autor})