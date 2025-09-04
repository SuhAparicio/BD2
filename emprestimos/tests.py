from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date
from livros.models import Livro, Autor, Categoria
from emprestimos.models import Emprestimo
from emprestimos.forms import EmprestimoForm
from unittest.mock import patch

# ================================
# Testes de Modelos de Empréstimos
# ================================
class EmprestimoModelTest(TestCase):
    def setUp(self):
        # Criar utilizador Django
        self.utilizador = User.objects.create_user(username='teste', password='12345')

        # Criar autor e categoria
        self.autor = Autor.objects.create(nome="Autor Teste")
        self.categoria = Categoria.objects.create(nome="Categoria Teste")

        # Criar livro
        self.livro = Livro.objects.create(
            titulo="Livro Teste",
            autor=self.autor,
            categoria=self.categoria,
            isbn="1234567890123",
            data_publicacao=date.today(),
            disponivel=True
        )

        # Criar empréstimo (simulando MongoDB ID como string)
        self.emprestimo = Emprestimo.objects.create(
            livro=self.livro,
            utilizador_id='12345',
            data_emprestimo=date.today()
        )

    def test_emprestimo_creation(self):
        self.assertEqual(self.emprestimo.livro, self.livro)
        self.assertEqual(self.emprestimo.utilizador_id, '12345')

    def test_emprestimo_delete_updates_livro_disponivel(self):
        self.emprestimo.delete()
        self.livro.refresh_from_db()
        self.assertTrue(self.livro.disponivel)

# =========================
# Testes de Formulários
# =========================
class EmprestimoFormTest(TestCase):
    def setUp(self):
        self.utilizador = User.objects.create_user(username='teste', password='12345')

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
        form = EmprestimoForm(data=form_data)
        form.fields['utilizador_id'].choices = [('12345', 'teste')]
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form_data = {
            'livro': '',
            'utilizador_id': '',
            'data_devolucao': ''
        }
        form = EmprestimoForm(data=form_data)
        form.fields['utilizador_id'].choices = [('12345', 'teste')]
        self.assertFalse(form.is_valid())

# =========================
# Testes de Views
# =========================
class EmprestimoViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.utilizador = User.objects.create_user(username='teste', password='12345')
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

        # Empréstimo simulado com MongoDB ID como string
        self.emprestimo = Emprestimo.objects.create(
            livro=self.livro,
            utilizador_id='12345',
            data_emprestimo=date.today()
        )

    def test_emprestimo_list_view(self):
        url = reverse('emprestimos:emprestimo_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.livro.titulo)

    @patch('emprestimos.views.listar_utilizadores')
    def test_emprestimo_detail_view(self, mock_listar):
        mock_listar.return_value = [{'_id': '12345', 'nome': 'teste'}]
        url = reverse('emprestimos:emprestimo_detail', args=[self.emprestimo.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.livro.titulo)

    @patch('emprestimos.views.listar_utilizadores')
    def test_emprestimo_create_view(self, mock_listar):
        mock_listar.return_value = [{'_id': '12345', 'nome': 'teste'}]
        url = reverse('emprestimos:emprestimo_create')
        data = {
            'livro': self.livro.id,
            'utilizador_id': '12345',
            'data_devolucao': date.today()
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Emprestimo.objects.filter(livro=self.livro).exists())

    @patch('emprestimos.views.listar_utilizadores')
    def test_emprestimo_update_view(self, mock_listar):
        mock_listar.return_value = [{'_id': '12345', 'nome': 'teste'}]
        url = reverse('emprestimos:emprestimo_update', args=[self.emprestimo.id])
        data = {
            'livro': self.livro.id,
            'utilizador_id': '12345',
            'data_devolucao': date.today()
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.emprestimo.refresh_from_db()
        self.assertEqual(self.emprestimo.livro, self.livro)

    @patch('emprestimos.views.listar_utilizadores')
    def test_emprestimo_delete_view(self, mock_listar):
        mock_listar.return_value = [{'_id': '12345', 'nome': 'teste'}]
        url = reverse('emprestimos:emprestimo_delete', args=[self.emprestimo.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Emprestimo.objects.filter(id=self.emprestimo.id).exists())
