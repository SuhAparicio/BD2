from django.db import connection
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
    with connection.cursor() as cursor:
        cursor.execute("SELECT id_editora, nome, localizacao FROM Editoras ORDER BY id_editora;")
        editoras = cursor.fetchall()
    # editoras = [(id, nome, localizacao), ...]
    return render(request, 'editoras/list.html', {'editoras': editoras})

@login_required
def editora_detail(request, id_editora):
    with connection.cursor() as cursor:
        cursor.execute("SELECT id_editora, nome, localizacao FROM Editoras WHERE id_editora = %s;", [id_editora])
        editora = cursor.fetchone()
    # editora = (id, nome, localizacao)
    return render(request, 'editoras/detail.html', {'editora': editora})

@login_required
def editora_create(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        localizacao = request.POST.get('localizacao')
        with connection.cursor() as cursor:
            cursor.execute("CALL inserir_editora(%s, %s);", [nome, localizacao])
        return redirect('editoras:editora_list')
    return render(request, 'editoras/create.html')

@login_required
def editora_update(request, id_editora):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        localizacao = request.POST.get('localizacao')
        with connection.cursor() as cursor:
            cursor.execute("CALL atualizar_editora(%s, %s, %s);", [id_editora, nome, localizacao])
        return redirect('editoras:editora_list')
    # Para mostrar o formulário com dados atuais:
    with connection.cursor() as cursor:
        cursor.execute("SELECT nome, localizacao FROM Editoras WHERE id_editora = %s;", [id_editora])
        row = cursor.fetchone()
    return render(request, 'editoras/update.html', {'id_editora': id_editora, 'nome': row[0], 'localizacao': row[1]})

@login_required
def editora_delete(request, id_editora):
    if request.method == 'POST':
        with connection.cursor() as cursor:
            cursor.execute("CALL eliminar_editora(%s);", [id_editora])
        return redirect('editoras:editora_list')
    # Para mostrar confirmação:
    return render(request, 'editoras/delete.html', {'id_editora': id_editora})