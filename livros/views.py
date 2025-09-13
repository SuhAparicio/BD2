from django.shortcuts import render, redirect
from django.db import connections
from django.contrib.auth.decorators import login_required
from django.db import DatabaseError

from utilizadores.mongo_utils import is_admin, is_bibliotecario, is_membro

def is_bibliotecario_ou_admin(user):
    return is_admin(user) or is_bibliotecario(user)

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

@login_required
def livro_list(request):
    connection = get_db_connection_for_user(request.user)
    error = None
    livro_estrela = None
    livro_estrela_obj = None
    livros = []
    # Filtros do GET
    nome_livro = request.GET.get('nome_livro') or None
    mostrar_disponivel = request.GET.get('mostrar_disponivel')
    mostrar_indisponivel = request.GET.get('mostrar_indisponivel')
    # Por default, ambos True
    disponivel_param = True
    nao_disponivel_param = True
    if request.GET:
        disponivel_param = True if mostrar_disponivel == 'on' else False
        nao_disponivel_param = True if mostrar_indisponivel == 'on' else False
    try:
        with connection.cursor() as cursor:
            # Livro mais requisitado (mantém a query antiga)
            cursor.execute("SELECT livro_mais_requisitado();")
            livro_estrela = cursor.fetchone()[0]
            livro_estrela_exemplares = None
            if livro_estrela:
                cursor.execute("""
                    SELECT l.id_livro, l.titulo, l.isbn, l.stock, l.ano_publicacao,
                        c.nome as categoria, a.nome as autor, e.nome as editora
                    FROM Livros l
                    LEFT JOIN Categorias c ON l.id_categoria = c.id_categoria
                    LEFT JOIN Autores a ON l.id_autor = a.id_autor
                    LEFT JOIN Editoras e ON l.id_editora = e.id_editora
                    WHERE l.id_livro = %s
                    ORDER BY l.titulo;
                """, [livro_estrela])
                livro_estrela_obj = cursor.fetchone()
                cursor.execute("SELECT livros_disponiveis_por_livro(%s);", [livro_estrela])
                livro_estrela_exemplares = cursor.fetchone()[0]
            # Listagem de livros via função
            cursor.execute(
                "SELECT * FROM filtrar_livros(%s, %s, %s);",
                [nome_livro, disponivel_param, nao_disponivel_param]
            )
            livros = cursor.fetchall()
    except Exception as e:
        livros = []
        error = str(e).split('\n')[0]
    is_membro_var = is_membro(request.user.id)
    return render(request, 'livros/list.html', {
        'livros': livros,
        'is_membro': is_membro_var,
        'error': error,
        'livro_estrela_obj': livro_estrela_obj,
        'livro_estrela_exemplares': livro_estrela_exemplares,
        'nome_livro': nome_livro or '',
        'mostrar_disponivel': disponivel_param,
        'mostrar_indisponivel': nao_disponivel_param,
    })

@login_required
def livro_detail(request, pk):
    connection = get_db_connection_for_user(request.user)
    error = None
    livro = None
    exemplares_disponiveis = 0
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT l.id_livro, l.titulo, l.isbn, l.stock, l.ano_publicacao,
                       c.nome as categoria, a.nome as autor, e.nome as editora
                FROM Livros l
                LEFT JOIN Categorias c ON l.id_categoria = c.id_categoria
                LEFT JOIN Autores a ON l.id_autor = a.id_autor
                LEFT JOIN Editoras e ON l.id_editora = e.id_editora
                WHERE l.id_livro = %s;
            """, [pk])
            livro = cursor.fetchone()
            cursor.execute("SELECT livros_disponiveis_por_livro(%s);", [pk])
            exemplares_disponiveis = cursor.fetchone()[0]
    except Exception as e:
        error = str(e).split('\n')[0]
    return render(request, 'livros/detail.html', {
        'livro': livro,
        'error': error,
        'exemplares_disponiveis': exemplares_disponiveis,
    })

@login_required
def livro_create(request):
    if not is_bibliotecario_ou_admin(request.user.id):
        return render(request, '404.html', status=404)
    connection = get_db_connection_for_user(request.user)
    with connection.cursor() as cursor:
        cursor.execute("SELECT id_autor, nome FROM Autores ORDER BY nome;")
        autores = cursor.fetchall()
        cursor.execute("SELECT id_categoria, nome FROM Categorias ORDER BY nome;")
        categorias = cursor.fetchall()
        cursor.execute("SELECT id_editora, nome FROM Editoras ORDER BY nome;")
        editoras = cursor.fetchall()
    error = None
    form_data = {}
    if request.method == 'POST':
        form_data = request.POST
        titulo = form_data.get('titulo')
        isbn = form_data.get('isbn')
        stock = form_data.get('stock') or 1
        ano_publicacao = form_data.get('ano_publicacao') or None
        id_categoria = form_data.get('id_categoria') or None
        id_autor = form_data.get('id_autor') or None
        id_editora = form_data.get('id_editora') or None
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "CALL inserir_livro(%s, %s, %s, %s, %s, %s, %s);",
                    [titulo, isbn, stock, ano_publicacao, id_categoria, id_autor, id_editora]
                )
            return redirect('livros:livro_list')
        except DatabaseError as e:
            error = str(e).split('\n')[0]
    return render(request, 'livros/create.html', {
        'autores': autores,
        'categorias': categorias,
        'editoras': editoras,
        'error': error,
        'form_data': form_data,
    })

@login_required
def livro_update(request, pk):
    if not is_bibliotecario_ou_admin(request.user.id):
        return render(request, '404.html', status=404)
    connection = get_db_connection_for_user(request.user)
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id_livro, titulo, isbn, stock, ano_publicacao, id_categoria, id_autor, id_editora
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
    form_data = None
    if request.method == 'POST':
        form_data = request.POST
        titulo = form_data.get('titulo')
        isbn = form_data.get('isbn')
        stock = form_data.get('stock') or 1
        ano_publicacao = form_data.get('ano_publicacao') or None
        id_categoria = form_data.get('id_categoria') or None
        id_autor = form_data.get('id_autor') or None
        id_editora = form_data.get('id_editora') or None     
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "CALL atualizar_livro(%s, %s, %s, %s, %s, %s, %s, %s);",
                    [pk, titulo, isbn, stock, ano_publicacao, id_categoria, id_autor, id_editora]
                )
            return redirect('livros:livro_list')
        except DatabaseError as e:
            error = str(e).split('\n')[0]
    return render(request, 'livros/update.html', {
        'livro': livro,
        'autores': autores,
        'categorias': categorias,
        'editoras': editoras,
        'error': error,
        'form_data': form_data,
    })

@login_required
def livro_delete(request, pk):
    if not is_bibliotecario_ou_admin(request.user.id):
        return render(request, '404.html', status=404)
    connection = get_db_connection_for_user(request.user)
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