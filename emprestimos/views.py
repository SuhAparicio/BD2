from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import EmprestimoForm
from .models import Emprestimo

@login_required
def emprestimo_list(request):
    emprestimos = Emprestimo.objects.all()
    return render(request, 'emprestimos/list.html', {'emprestimos': emprestimos})

@login_required
def emprestimo_detail(request, pk):
    emprestimo = get_object_or_404(Emprestimo, pk=pk)
    return render(request, 'emprestimos/detail.html', {'emprestimo': emprestimo})

@login_required
def emprestimo_create(request):
    if request.method == 'POST':
        form = EmprestimoForm(request.POST)
        if form.is_valid():
            emprestimo = form.save()
            # Marca o livro como indisponível
            emprestimo.livro.disponivel = False
            emprestimo.livro.save()
            return redirect('emprestimos:emprestimo_list')
    else:
        form = EmprestimoForm()
    return render(request, 'emprestimos/create.html', {'form': form})

@login_required
def emprestimo_update(request, pk):
    emprestimo = get_object_or_404(Emprestimo, pk=pk)
    if request.method == 'POST':
        form = EmprestimoForm(request.POST, instance=emprestimo)
        if form.is_valid():
            form.save()
            return redirect('emprestimos:emprestimo_list')
    else:
        form = EmprestimoForm(instance=emprestimo)
    return render(request, 'emprestimos/update.html', {'form': form})

@login_required
def emprestimo_delete(request, pk):
    emprestimo = get_object_or_404(Emprestimo, pk=pk)
    if request.method == 'POST':
        # Marca o livro como disponível ao devolver
        if emprestimo.devolvido:
            emprestimo.livro.disponivel = True
            emprestimo.livro.save()
        emprestimo.delete()
        return redirect('emprestimos:emprestimo_list')
    return render(request, 'emprestimos/delete.html', {'emprestimo': emprestimo})