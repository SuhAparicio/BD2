from django.shortcuts import render, redirect
from django.db import connection
from django.contrib.auth.decorators import login_required
from django.db import DatabaseError

def is_bibliotecario_ou_admin(user):
    return (
        user.is_superuser or
        user.groups.filter(name='bibliotecario').exists() or
        user.groups.filter(name='admin').exists()
    )

@login_required
def livro_list(request):
    error = None
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT l.id_livro, l.titulo, l.isbn, l.ano_publicacao,
                       c.nome as categoria, a.nome as autor, e.nome as editora
                FROM Livros l
                LEFT JOIN Categorias c ON l.id_categoria = c.id_categoria
                LEFT JOIN Autores a ON l.id_autor = a.id_autor
                LEFT JOIN Editoras e ON l.id_editora = e.id_editora
                ORDER BY l.titulo;
            """)
            livros = cursor.fetchall()
    except Exception as e:
        livros = []
        error = str(e).split('\n')[0]  # Só a primeira linha do erro
    is_membro = request.user.groups.filter(name='membro').exists()
    return render(request, 'livros/list.html', {'livros': livros, 'is_membro': is_membro, 'error': error})

@login_required
def livro_detail(request, pk):
    error = None
    livro = None
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT l.id_livro, l.titulo, l.isbn, l.ano_publicacao,
                       c.nome as categoria, a.nome as autor, e.nome as editora
                FROM Livros l
                LEFT JOIN Categorias c ON l.id_categoria = c.id_categoria
                LEFT JOIN Autores a ON l.id_autor = a.id_autor
                LEFT JOIN Editoras e ON l.id_editora = e.id_editora
                WHERE l.id_livro = %s;
            """, [pk])
            livro = cursor.fetchone()
    except Exception as e:
        error = str(e).split('\n')[0]  # Só a primeira linha do erro
    return render(request, 'livros/detail.html', {'livro': livro, 'error': error})

@login_required
def livro_create(request):
    if not is_bibliotecario_ou_admin(request.user):
        return render(request, '404.html', status=404)
    with connection.cursor() as cursor:
        cursor.execute("SELECT id_autor, nome FROM Autores ORDER BY nome;")
        autores = cursor.fetchall()
        cursor.execute("SELECT id_categoria, nome FROM Categorias ORDER BY nome;")
        categorias = cursor.fetchall()
        cursor.execute("SELECT id_editora, nome FROM Editoras ORDER BY nome;")
        editoras = cursor.fetchall()
    error = None
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        isbn = request.POST.get('isbn')
        ano_publicacao = request.POST.get('ano_publicacao') or None
        id_categoria = request.POST.get('id_categoria') or None
        id_autor = request.POST.get('id_autor') or None
        id_editora = request.POST.get('id_editora') or None
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "CALL inserir_livro(%s, %s, %s, %s, %s, %s);",
                    [titulo, isbn, ano_publicacao, id_categoria, id_autor, id_editora]
                )
            return redirect('livros:livro_list')
        except DatabaseError as e:
            error = str(e).split('\n')[0]  # Só a primeira linha do erro
    return render(request, 'livros/create.html', {
        'autores': autores,
        'categorias': categorias,
        'editoras': editoras,
        'error': error,
    })

@login_required
def livro_update(request, pk):
    if not is_bibliotecario_ou_admin(request.user):
        return render(request, '404.html', status=404)
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id_livro, titulo, isbn, ano_publicacao, id_categoria, id_autor, id_editora
            FROM Livros WHERE id_livro = %s;
        """, [pk])
        livro = cursor.fetchone()
        cursor.execute("SELECT id_autor, nome FROM Autores ORDER BY nome;")
        autores = cursor.fetchall()
        cursor.execute("SELECT id_categoria, nome FROM Categorias ORDER BY nome;")
        categorias = cursor.fetchall()
        cursor.execute("SELECT id_editora, nome FROM Editoras ORDER BY nome;")
        editoras = cursor.fetchall()
    error = None
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        isbn = request.POST.get('isbn')
        ano_publicacao = request.POST.get('ano_publicacao') or None
        id_categoria = request.POST.get('id_categoria') or None
        id_autor = request.POST.get('id_autor') or None
        id_editora = request.POST.get('id_editora') or None
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "CALL atualizar_livro(%s, %s, %s, %s, %s, %s, %s);",
                    [pk, titulo, isbn, ano_publicacao, id_categoria, id_autor, id_editora]
                )
            return redirect('livros:livro_list')
        except DatabaseError as e:
            error = str(e).split('\n')[0]  # Só a primeira linha do erro
    return render(request, 'livros/update.html', {
        'livro': livro,
        'autores': autores,
        'categorias': categorias,
        'editoras': editoras,
        'error': error,
    })

@login_required
def livro_delete(request, pk):
    if not is_bibliotecario_ou_admin(request.user):
        return render(request, '404.html', status=404)
    with connection.cursor() as cursor:
        cursor.execute("SELECT titulo FROM Livros WHERE id_livro = %s;", [pk])
        livro = cursor.fetchone()
    error = None
    if request.method == 'POST':
        try:
            with connection.cursor() as cursor:
                cursor.execute("CALL eliminar_livro(%s);", [pk])
            return redirect('livros:livro_list')
        except DatabaseError as e:
            error = str(e).split('\n')[0]  # Só a primeira linha do erro
    return render(request, 'livros/delete.html', {'livro': livro[0] if livro else '', 'error': error})