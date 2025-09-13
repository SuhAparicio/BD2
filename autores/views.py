from django.shortcuts import render, redirect
from django.db import connections
from django.contrib.auth.decorators import login_required
import datetime
from django.db import DatabaseError

from utilizadores.mongo_utils import is_admin, is_bibliotecario

def get_db_connection_for_user(user):
    from utilizadores.mongo_utils import is_admin, is_bibliotecario, is_membro
    if is_admin(user.id):
        return connections['admin']
    elif is_bibliotecario(user.id):
        return connections['bibliotecario']
    elif is_membro(user.id):
        return connections['membro']
    else:
        return connections['default']

def is_bibliotecario_ou_admin(user):
    return is_admin(user) or is_bibliotecario(user)

@login_required
def autor_list(request):
    if not is_bibliotecario_ou_admin(request.user.id):
        return render(request, '404.html', status=404)
    connection = get_db_connection_for_user(request.user)
    error = None
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT id_autor, nome, data_nascimento, nacionalidade FROM Autores ORDER BY nome;")
            autores = cursor.fetchall()
    except Exception as e:
        autores = []
        error = str(e).split('\n')[0]
    return render(request, 'autores/list.html', {'autores': autores, 'error': error})

@login_required
def autor_detail(request, pk):
    if not is_bibliotecario_ou_admin(request.user.id):
        return render(request, '404.html', status=404)
    connection = get_db_connection_for_user(request.user)
    with connection.cursor() as cursor:
        cursor.execute("SELECT id_autor, nome, data_nascimento, nacionalidade FROM Autores WHERE id_autor = %s;", [pk])
        autor = cursor.fetchone()
    return render(request, 'autores/detail.html', {'autor': autor})

@login_required
def autor_create(request):
    if not is_bibliotecario_ou_admin(request.user.id):
        return render(request, '404.html', status=404)
    connection = get_db_connection_for_user(request.user)
    error = None
    if request.method == 'POST':
        nome = request.POST.get('nome')
        data_nascimento = request.POST.get('data_nascimento') or None
        nacionalidade = request.POST.get('nacionalidade')
        try:
            with connection.cursor() as cursor:
                cursor.execute("CALL inserir_autor(%s, %s, %s);", [nome, data_nascimento, nacionalidade])
            return redirect('autores:autor_list')
        except DatabaseError as e:
            error = str(e).split('\n')[0]  # Só a mensagem principal
    return render(request, 'autores/create.html', {'error': error})

@login_required
def autor_update(request, pk):
    if not is_bibliotecario_ou_admin(request.user.id):
        return render(request, '404.html', status=404)
    connection = get_db_connection_for_user(request.user)
    error = None
    with connection.cursor() as cursor:
        cursor.execute("SELECT id_autor, nome, data_nascimento, nacionalidade FROM Autores WHERE id_autor = %s;", [pk])
        autor = cursor.fetchone()
    # Converte data_nascimento para string YYYY-MM-DD ou vazio
    data_nascimento_str = ''
    if autor and autor[2]:
        if isinstance(autor[2], datetime.date):
            data_nascimento_str = autor[2].strftime('%Y-%m-%d')
        else:
            data_nascimento_str = str(autor[2])
    if request.method == 'POST':
        nome = request.POST.get('nome')
        data_nascimento = request.POST.get('data_nascimento') or None
        nacionalidade = request.POST.get('nacionalidade')
        try:
            with connection.cursor() as cursor:
                cursor.execute("CALL atualizar_autor(%s, %s, %s, %s);", [pk, nome, data_nascimento, nacionalidade])
            return redirect('autores:autor_list')
        except DatabaseError as e:
            error = str(e).split('\n')[0]
    return render(request, 'autores/update.html', {
        'autor': autor,
        'error': error,
        'nome': autor[1] if autor else '',
        'data_nascimento': data_nascimento_str,
        'nacionalidade': autor[3] if autor else '',
    })

@login_required
def autor_delete(request, pk):
    if not is_bibliotecario_ou_admin(request.user.id):
        return render(request, '404.html', status=404)
    connection = get_db_connection_for_user(request.user)
    error = None
    with connection.cursor() as cursor:
        cursor.execute("SELECT id_autor, nome FROM Autores WHERE id_autor = %s;", [pk])
        autor = cursor.fetchone()
    if request.method == 'POST':
        try:
            with connection.cursor() as cursor:
                cursor.execute("CALL eliminar_autor(%s);", [pk])
            return redirect('autores:autor_list')
        except DatabaseError as e:
            error = str(e).split('\n')[0]
    return render(request, 'autores/delete.html', {'autor': autor, 'error': error})