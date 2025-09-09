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
def categoria_list(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT id_categoria, nome, descricao FROM Categorias ORDER BY id_categoria;")
        categorias = cursor.fetchall()
    # categorias = [(id, nome, descricao), ...]
    return render(request, 'categorias/list.html', {'categorias': categorias})

@login_required
def categoria_detail(request, id_categoria):
    with connection.cursor() as cursor:
        cursor.execute("SELECT id_categoria, nome, descricao FROM Categorias WHERE id_categoria = %s;", [id_categoria])
        categoria = cursor.fetchone()
    # categoria = (id, nome, descricao)
    return render(request, 'categorias/detail.html', {'categoria': categoria})

@login_required
def categoria_create(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        descricao = request.POST.get('descricao')
        with connection.cursor() as cursor:
            cursor.execute("CALL inserir_categoria(%s, %s);", [nome, descricao])
        return redirect('categorias:categoria_list')
    return render(request, 'categorias/create.html')

@login_required
def categoria_update(request, id_categoria):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        descricao = request.POST.get('descricao')
        with connection.cursor() as cursor:
            cursor.execute("CALL atualizar_categoria(%s, %s, %s);", [id_categoria, nome, descricao])
        return redirect('categorias:categoria_list')
    # Para mostrar o formulário com dados atuais:
    with connection.cursor() as cursor:
        cursor.execute("SELECT nome, descricao FROM Categorias WHERE id_categoria = %s;", [id_categoria])
        row = cursor.fetchone()
    return render(request, 'categorias/update.html', {'id_categoria': id_categoria, 'nome': row[0], 'descricao': row[1]})

@login_required
def categoria_delete(request, id_categoria):
    if request.method == 'POST':
        with connection.cursor() as cursor:
            cursor.execute("CALL eliminar_categoria(%s);", [id_categoria])
        return redirect('categorias:categoria_list')
    # Para mostrar confirmação:
    return render(request, 'categorias/delete.html', {'id_categoria': id_categoria})