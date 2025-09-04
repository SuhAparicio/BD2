from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User, Group
from .models import Categoria
from .forms import CategoriaForm


def criar_utilizador_com_permissao():
    """Cria um utilizador com permissões de admin (grupo) para os testes."""
    user = User.objects.create_user(username='testuser', password='testpass')
    grupo_admin, _ = Group.objects.get_or_create(name='admin')
    user.groups.add(grupo_admin)
    return user


class CategoriaModelTest(TestCase):
    def setUp(self):
        self.categoria = Categoria.objects.create(nome="Categoria Inicial")

    def test_categoria_creation(self):
        """Verifica se a categoria é criada corretamente."""
        self.assertEqual(self.categoria.nome, "Categoria Inicial")
        self.assertIsInstance(self.categoria, Categoria)

    def test_categoria_str_method(self):
        """Verifica se o método __str__ retorna o nome da categoria."""
        self.assertEqual(str(self.categoria), "Categoria Inicial")

    def test_categoria_update(self):
        """Verifica se é possível atualizar a categoria."""
        self.categoria.nome = "Categoria Atualizada"
        self.categoria.save()
        self.assertEqual(Categoria.objects.get(pk=self.categoria.pk).nome, "Categoria Atualizada")

    def test_categoria_delete(self):
        """Verifica se a categoria pode ser eliminada."""
        pk = self.categoria.pk
        self.categoria.delete()
        self.assertFalse(Categoria.objects.filter(pk=pk).exists())


class CategoriaFormTest(TestCase):
    def test_valid_form(self):
        """Verifica se o formulário é válido com dados corretos."""
        form = CategoriaForm(data={'nome': 'Nova Categoria'})
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        """Verifica se o formulário é inválido quando campos obrigatórios estão em falta."""
        form = CategoriaForm(data={})  # sem nome
        self.assertFalse(form.is_valid())
        self.assertIn('nome', form.errors)


class CategoriaViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = criar_utilizador_com_permissao()
        self.categoria = Categoria.objects.create(nome="Categoria Teste")

    def test_redirect_if_not_logged_in(self):
        """Verifica se utilizador não autenticado é redirecionado para login."""
        response = self.client.get(reverse('categorias:categoria_list'))
        self.assertRedirects(response, '/login/?next=' + reverse('categorias:categoria_list'))

    def test_categoria_list_view_logged_in(self):
        """Testa listagem de categorias com login efetuado."""
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('categorias:categoria_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'categorias/list.html')
        self.assertContains(response, self.categoria.nome)

    def test_categoria_detail_view(self):
        """Testa página de detalhe de uma categoria."""
        self.client.login(username='testuser', password='testpass')
        url = reverse('categorias:categoria_detail', args=[self.categoria.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'categorias/detail.html')
        self.assertContains(response, self.categoria.nome)

    def test_categoria_create_view(self):
        """Testa criação de uma nova categoria via POST."""
        self.client.login(username='testuser', password='testpass')
        url = reverse('categorias:categoria_create')
        data = {'nome': 'Nova Categoria'}
        response = self.client.post(url, data, follow=True)
        self.assertRedirects(response, reverse('categorias:categoria_list'))
        self.assertTrue(Categoria.objects.filter(nome='Nova Categoria').exists())

    def test_categoria_update_view(self):
        """Testa atualização de uma categoria existente."""
        self.client.login(username='testuser', password='testpass')
        url = reverse('categorias:categoria_update', args=[self.categoria.pk])
        data = {'nome': 'Categoria Atualizada'}
        response = self.client.post(url, data, follow=True)
        self.assertRedirects(response, reverse('categorias:categoria_list'))
        self.categoria.refresh_from_db()
        self.assertEqual(self.categoria.nome, 'Categoria Atualizada')

    def test_categoria_delete_view(self):
        """Testa eliminação de uma categoria existente."""
        self.client.login(username='testuser', password='testpass')
        url = reverse('categorias:categoria_delete', args=[self.categoria.pk])
        response = self.client.post(url, follow=True)
        self.assertRedirects(response, reverse('categorias:categoria_list'))
        self.assertFalse(Categoria.objects.filter(pk=self.categoria.pk).exists())
