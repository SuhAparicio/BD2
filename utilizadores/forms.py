from django import forms

class UtilizadorForm(forms.Form):
    nome = forms.CharField(max_length=100)
    contacto = forms.CharField(max_length=20, required=False)
    numero_socio = forms.CharField(max_length=10)