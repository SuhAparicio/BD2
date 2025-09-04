from django import forms
from .models import Reserva

class ReservaForm(forms.ModelForm):
    utilizador_id = forms.ChoiceField(choices=[])
    data_retirada = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=True
    )
    data_devolucao = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=True
    )

    class Meta:
        model = Reserva
        fields = ['livro', 'utilizador_id', 'data_retirada', 'data_devolucao']