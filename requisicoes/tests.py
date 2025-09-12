from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User, Group
from datetime import date
from livros.models import Livro, Autor, Categoria
from requisicoes.models import Requisicao
from requisicoes.forms import RequisicaoForm
from unittest.mock import patch

# Função utilitária para criar utilizador com permissões
def criar_utilizador_com_permissao():
    user = User.objects.create_user(username='teste', password='12345')
    grupo_admin, _ = Group.objects.get_or_create(name='admin')
    user.groups.add(grupo_admin)
    return user

# ================================
# Testes de Modelos de Empréstimos
# ================================
class EmprestimoModelTest(TestCase):
    def setUp(self):
        self.utilizador = criar_utilizador_com_permissao()
        self.autor = Autor.objects.create(nome="Autor Teste")
        self.categoria = Categoria.objects.create(nome="Categoria Teste")
        self.livro = Livro.objects.create(
            titulo="Livro Teste",
            autor=self.autor,
            categoria=self.categoria,
            isbn="1234567890123",
            data_publicacao=date.today(),
            disponivel=True
        )
        self.requisicao = Requisicao.objects.create(
            livro=self.livro,
            utilizador_id='12345',
            data_requisicao=date.today()
        )

    def test_requisicao_creation(self):
        self.assertEqual(self.requisicao.livro, self.livro)
        self.assertEqual(self.requisicao.utilizador_id, '12345')

    def test_requisicao_delete_updates_livro_disponivel(self):
        self.requisicao.delete()
        self.livro.refresh_from_db()
        self.assertTrue(self.livro.disponivel)

# =========================
# Testes de Formulários
# =========================
class EmprestimoFormTest(TestCase):
    def setUp(self):
        self.utilizador = criar_utilizador_com_permissao()
        self.autor = Autor.objects.create(nome="Autor Form Teste")
        self.categoria = Categoria.objects.create(nome="Categoria Form Teste")
        self.livro = Livro.objects.create(
            titulo="Livro Form Teste",
            autor=self.autor,
            categoria=self.categoria,
            isbn="9876543210123",
            data_publicacao=date.today(),
            disponivel=True
        )

    def test_valid_form(self):
        form_data = {
            'livro': self.livro.id,
            'utilizador_id': '12345',
            'data_devolucao': date.today()
        }
        form = RequisicaoForm(data=form_data)
        form.fields['utilizador_id'].choices = [('12345', 'teste')]
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form_data = {
            'livro': '',
            'utilizador_id': '',
            'data_devolucao': ''
        }
        form = RequisicaoForm(data=form_data)
        form.fields['utilizador_id'].choices = [('12345', 'teste')]
        self.assertFalse(form.is_valid())

# =========================
# Testes de Views
# =========================
class EmprestimoViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.utilizador = criar_utilizador_com_permissao()
        self.client.login(username='teste', password='12345')

        self.autor = Autor.objects.create(nome="Autor View Teste")
        self.categoria = Categoria.objects.create(nome="Categoria View Teste")
        self.livro = Livro.objects.create(
            titulo="Livro Teste",
            autor=self.autor,
            categoria=self.categoria,
            isbn="1234567890123",
            data_publicacao=date.today(),
            disponivel=True
        )

        self.requisicao = Requisicao.objects.create(
            livro=self.livro,
            utilizador_id='12345',
            data_requisicao=date.today()
        )

    def test_requisicao_list_view(self):
        url = reverse('requisicoes:requisicao_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.livro.titulo)

    @patch('requisicoes.views.listar_utilizadores')
    def test_requisicao_detail_view(self, mock_listar):
        mock_listar.return_value = [{'_id': '12345', 'nome': 'teste'}]
        url = reverse('requisicoes:requisicao_detail', args=[self.requisicao.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.livro.titulo)

    @patch('requisicoes.views.listar_utilizadores')
    def test_requisicao_create_view(self, mock_listar):
        mock_listar.return_value = [{'_id': '12345', 'nome': 'teste'}]
        url = reverse('requisicoes:requisicao_create')
        data = {
            'livro': self.livro.id,
            'utilizador_id': '12345',
            'data_devolucao': date.today()
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Requisicao.objects.filter(livro=self.livro).exists())

    @patch('requisicoes.views.listar_utilizadores')
    def test_requisicao_update_view(self, mock_listar):
        mock_listar.return_value = [{'_id': '12345', 'nome': 'teste'}]
        url = reverse('requisicoes:requisicao_update', args=[self.requisicao.id])
        data = {
            'livro': self.livro.id,
            'utilizador_id': '12345',
            'data_devolucao': date.today()
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.requisicao.refresh_from_db()
        self.assertEqual(self.requisicao.livro, self.livro)

    @patch('requisicoes.views.listar_utilizadores')
    def test_requisicao_delete_view(self, mock_listar):
        mock_listar.return_value = [{'_id': '12345', 'nome': 'teste'}]
        url = reverse('requisicoes:requisicao_delete', args=[self.requisicao.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Requisicao.objects.filter(id=self.requisicao.id).exists())
