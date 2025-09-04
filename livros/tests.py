from datetime import date
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from livros.models import Livro, Autor, Categoria
from livros.forms import LivroForm

class LivroModelTest(TestCase):
    def setUp(self):
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

    def test_livro_str_method(self):
        # Ajusta o teste para refletir a implementação atual do __str__
        self.assertEqual(str(self.livro), "Livro Teste por Autor Teste")

class LivroFormTest(TestCase):
    def setUp(self):
        self.autor = Autor.objects.create(nome="Autor Teste")
        self.categoria = Categoria.objects.create(nome="Categoria Teste")

    def test_valid_form(self):
        form_data = {
            "titulo": "Novo Livro",
            "autor": self.autor.id,
            "categoria": self.categoria.id,
            "isbn": "1234567890123",
            "data_publicacao": date.today(),
            "disponivel": True
        }
        form = LivroForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form_data = {"titulo": "", "autor": "", "categoria": ""}
        form = LivroForm(data=form_data)
        self.assertFalse(form.is_valid())

class LivroViewsTest(TestCase):
    def setUp(self):
        self.usuario = User.objects.create_user(username='teste', password='12345')
        self.client.force_login(self.usuario)

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

    def test_livro_list_view_logged_in(self):
        response = self.client.get(reverse('livros:livro_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.livro.titulo)

    def test_livro_detail_view(self):
        response = self.client.get(reverse('livros:livro_detail', args=[self.livro.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.livro.titulo)

    def test_livro_create_view(self):
        response = self.client.post(
            reverse('livros:livro_create'),
            data={
                "titulo": "Novo Livro",
                "autor": self.autor.id,
                "categoria": self.categoria.id,
                "isbn": "9876543210987",
                "data_publicacao": "2025-09-02",
                "disponivel": True
            }
        )
        self.assertEqual(response.status_code, 302)  # redireciona após criação
        self.assertTrue(Livro.objects.filter(titulo="Novo Livro").exists())

    def test_livro_update_view(self):
        response = self.client.post(
            reverse('livros:livro_update', args=[self.livro.id]),
            data={
                "titulo": "Livro Atualizado",
                "autor": self.autor.id,
                "categoria": self.categoria.id,
                "isbn": "1234567890123",
                "data_publicacao": "2025-09-02",
                "disponivel": True
            }
        )
        self.assertEqual(response.status_code, 302)
        self.livro.refresh_from_db()
        self.assertEqual(self.livro.titulo, "Livro Atualizado")

    def test_livro_delete_view(self):
        response = self.client.post(reverse('livros:livro_delete', args=[self.livro.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Livro.objects.filter(id=self.livro.id).exists())

    def test_redirect_if_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse('livros:livro_create'))
        self.assertEqual(response.status_code, 302)  # deve redirecionar para login
