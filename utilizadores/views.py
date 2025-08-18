from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import UtilizadorForm
from .models import UtilizadorBiblioteca

@login_required
def utilizador_list(request):
    utilizadores = UtilizadorBiblioteca.objects.all()
    return render(request, 'utilizadores/list.html', {'utilizadores': utilizadores})

@login_required
def utilizador_detail(request, pk):
    utilizador = get_object_or_404(UtilizadorBiblioteca, pk=pk)
    return render(request, 'utilizadores/detail.html', {'utilizador': utilizador})

@login_required
def utilizador_create(request):
    if request.method == 'POST':
        form = UtilizadorForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)  # não salva ainda
            obj.user = request.user  # garante que o user_id não será nulo
            obj.save()
            return redirect('utilizadores:utilizador_list')
    else:
        form = UtilizadorForm()
    return render(request, 'utilizadores/create.html', {'form': form})

@login_required
def utilizador_update(request, pk):
    utilizador = get_object_or_404(UtilizadorBiblioteca, pk=pk)
    if request.method == 'POST':
        form = UtilizadorForm(request.POST, instance=utilizador)
        if form.is_valid():
            form.save()
            return redirect('utilizadores:utilizador_list')
    else:
        form = UtilizadorForm(instance=utilizador)
    return render(request, 'utilizadores/update.html', {'form': form})

@login_required
def utilizador_delete(request, pk):
    utilizador = get_object_or_404(UtilizadorBiblioteca, pk=pk)
    if request.method == 'POST':
        utilizador.delete()
        return redirect('utilizadores:utilizador_list')
    return render(request, 'utilizadores/delete.html', {'utilizador': utilizador})