from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Autor
from .forms import AutorForm


class AutorModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client = Client()
        self.autor = Autor.objects.create(nome="Autor Teste")
        self.client.login(username='admin', password='admin')

    def test_autor_creation(self):
        """Verifica se o autor é criado corretamente."""
        self.assertEqual(self.autor.nome, "Autor Inicial")
        self.assertIsInstance(self.autor, Autor)

    def test_autor_str_method(self):
        """Verifica se o método __str__ retorna o nome do autor."""
        self.assertEqual(str(self.autor), "Autor Inicial")

    def test_autor_update(self):
        """Verifica se é possível atualizar o autor."""
        self.autor.nome = "Autor Atualizado"
        self.autor.save()
        self.assertEqual(Autor.objects.get(pk=self.autor.pk).nome, "Autor Atualizado")

    def test_autor_delete(self):
        """Verifica se o autor pode ser eliminado."""
        pk = self.autor.pk
        self.autor.delete()
        self.assertFalse(Autor.objects.filter(pk=pk).exists())


class AutorFormTest(TestCase):
    def test_valid_form(self):
        """Verifica se o formulário é válido com dados corretos."""
        form = AutorForm(data={'nome': 'Novo Autor'})
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        """Verifica se o formulário é inválido quando campos obrigatórios estão em falta."""
        form = AutorForm(data={})  # sem nome
        self.assertFalse(form.is_valid())
        self.assertIn('nome', form.errors)


class AutorViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client = Client()
        self.autor = Autor.objects.create(nome="Autor Teste")

    def test_redirect_if_not_logged_in(self):
        """Verifica se utilizador não autenticado é redirecionado para login."""
        response = self.client.get(reverse('autores:autor_list'))
        self.assertRedirects(response, '/login/?next=' + reverse('autores:autor_list'))

    def test_autor_list_view_logged_in(self):
        """Testa listagem de autores com login efetuado."""
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('autores:autor_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'autores/list.html')
        self.assertContains(response, self.autor.nome)

    def test_autor_detail_view(self):
        """Testa página de detalhe de um autor."""
        self.client.login(username='testuser', password='testpass')
        url = reverse('autores:autor_detail', args=[self.autor.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'autores/detail.html')
        self.assertContains(response, self.autor.nome)

    def test_autor_create_view(self):
        """Testa criação de um novo autor via POST."""
        self.client.login(username='testuser', password='testpass')
        url = reverse('autores:autor_create')
        data = {'nome': 'Novo Autor'}
        response = self.client.post(url, data, follow=True)
        self.assertRedirects(response, reverse('autores:autor_list'))
        self.assertTrue(Autor.objects.filter(nome='Novo Autor').exists())

    def test_autor_update_view(self):
        """Testa atualização de um autor existente."""
        self.client.login(username='testuser', password='testpass')
        url = reverse('autores:autor_update', args=[self.autor.pk])
        data = {'nome': 'Autor Atualizado'}
        response = self.client.post(url, data, follow=True)
        self.assertRedirects(response, reverse('autores:autor_list'))
        self.autor.refresh_from_db()
        self.assertEqual(self.autor.nome, 'Autor Atualizado')

    def test_autor_delete_view(self):
        """Testa eliminação de um autor existente."""
        self.client.login(username='testuser', password='testpass')
        url = reverse('autores:autor_delete', args=[self.autor.pk])
        response = self.client.post(url, follow=True)
        self.assertRedirects(response, reverse('autores:autor_list'))
        self.assertFalse(Autor.objects.filter(pk=self.autor.pk).exists())
