from django.db import models

class Autor(models.Model):
    nome = models.CharField(max_length=100)
    data_nascimento = models.DateField(null=True, blank=True)

    class Meta:
        db_table = 'autor'

    def __str__(self):
        return self.nome