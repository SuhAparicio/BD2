from django.db import models
from django.contrib.auth.models import User

class UtilizadorBiblioteca(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    contacto = models.CharField(max_length=20, blank=True)
    numero_socio = models.CharField(max_length=10, unique=True)
    data_registo = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'utilizador_biblioteca'

    def __str__(self):
        return f"{self.nome} (Socio: {self.numero_socio})"