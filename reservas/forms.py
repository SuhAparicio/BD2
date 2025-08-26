from django import forms
from .models import Reserva

class ReservaForm(forms.ModelForm):
    utilizador_id = forms.ChoiceField(choices=[])

    class Meta:
        model = Reserva
        fields = ['livro', 'utilizador_id', 'data_retirada']