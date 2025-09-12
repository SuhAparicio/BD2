from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from utilizadores.mongo_utils import listar_utilizadores
from bson.objectid import ObjectId
from django.db import connection, DatabaseError


def is_bibliotecario_ou_admin(user):
    return (
        user.is_superuser or
        user.groups.filter(name='bibliotecario').exists() or
        user.groups.filter(name='admin').exists()
    )

@login_required
def requisicao_list(request):
    error = None
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT r.id_requisicao, r.id_livro, l.titulo, r.id_utilizador, r.data_requisicao,
                       r.data_devolucao_prevista, r.data_devolucao_real, r.estado
                FROM Requisicoes r
                JOIN Livros l ON r.id_livro = l.id_livro
                ORDER BY r.data_requisicao DESC;
            """)
            requisicoes = cursor.fetchall()
        # Buscar nomes dos utilizadores do Mongo
        utilizadores = {str(u['_id']): u['nome'] for u in listar_utilizadores()}
        # Adiciona o nome do utilizador a cada requisição
        requisicoes = [
            req + (utilizadores.get(req[3], 'Desconhecido'),)
            for req in requisicoes
        ]
    except Exception as e:
        requisicoes = []
        error = str(e).split('\n')[0]
    return render(request, 'requisicoes/list.html', {'requisicoes': requisicoes, 'error': error})

@login_required
def requisicao_detail(request, id_requisicao):
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
    if not is_bibliotecario_ou_admin(request.user):
        return render(request, '404.html', status=404)
    # Buscar livros disponíveis
    with connection.cursor() as cursor:
        cursor.execute("SELECT id_livro, titulo FROM Livros WHERE stock > 0;")
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
        cursor.execute("SELECT id_livro, titulo FROM Livros;")
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
                cursor.execute("CALL devolver_requisicao(%s);", [id_requisicao])
            return redirect('requisicoes:requisicao_list')
        except DatabaseError as e:
            error = str(e).split('\n')[0]
    return render(request, 'requisicoes/devolver.html', {
        'req': req,
        'utilizador_nome': utilizador_nome,
        'error': error,
    })