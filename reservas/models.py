from django.db import models
from livros.models import Livro
from utilizadores.models import UtilizadorBiblioteca

class Reserva(models.Model):
    livro = models.ForeignKey(Livro, on_delete=models.CASCADE)
    utilizador = models.ForeignKey(UtilizadorBiblioteca, on_delete=models.CASCADE)
    data_reserva = models.DateField(auto_now_add=True)
    data_retirada = models.DateField(null=True, blank=True)
    concluida = models.BooleanField(default=False)

    class Meta:
        db_table = 'reserva'

    def __str__(self):
        return f"{self.livro} - {self.utilizador.nome} (Concluída: {self.concluida})"