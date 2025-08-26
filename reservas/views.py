from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import ReservaForm
from .models import Reserva
from utilizadores.mongo_utils import listar_utilizadores
from bson.objectid import ObjectId

@login_required
def reserva_list(request):
    reservas = Reserva.objects.all()
    utilizadores = listar_utilizadores()
    # Cria um dicionário para pesquisa rápida pelo id
    utilizadores_dict = {str(u['_id']): u['nome'] for u in utilizadores}
    # Adiciona o nome do utilizador a cada reserva
    for reserva in reservas:
        reserva.utilizador_nome = utilizadores_dict.get(reserva.utilizador_id, 'Desconhecido')
    return render(request, 'reservas/list.html', {'reservas': reservas})

@login_required
def reserva_detail(request, pk):
    reserva = get_object_or_404(Reserva, pk=pk)
    # Buscar nome do utilizador no MongoDB
    utilizador_nome = None
    if reserva.utilizador_id:
        utilizadores = listar_utilizadores()
        for u in utilizadores:
            if u['id'] == reserva.utilizador_id:
                utilizador_nome = u['nome']
                break
    return render(request, 'reservas/detail.html', {'reserva': reserva, 'utilizador_nome': utilizador_nome})

@login_required
def reserva_create(request):
    utilizadores = listar_utilizadores()
    for u in utilizadores:
        u['id'] = str(u['_id'])           # Adiciona o campo 'id' como string
    opcoes_utilizador = [(u['id'], u['nome']) for u in utilizadores]  # Usa 'id' no dropdown
    if request.method == 'POST':
        form = ReservaForm(request.POST)
        form.fields['utilizador_id'].choices = opcoes_utilizador
        if form.is_valid():
            reserva = form.save(commit=False)
            # Guarda o utilizador_id selecionado
            reserva.utilizador_id = form.cleaned_data['utilizador_id']
            if reserva.data_retirada:
                reserva.livro.disponivel = False
                reserva.livro.save()
            reserva.save()
            return redirect('reservas:reserva_list')
    else:
        form = ReservaForm()
        form.fields['utilizador_id'].choices = opcoes_utilizador
    return render(request, 'reservas/create.html', {'form': form})

@login_required
def reserva_update(request, pk):
    reserva = get_object_or_404(Reserva, pk=pk)
    utilizadores = listar_utilizadores()
    for u in utilizadores:
        u['id'] = str(u['_id'])           # Adiciona o campo 'id' como string
    opcoes_utilizador = [(u['id'], u['nome']) for u in utilizadores]  # Usa 'id' no dropdown
    if request.method == 'POST':
        form = ReservaForm(request.POST, instance=reserva)
        form.fields['utilizador_id'].choices = opcoes_utilizador
        if form.is_valid():
            reserva = form.save(commit=False)
            reserva.utilizador_id = form.cleaned_data['utilizador_id']
            reserva.save()
            return redirect('reservas:reserva_list')
    else:
        form = ReservaForm(instance=reserva)
        form.fields['utilizador_id'].choices = opcoes_utilizador
    return render(request, 'reservas/update.html', {'form': form})

@login_required
def reserva_delete(request, pk):
    reserva = get_object_or_404(Reserva, pk=pk)
    if request.method == 'POST':
        if not reserva.concluida:
            reserva.livro.disponivel = True
            reserva.livro.save()
        reserva.delete()
        return redirect('reservas:reserva_list')
    return render(request, 'reservas/delete.html', {'reserva': reserva})