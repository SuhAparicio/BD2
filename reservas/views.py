from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import ReservaForm
from .models import Reserva
from utilizadores.mongo_utils import listar_utilizadores, obter_utilizador_por_id, get_user_by_django_id
from bson.objectid import ObjectId

@login_required
def reserva_list(request):
    utilizadores = listar_utilizadores()
    utilizadores_dict = {str(u['_id']): u['nome'] for u in utilizadores}
    user_mongo_id = None
    # Descobre o id do utilizador logado no MongoDB
    for u in utilizadores:
        if u.get('django_user_id') == request.user.id:
            user_mongo_id = str(u['_id'])
            break
    # Verifica se é membro
    is_membro = request.user.groups.filter(name='membro').exists()
    if is_membro and user_mongo_id:
        reservas = Reserva.objects.filter(utilizador_id=user_mongo_id)
    else:
        reservas = Reserva.objects.all()
    # Adiciona o nome do utilizador a cada reserva
    for reserva in reservas:
        reserva.utilizador_nome = utilizadores_dict.get(reserva.utilizador_id, 'Desconhecido')
    return render(request, 'reservas/list.html', {
        'reservas': reservas,
        'is_membro': is_membro
    })

@login_required
def reserva_detail(request, pk):
    reserva = get_object_or_404(Reserva, pk=pk)
    utilizador_nome = None
    utilizador = obter_utilizador_por_id(reserva.utilizador_id)
    if utilizador:
        utilizador_nome = utilizador.get('nome', reserva.utilizador_id)
    else:
        utilizador_nome = reserva.utilizador_id

    is_membro = request.user.groups.filter(name='membro').exists()
    user_mongo = get_user_by_django_id(request.user.id)
    user_mongo_id = str(user_mongo['_id']) if user_mongo else None

    # Proteção: membro só pode ver as próprias reservas
    if is_membro and reserva.utilizador_id != user_mongo_id:
        return render(request, '404.html', status=404)

    return render(request, 'reservas/detail.html', {
        'reserva': reserva,
        'utilizador_nome': utilizador_nome,
        'is_membro': is_membro
    })

@login_required
def reserva_create(request):
    utilizadores = listar_utilizadores()
    for u in utilizadores:
        u['id'] = str(u['_id'])
    opcoes_utilizador = [('', '--------------')] + [(u['id'], u['nome']) for u in utilizadores]
    is_membro = request.user.groups.filter(name='membro').exists()
    user_mongo = get_user_by_django_id(request.user.id)
    user_mongo_id = str(user_mongo['_id']) if user_mongo else None

    if request.method == 'POST':
        form = ReservaForm(request.POST)
        # Só obriga a selecionar utilizador se não for membro
        form.fields['utilizador_id'].required = not is_membro
        if not is_membro:
            form.fields['utilizador_id'].choices = opcoes_utilizador
        if form.is_valid():
            reserva = form.save(commit=False)
            if is_membro:
                reserva.utilizador_id = user_mongo_id
            else:
                reserva.utilizador_id = form.cleaned_data['utilizador_id']
            reserva.save()
            return redirect('reservas:reserva_list')
    else:
        form = ReservaForm()
        form.fields['utilizador_id'].required = not is_membro
        if not is_membro:
            form.fields['utilizador_id'].choices = opcoes_utilizador
    return render(request, 'reservas/create.html', {
        'form': form,
        'is_membro': is_membro
    })

@login_required
def reserva_update(request, pk):
    reserva = get_object_or_404(Reserva, pk=pk)
    utilizadores = listar_utilizadores()
    for u in utilizadores:
        u['id'] = str(u['_id'])
    opcoes_utilizador = [('', '--------------')] + [(u['id'], u['nome']) for u in utilizadores]
    is_membro = request.user.groups.filter(name='membro').exists()
    user_mongo = get_user_by_django_id(request.user.id)
    user_mongo_id = str(user_mongo['_id']) if user_mongo else None

    # Proteção: membro só pode editar as próprias reservas
    if is_membro and reserva.utilizador_id != user_mongo_id:
        return render(request, '404.html', status=404)

    if request.method == 'POST':
        form = ReservaForm(request.POST, instance=reserva)
        form.fields['utilizador_id'].required = not is_membro
        if not is_membro:
            form.fields['utilizador_id'].choices = opcoes_utilizador
        if form.is_valid():
            reserva = form.save(commit=False)
            if is_membro:
                reserva.utilizador_id = user_mongo_id
            else:
                reserva.utilizador_id = form.cleaned_data['utilizador_id']
            reserva.save()
            return redirect('reservas:reserva_list')
    else:
        form = ReservaForm(instance=reserva)
        form.fields['utilizador_id'].required = not is_membro
        if not is_membro:
            form.fields['utilizador_id'].choices = opcoes_utilizador
    return render(request, 'reservas/update.html', {
        'form': form,
        'is_membro': is_membro
    })

@login_required
def reserva_delete(request, pk):
    reserva = get_object_or_404(Reserva, pk=pk)
    is_membro = request.user.groups.filter(name='membro').exists()
    utilizador_nome = None
    if not is_membro:
        from utilizadores.mongo_utils import obter_utilizador_por_id
        utilizador = obter_utilizador_por_id(reserva.utilizador_id)
        utilizador_nome = utilizador.get('nome', reserva.utilizador_id) if utilizador else reserva.utilizador_id
    if is_membro:
        # Proteção: membro só pode apagar as próprias reservas
        from utilizadores.mongo_utils import get_user_by_django_id
        user_mongo = get_user_by_django_id(request.user.id)
        user_mongo_id = str(user_mongo['_id']) if user_mongo else None
        if reserva.utilizador_id != user_mongo_id:
            return render(request, '404.html', status=404)
    if request.method == 'POST':
        reserva.delete()
        return redirect('reservas:reserva_list')
    return render(request, 'reservas/delete.html', {
        'reserva': reserva,
        'utilizador_nome': utilizador_nome,
        'is_membro': is_membro
    })