# forms.py
from django import forms
from .models import Livro

class LivroForm(forms.ModelForm):
    class Meta:
        model = Livro
        fields = ['titulo', 'autor', 'categoria', 'isbn', 'data_publicacao', 'disponivel']
        widgets = {
            'data_publicacao': forms.DateInput(
                attrs={
                    'type': 'date',  # se quiser datetime picker: 'datetime-local'
                    'class': 'form-control'
                }
            ),
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'isbn': forms.TextInput(attrs={'class': 'form-control'}),
            'autor': forms.Select(attrs={'class': 'form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'disponivel': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
