from django import forms
from .models import Emprestimo

class EmprestimoForm(forms.ModelForm):
    utilizador_id = forms.ChoiceField(choices=[])

    class Meta:
        model = Emprestimo
        fields = ['livro', 'utilizador_id', 'data_devolucao']
        widgets = {
            'data_devolucao': forms.DateInput(attrs={'type': 'date'}),
        }