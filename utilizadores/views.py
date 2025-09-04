from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User, Group
from django.utils.crypto import get_random_string
from .mongo_utils import listar_utilizadores, inserir_utilizador, get_mongo_collection, atualizar_utilizador, obter_utilizador_por_id
from django import forms
from bson.objectid import ObjectId
from .forms import UtilizadorCreateForm, UtilizadorUpdateForm

def is_admin(user):
    return user.is_superuser or user.groups.filter(name='admin').exists()

@login_required
def utilizador_list(request):
    if not is_admin(request.user):
        return render(request, '404.html', status=404)
    utilizadores = listar_utilizadores()
    for u in utilizadores:
        u['id'] = str(u['_id'])
    return render(request, 'utilizadores/list.html', {'utilizadores': utilizadores})

@login_required
def utilizador_detail(request, pk):
    if not is_admin(request.user):
        return render(request, '404.html', status=404)
    utilizador = obter_utilizador_por_id(pk)
    utilizador['id'] = str(utilizador['_id'])  # Adiciona campo 'id' para usar no template
    user = User.objects.get(id=utilizador['django_user_id'])
    return render(request, 'utilizadores/detail.html', {
        'utilizador': utilizador,
        'username': user.username
    })

@login_required
def utilizador_create(request):
    if not is_admin(request.user):
        return render(request, '404.html', status=404)
    if request.method == 'POST':
        form = UtilizadorCreateForm(request.POST)
        if form.is_valid():
            role = form.cleaned_data['role']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            # Define permissões conforme a role
            if User.objects.filter(username=username).exists():
                form.add_error('username', 'Já existe um utilizador com esse username.')
                return render(request, 'utilizadores/create.html', {'form': form})
            if role == 'admin':
                user = User.objects.create_user(username=username, password=password, is_superuser=True, is_staff=True)
            else:
                user = User.objects.create_user(username=username, password=password, is_superuser=False, is_staff=True)
            # Atribui ao grupo correto
            group, _ = Group.objects.get_or_create(name=role)
            user.groups.add(group)
            user.save()
            # Guarda o utilizador no MongoDB com o id do user Django
            inserir_utilizador(
                nome=form.cleaned_data['nome'],
                contacto=form.cleaned_data['contacto'],
                django_user_id=user.id,
                role=role
            )
            return redirect('utilizadores:utilizador_list')
    else:
        # Gera uma password aleatória para pré-preencher o campo
        random_password = get_random_string(16)
        form = UtilizadorCreateForm(initial={'password': random_password})
    return render(request, 'utilizadores/create.html', {'form': form})

@login_required
def utilizador_update(request, pk):
    if not is_admin(request.user):
        return render(request, '404.html', status=404)
    utilizador = obter_utilizador_por_id(pk)
    user = User.objects.get(id=utilizador['django_user_id'])
    if request.method == 'POST':
        form = UtilizadorUpdateForm(request.POST, user_instance=user)
        if form.is_valid():
            user.username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            if password and password.strip():
                user.set_password(password)
            # Atualiza superuser conforme a role
            role = form.cleaned_data['role']
            user.is_superuser = (role == 'admin')
            # Remove de todos os grupos e adiciona ao novo grupo
            user.groups.clear()
            group, _ = Group.objects.get_or_create(name=role)
            user.groups.add(group)
            user.save()
            atualizar_utilizador(
                pk,
                {
                    'nome': form.cleaned_data['nome'],
                    'contacto': form.cleaned_data['contacto'],
                    'username': form.cleaned_data['username'],
                    'role': role,
                }
            )
            return redirect('utilizadores:utilizador_list')
    else:
        initial = {
            'nome': utilizador['nome'],
            'contacto': utilizador.get('contacto', ''),
            'username': user.username,
            'password': '',
            'role': utilizador['role'],
        }
        form = UtilizadorUpdateForm(initial=initial, user_instance=user)
    return render(request, 'utilizadores/update.html', {'form': form})

@login_required
def utilizador_delete(request, pk):
    if not is_admin(request.user):
        return render(request, '404.html', status=404)
    colecao = get_mongo_collection()
    utilizador = colecao.find_one({'_id': ObjectId(pk)})
    utilizador['django_user_id'] = str(utilizador.get('django_user_id', ''))
    user_django_id = utilizador.get('django_user_id')
    user_to_delete = User.objects.get(id=user_django_id) if user_django_id else None
    # Impede apagar o próprio utilizador
    if request.user.id == int(user_django_id):
        return render(request, 'utilizadores/delete.html', {
            'utilizador': utilizador,
            'error': 'Não pode eliminar o seu próprio utilizador. Apenas outro admin pode fazê-lo.'
        })
    if request.method == 'POST':
        if user_to_delete:
            user_to_delete.delete()
        colecao.delete_one({'_id': ObjectId(pk)})
        return redirect('utilizadores:utilizador_list')
    return render(request, 'utilizadores/delete.html', {'utilizador': utilizador})
