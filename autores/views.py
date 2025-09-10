from django.shortcuts import render, redirect
from django.db import connection
from django.contrib.auth.decorators import login_required

def is_bibliotecario_ou_admin(user):
    return (
        user.is_superuser or
        user.groups.filter(name='bibliotecario').exists() or
        user.groups.filter(name='admin').exists()
    )

@login_required
def autor_list(request):
    if not is_bibliotecario_ou_admin(request.user):
        return render(request, '404.html', status=404)
    with connection.cursor() as cursor:
        cursor.execute("SELECT id_autor, nome, data_nascimento, nacionalidade FROM Autores ORDER BY nome;")
        autores = cursor.fetchall()
    # autores = [(id_autor, nome, data_nascimento, nacionalidade), ...]
    return render(request, 'autores/list.html', {'autores': autores})

@login_required
def autor_detail(request, pk):
    if not is_bibliotecario_ou_admin(request.user):
        return render(request, '404.html', status=404)
    with connection.cursor() as cursor:
        cursor.execute("SELECT id_autor, nome, data_nascimento, nacionalidade FROM Autores WHERE id_autor = %s;", [pk])
        autor = cursor.fetchone()
    return render(request, 'autores/detail.html', {'autor': autor})

@login_required
def autor_create(request):
    if not is_bibliotecario_ou_admin(request.user):
        return render(request, '404.html', status=404)
    if request.method == 'POST':
        nome = request.POST.get('nome')
        data_nascimento = request.POST.get('data_nascimento') or None
        nacionalidade = request.POST.get('nacionalidade')
        with connection.cursor() as cursor:
            cursor.execute("CALL inserir_autor(%s, %s, %s);", [nome, data_nascimento, nacionalidade])
        return redirect('autores:autor_list')
    return render(request, 'autores/create.html')

@login_required
def autor_update(request, pk):
    if not is_bibliotecario_ou_admin(request.user):
        return render(request, '404.html', status=404)
    with connection.cursor() as cursor:
        cursor.execute("SELECT id_autor, nome, data_nascimento, nacionalidade FROM Autores WHERE id_autor = %s;", [pk])
        autor = cursor.fetchone()
    if request.method == 'POST':
        nome = request.POST.get('nome')
        data_nascimento = request.POST.get('data_nascimento') or None
        nacionalidade = request.POST.get('nacionalidade')
        with connection.cursor() as cursor:
            cursor.execute("CALL atualizar_autor(%s, %s, %s, %s);", [pk, nome, data_nascimento, nacionalidade])
        return redirect('autores:autor_list')
    return render(request, 'autores/update.html', {
        'autor': autor,
        'nome': autor[1] if autor else '',
        'data_nascimento': autor[2] if autor else '',
        'nacionalidade': autor[3] if autor else '',
    })

@login_required
def autor_delete(request, pk):
    if not is_bibliotecario_ou_admin(request.user):
        return render(request, '404.html', status=404)
    with connection.cursor() as cursor:
        cursor.execute("SELECT id_autor, nome FROM Autores WHERE id_autor = %s;", [pk])
        autor = cursor.fetchone()
    if request.method == 'POST':
        with connection.cursor() as cursor:
            cursor.execute("CALL eliminar_autor(%s);", [pk])
        return redirect('autores:autor_list')
    return render(request, 'autores/delete.html', {'autor': autor})