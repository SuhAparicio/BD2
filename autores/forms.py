from django import forms
from .models import Autor

class AutorForm(forms.ModelForm):
    class Meta:
        model = Autor
        fields = ['nome', 'data_nascimento']

    def __init__(self, *args, **kwargs):
        super(AutorForm, self).__init__(*args, **kwargs)
        self.fields['data_nascimento'].widget = forms.DateInput(attrs={'type': 'date'})