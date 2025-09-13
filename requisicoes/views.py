from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from utilizadores.mongo_utils import listar_utilizadores
from django.db import connections, DatabaseError


from utilizadores.mongo_utils import is_admin, is_bibliotecario, is_membro, get_userid_by_django_id

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
def requisicao_list(request):
    connection = get_db_connection_for_user(request.user)
    error = None
    titulo_livro = request.GET.get('titulo_livro') or None
    id_utilizador = request.GET.get('id_utilizador') or None
    is_membro_var = is_membro(request.user.id)

    # Por default, ambos True
    ativa_param = True
    nao_mostrar_ativas_param = True

    if request.GET:
        ativa_param = True if request.GET.get('ativa') == 'on' else False
        nao_mostrar_ativas_param = True if request.GET.get('mostrar_inativas') == 'on' else False

    if is_membro_var:
        # Filtra sempre pelo id do utilizador logado
        id_utilizador = get_userid_by_django_id(request.user.id)  # ou request.user.id, conforme o que tens no Mongo

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM filtrar_requisicoes(%s, %s, %s, %s);",
                [titulo_livro, id_utilizador, ativa_param, nao_mostrar_ativas_param]
            )
            requisicoes = cursor.fetchall()
        utilizadores = {str(u['_id']): u['nome'] for u in listar_utilizadores()}
        requisicoes = [
            req + (utilizadores.get(req[2], 'Desconhecido'),)
            for req in requisicoes
        ]
    except Exception as e:
        requisicoes = []
        error = str(e).split('\n')[0]

    opcoes_utilizador = [(str(u['_id']), u['nome']) for u in listar_utilizadores()]

    return render(request, 'requisicoes/list.html', {
        'requisicoes': requisicoes,
        'error': error,
        'titulo_livro': titulo_livro or '',
        'id_utilizador': id_utilizador or '',
        'ativa': ativa_param,
        'mostrar_inativas': nao_mostrar_ativas_param,
        'opcoes_utilizador': opcoes_utilizador,
        'is_membro': is_membro_var,
    })

@login_required
def requisicao_detail(request, id_requisicao):
    connection = get_db_connection_for_user(request.user)
    error = None
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT r.id_requisicao, l.titulo, r.id_utilizador, r.data_requisicao,
                   r.data_devolucao_prevista, r.data_devolucao_real, r.estado
            FROM Requisicoes r
            JOIN Livros l ON r.id_livro = l.id_livro
            WHERE r.id_requisicao = %s;
        """, [id_requisicao])
        req = cursor.fetchone()
    utilizador_nome = 'Desconhecido'
    if req:
        utilizadores = {str(u['_id']): u['nome'] for u in listar_utilizadores()}
        utilizador_nome = utilizadores.get(req[2], 'Desconhecido')
        return render(request, 'requisicoes/detail.html', {
            'req': req,
            'utilizador_nome': utilizador_nome,
            'error': error,
        })
    else:
        # Mostra página de erro amigável ou redireciona
        return render(request, '404.html', status=404)

@login_required
def requisicao_create(request):
    if is_membro(request.user.id):
        return render(request, '404.html', status=404)
    connection = get_db_connection_for_user(request.user)
    # Buscar livros disponíveis
    with connection.cursor() as cursor:
        cursor.execute("SELECT id_livro, titulo, stock, exemplares_disponiveis FROM livros_disponiveis_requisicao();")
        livros = cursor.fetchall()
    # Buscar utilizadores do Mongo
    utilizadores = listar_utilizadores()
    opcoes_utilizador = [(str(u['_id']), u['nome']) for u in utilizadores]
    error = None
    if request.method == 'POST':
        id_livro = request.POST.get('id_livro')
        id_utilizador = request.POST.get('id_utilizador')
        data_devolucao_prevista = request.POST.get('data_devolucao_prevista')
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "CALL inserir_requisicao(%s, %s, %s);",
                    [id_livro, id_utilizador, data_devolucao_prevista]
                )
            return redirect('requisicoes:requisicao_list')
        except DatabaseError as e:
            error = str(e).split('\n')[0]
    return render(request, 'requisicoes/create.html', {
        'livros': livros,
        'utilizadores': opcoes_utilizador,
        'error': error,
    })

@login_required
def requisicao_update(request, id_requisicao):
    if is_membro(request.user.id):
        return render(request, '404.html', status=404)
    connection = get_db_connection_for_user(request.user)
    error = None
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT r.id_requisicao, r.id_livro, r.id_utilizador, r.data_devolucao_prevista, r.estado
            FROM Requisicoes r
            WHERE r.id_requisicao = %s;
        """, [id_requisicao])
        req = cursor.fetchone()
    if not req or req[4] == "Devolvido":
        return redirect('requisicoes:requisicao_list')
    # Buscar livros e utilizadores
    with connection.cursor() as cursor:
        cursor.execute("SELECT id_livro, titulo, stock, exemplares_disponiveis FROM livros_disponiveis_requisicao();")
        livros = cursor.fetchall()
    utilizadores = listar_utilizadores()
    opcoes_utilizador = [(str(u['_id']), u['nome']) for u in utilizadores]
    if request.method == 'POST':
        id_livro = request.POST.get('id_livro')
        id_utilizador = request.POST.get('id_utilizador')
        data_devolucao_prevista = request.POST.get('data_devolucao_prevista')
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "CALL atualizar_requisicao(%s, %s, %s, %s);",
                    [id_requisicao, id_livro, id_utilizador, data_devolucao_prevista]
                )
            return redirect('requisicoes:requisicao_list')
        except DatabaseError as e:
            error = str(e).split('\n')[0]
    return render(request, 'requisicoes/update.html', {
        'req': req,
        'livros': livros,
        'utilizadores': opcoes_utilizador,
        'error': error,
    })

@login_required
def requisicao_delete(request, id_requisicao):
    if is_membro(request.user.id):
        return render(request, '404.html', status=404)
    connection = get_db_connection_for_user(request.user)
    error = None
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT r.id_requisicao, l.titulo, r.id_utilizador
            FROM Requisicoes r
            JOIN Livros l ON r.id_livro = l.id_livro
            WHERE r.id_requisicao = %s;
        """, [id_requisicao])
        req = cursor.fetchone()
    utilizador_nome = 'Desconhecido'
    if req:
        utilizadores = {str(u['_id']): u['nome'] for u in listar_utilizadores()}
        utilizador_nome = utilizadores.get(req[2], 'Desconhecido')
    if request.method == 'POST':
        try:
            with connection.cursor() as cursor:
                cursor.execute("CALL eliminar_requisicao(%s);", [id_requisicao])
            return redirect('requisicoes:requisicao_list')
        except DatabaseError as e:
            error = str(e).split('\n')[0]
    return render(request, 'requisicoes/delete.html', {
        'req': req,
        'utilizador_nome': utilizador_nome,
        'error': error,
    })

@login_required
def requisicao_devolver(request, id_requisicao):
    if is_membro(request.user.id):
        return render(request, '404.html', status=404)
    connection = get_db_connection_for_user(request.user)
    error = None
    # Buscar dados da requisição
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT r.id_requisicao, l.titulo, r.id_utilizador, r.estado
            FROM Requisicoes r
            JOIN Livros l ON r.id_livro = l.id_livro
            WHERE r.id_requisicao = %s;
        """, [id_requisicao])
        req = cursor.fetchone()
    utilizador_nome = 'Desconhecido'
    if req:
        utilizadores = {str(u['_id']): u['nome'] for u in listar_utilizadores()}
        utilizador_nome = utilizadores.get(req[2], 'Desconhecido')
    if request.method == 'POST':
        try:
            with connection.cursor() as cursor:
                cursor.execute("CALL marcar_requisicao_devolvida(%s);", [id_requisicao])
            return redirect('requisicoes:requisicao_list')
        except DatabaseError as e:
            error = str(e).split('\n')[0]
    return render(request, 'requisicoes/devolver.html', {
        'req': req,
        'utilizador_nome': utilizador_nome,
        'error': error,
    })