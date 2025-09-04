from django.db import models
from livros.models import Livro

class Reserva(models.Model):
    livro = models.ForeignKey(Livro, on_delete=models.CASCADE)
    utilizador_id = models.CharField(max_length=24)
    data_reserva = models.DateField(auto_now_add=True)
    data_retirada = models.DateField(null=True, blank=True)
    data_devolucao = models.DateField(null=True, blank=True)
    concluida = models.BooleanField(default=False)

    class Meta:
        db_table = 'reserva'

    def __str__(self):
        return f"{self.livro} - Utilizador ID: {self.utilizador_id} (Concluída: {self.concluida})"