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
def categoria_list(request):
    error = None
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT id_categoria, nome, descricao FROM Categorias ORDER BY id_categoria;")
            categorias = cursor.fetchall()
    except Exception as e:
        categorias = []
        error = str(e).split('\n')[0]
    return render(request, 'categorias/list.html', {'categorias': categorias, 'error': error})

@login_required
def categoria_detail(request, id_categoria):
    error = None
    categoria = None
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT id_categoria, nome, descricao FROM Categorias WHERE id_categoria = %s;", [id_categoria])
            categoria = cursor.fetchone()
    except Exception as e:
        error = str(e).split('\n')[0]
    return render(request, 'categorias/detail.html', {'categoria': categoria, 'error': error})

@login_required
def categoria_create(request):
    error = None
    if request.method == 'POST':
        nome = request.POST.get('nome')
        descricao = request.POST.get('descricao')
        try:
            with connection.cursor() as cursor:
                cursor.execute("CALL inserir_categoria(%s, %s);", [nome, descricao])
            return redirect('categorias:categoria_list')
        except DatabaseError as e:
            error = str(e).split('\n')[0]
    return render(request, 'categorias/create.html', {'error': error})

@login_required
def categoria_update(request, id_categoria):
    error = None
    if request.method == 'POST':
        nome = request.POST.get('nome')
        descricao = request.POST.get('descricao')
        try:
            with connection.cursor() as cursor:
                cursor.execute("CALL atualizar_categoria(%s, %s, %s);", [id_categoria, nome, descricao])
            return redirect('categorias:categoria_list')
        except DatabaseError as e:
            error = str(e).split('\n')[0]
        # Mantém os valores preenchidos em caso de erro
        return render(request, 'categorias/update.html', {
            'id_categoria': id_categoria,
            'nome': nome,
            'descricao': descricao,
            'error': error,
        })
    # Para mostrar o formulário com dados atuais:
    with connection.cursor() as cursor:
        cursor.execute("SELECT nome, descricao FROM Categorias WHERE id_categoria = %s;", [id_categoria])
        row = cursor.fetchone()
    return render(request, 'categorias/update.html', {
        'id_categoria': id_categoria,
        'nome': row[0],
        'descricao': row[1],
        'error': error,
    })

@login_required
def categoria_delete(request, id_categoria):
    error = None
    if request.method == 'POST':
        try:
            with connection.cursor() as cursor:
                cursor.execute("CALL eliminar_categoria(%s);", [id_categoria])
            return redirect('categorias:categoria_list')
        except DatabaseError as e:
            error = str(e).split('\n')[0]
        return render(request, 'categorias/delete.html', {
            'id_categoria': id_categoria,
            'error': error,
        })
    return render(request, 'categorias/delete.html', {
        'id_categoria': id_categoria,
        'error': error,
    })