from django.db import connection, DatabaseError
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

def is_bibliotecario_ou_admin(user):
    return (
        user.is_superuser or
        user.groups.filter(name='bibliotecario').exists() or
        user.groups.filter(name='admin').exists()
    )

@login_required
def editora_list(request):
    error = None
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT id_editora, nome, localizacao FROM Editoras ORDER BY id_editora;")
            editoras = cursor.fetchall()
    except Exception as e:
        editoras = []
        error = str(e).split('\n')[0]
    return render(request, 'editoras/list.html', {'editoras': editoras, 'error': error})

@login_required
def editora_detail(request, id_editora):
    error = None
    editora = None
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT id_editora, nome, localizacao FROM Editoras WHERE id_editora = %s;", [id_editora])
            editora = cursor.fetchone()
    except Exception as e:
        error = str(e).split('\n')[0]
    return render(request, 'editoras/detail.html', {'editora': editora, 'error': error})

@login_required
def editora_create(request):
    error = None
    if request.method == 'POST':
        nome = request.POST.get('nome')
        localizacao = request.POST.get('localizacao')
        try:
            with connection.cursor() as cursor:
                cursor.execute("CALL inserir_editora(%s, %s);", [nome, localizacao])
            return redirect('editoras:editora_list')
        except DatabaseError as e:
            error = str(e).split('\n')[0]
    return render(request, 'editoras/create.html', {'error': error})

@login_required
def editora_update(request, id_editora):
    error = None
    if request.method == 'POST':
        nome = request.POST.get('nome')
        localizacao = request.POST.get('localizacao')
        try:
            with connection.cursor() as cursor:
                cursor.execute("CALL atualizar_editora(%s, %s, %s);", [id_editora, nome, localizacao])
            return redirect('editoras:editora_list')
        except DatabaseError as e:
            error = str(e).split('\n')[0]
        return render(request, 'editoras/update.html', {
            'id_editora': id_editora,
            'nome': nome,
            'localizacao': localizacao,
            'error': error,
        })
    with connection.cursor() as cursor:
        cursor.execute("SELECT nome, localizacao FROM Editoras WHERE id_editora = %s;", [id_editora])
        row = cursor.fetchone()
    return render(request, 'editoras/update.html', {
        'id_editora': id_editora,
        'nome': row[0],
        'localizacao': row[1],
        'error': error,
    })

@login_required
def editora_delete(request, id_editora):
    error = None
    if request.method == 'POST':
        try:
            with connection.cursor() as cursor:
                cursor.execute("CALL eliminar_editora(%s);", [id_editora])
            return redirect('editoras:editora_list')
        except DatabaseError as e:
            error = str(e).split('\n')[0]
        return render(request, 'editoras/delete.html', {
            'id_editora': id_editora,
            'error': error,
        })
    return render(request, 'editoras/delete.html', {
        'id_editora': id_editora,
        'error': error,
    })