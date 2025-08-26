from django import forms
from .models import Emprestimo

class EmprestimoForm(forms.ModelForm):
    utilizador_id = forms.ChoiceField(choices=[])  # choices definidos na view

    class Meta:
        model = Emprestimo
        fields = ['livro', 'utilizador_id', 'data_devolucao']