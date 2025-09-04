from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from .forms import EmprestimoForm
from .models import Emprestimo
from utilizadores.mongo_utils import listar_utilizadores
from bson.objectid import ObjectId

def is_bibliotecario_ou_admin(user):
    return (
        user.is_superuser or
        user.groups.filter(name='bibliotecario').exists() or
        user.groups.filter(name='admin').exists()
    )

@login_required
def emprestimo_list(request):
    if not is_bibliotecario_ou_admin(request.user):
        return render(request, '404.html', status=404)
    emprestimos = Emprestimo.objects.all()
    utilizadores = listar_utilizadores()
    utilizadores_dict = {str(u['_id']): u['nome'] for u in utilizadores}
    for emprestimo in emprestimos:
        emprestimo.utilizador_nome = utilizadores_dict.get(emprestimo.utilizador_id, 'Desconhecido')
    return render(request, 'emprestimos/list.html', {'emprestimos': emprestimos})

@login_required
def emprestimo_detail(request, pk):
    if not is_bibliotecario_ou_admin(request.user):
        return render(request, '404.html', status=404)
    emprestimo = get_object_or_404(Emprestimo, pk=pk)
    utilizador_nome = None
    if emprestimo.utilizador_id:
        utilizadores = listar_utilizadores()
        for u in utilizadores:
            u_id = str(u['_id'])  # Converte o ObjectId para string
            if u_id == emprestimo.utilizador_id:
                utilizador_nome = u['nome']
                break
    return render(request, 'emprestimos/detail.html', {'emprestimo': emprestimo, 'utilizador_nome': utilizador_nome})

@login_required
def emprestimo_create(request):
    if not is_bibliotecario_ou_admin(request.user):
        return render(request, '404.html', status=404)
    utilizadores = listar_utilizadores()
    for u in utilizadores:
        u['id'] = str(u['_id'])           # Adiciona o campo 'id' como string
    opcoes_utilizador = [(u['id'], u['nome']) for u in utilizadores]  # Usa 'id' no dropdown
    if request.method == 'POST':
        form = EmprestimoForm(request.POST)
        form.fields['utilizador_id'].choices = opcoes_utilizador
        if form.is_valid():
            emprestimo = form.save(commit=False)
            emprestimo.utilizador_id = form.cleaned_data['utilizador_id']
            emprestimo.livro.disponivel = False
            emprestimo.livro.save()
            emprestimo.save()
            return redirect('emprestimos:emprestimo_list')
    else:
        form = EmprestimoForm()
        form.fields['utilizador_id'].choices = opcoes_utilizador
    return render(request, 'emprestimos/create.html', {'form': form})

@login_required
def emprestimo_update(request, pk):
    if not is_bibliotecario_ou_admin(request.user):
        return render(request, '404.html', status=404)
    emprestimo = get_object_or_404(Emprestimo, pk=pk)
    utilizadores = listar_utilizadores()
    for u in utilizadores:
        u['id'] = str(u['_id'])           # Adiciona o campo 'id' como string
    opcoes_utilizador = [(u['id'], u['nome']) for u in utilizadores]  # Usa 'id' no dropdown
    if request.method == 'POST':
        form = EmprestimoForm(request.POST, instance=emprestimo)
        form.fields['utilizador_id'].choices = opcoes_utilizador
        if form.is_valid():
            emprestimo = form.save(commit=False)
            emprestimo.utilizador_id = form.cleaned_data['utilizador_id']
            emprestimo.save()
            return redirect('emprestimos:emprestimo_list')
    else:
        form = EmprestimoForm(instance=emprestimo)
        form.fields['utilizador_id'].choices = opcoes_utilizador
    return render(request, 'emprestimos/update.html', {'form': form})

@login_required
def emprestimo_delete(request, pk):
    if not is_bibliotecario_ou_admin(request.user):
        return render(request, '404.html', status=404)
    emprestimo = get_object_or_404(Emprestimo, pk=pk)
    if request.method == 'POST':
        if emprestimo.devolvido:
            emprestimo.livro.disponivel = True
            emprestimo.livro.save()
        emprestimo.delete()
        return redirect('emprestimos:emprestimo_list')
    return render(request, 'emprestimos/delete.html', {'emprestimo': emprestimo})