from django.db import models
from livros.models import Livro
from django.contrib.auth.models import User  # Para associar utilizadores autenticados

class Emprestimo(models.Model):
    livro = models.ForeignKey(Livro, on_delete=models.CASCADE)
    utilizador = models.ForeignKey(User, on_delete=models.CASCADE)
    data_emprestimo = models.DateField(auto_now_add=True)
    data_devolucao = models.DateField(null=True, blank=True)
    devolvido = models.BooleanField(default=False)

    class Meta:
        db_table = 'emprestimo'

    def __str__(self):
        return f"{self.livro} - {self.utilizador} (Devolvido: {self.devolvido})"