from django.db import models
from autores.models import Autor
from categorias.models import Categoria

class Livro(models.Model):
    titulo = models.CharField(max_length=200)
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    isbn = models.CharField(max_length=13, unique=True)
    data_publicacao = models.DateField(null=True, blank=True)
    disponivel = models.BooleanField(default=True)

    class Meta:
        db_table = 'livro'

    def __str__(self):
        return f"{self.titulo} por {self.autor}" 