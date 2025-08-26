from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .mongo_utils import listar_utilizadores, inserir_utilizador, get_mongo_collection
from django import forms
from bson.objectid import ObjectId
from .forms import UtilizadorForm

@login_required
def utilizador_list(request):
    utilizadores = listar_utilizadores()
    for u in utilizadores:
        u['id'] = str(u['_id'])
    return render(request, 'utilizadores/list.html', {'utilizadores': utilizadores})

@login_required
def utilizador_detail(request, pk):
    colecao = get_mongo_collection()
    utilizador = colecao.find_one({'_id': ObjectId(pk)})
    if not utilizador:
        return redirect('utilizadores:utilizador_list')
    utilizador['id'] = pk
    return render(request, 'utilizadores/detail.html', {'utilizador': utilizador})

@login_required
def utilizador_create(request):
    if request.method == 'POST':
        form = UtilizadorForm(request.POST)
        if form.is_valid():
            inserir_utilizador(
                nome=form.cleaned_data['nome'],
                contacto=form.cleaned_data['contacto'],
                numero_socio=form.cleaned_data['numero_socio'],
                user_id=request.user.id
            )
            return redirect('utilizadores:utilizador_list')
    else:
        form = UtilizadorForm()
    return render(request, 'utilizadores/create.html', {'form': form})

@login_required
def utilizador_update(request, pk):
    colecao = get_mongo_collection()
    utilizador = colecao.find_one({'_id': ObjectId(pk)})
    if not utilizador:
        return redirect('utilizadores:utilizador_list')
    if request.method == 'POST':
        form = UtilizadorForm(request.POST)
        if form.is_valid():
            colecao.update_one(
                {'_id': ObjectId(pk)},
                {'$set': {
                    'nome': form.cleaned_data['nome'],
                    'contacto': form.cleaned_data['contacto'],
                    'numero_socio': form.cleaned_data['numero_socio']
                }}
            )
            return redirect('utilizadores:utilizador_list')
    else:
        form = UtilizadorForm(initial={
            'nome': utilizador.get('nome', ''),
            'contacto': utilizador.get('contacto', ''),
            'numero_socio': utilizador.get('numero_socio', '')
        })
    return render(request, 'utilizadores/update.html', {'form': form})

@login_required
def utilizador_delete(request, pk):
    colecao = get_mongo_collection()
    utilizador = colecao.find_one({'_id': ObjectId(pk)})
    if request.method == 'POST':
        colecao.delete_one({'_id': ObjectId(pk)})
        return redirect('utilizadores:utilizador_list')
    return render(request, 'utilizadores/delete.html', {'utilizador': utilizador})