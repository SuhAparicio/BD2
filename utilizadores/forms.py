from django import forms
from .models import UtilizadorBiblioteca

class UtilizadorForm(forms.ModelForm):
    class Meta:
        model = UtilizadorBiblioteca
        fields = ['nome', 'contacto', 'numero_socio']