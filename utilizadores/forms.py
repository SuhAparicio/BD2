import re
from django import forms
from django.contrib.auth.models import User

class UtilizadorCreateForm(forms.Form):
    nome = forms.CharField(max_length=100)
    contacto = forms.CharField(max_length=20, required=False)
    username = forms.CharField(max_length=150)
    password = forms.CharField(max_length=128, widget=forms.PasswordInput, required=True)
    role = forms.ChoiceField(choices=[('admin', 'Admin'), ('bibliotecario', 'Bibliotecario'), ('membro', 'Membro')])

    def clean_username(self):
        username = self.cleaned_data['username']
        if self.user_instance and username != self.user_instance.username:
            if User.objects.filter(username=username).exists():
                raise forms.ValidationError("Já existe um utilizador com esse username.")
        return username

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise forms.ValidationError("A password deve ter pelo menos 8 caracteres.")
        if not re.search(r'[A-Z]', password):
            raise forms.ValidationError("A password deve conter pelo menos uma letra maiúscula.")
        if not re.search(r'[a-z]', password):
            raise forms.ValidationError("A password deve conter pelo menos uma letra minúscula.")
        if not re.search(r'\d', password):
            raise forms.ValidationError("A password deve conter pelo menos um número.")
        if not re.search(r'[!@#$%^&*()\-\_=+\[\]{};:,.<>?]', password):
            raise forms.ValidationError("A password deve conter pelo menos um símbolo especial: !@#$%^&*()-_=+[]{};:,.<>?")
        return password

class UtilizadorUpdateForm(forms.Form):
    nome = forms.CharField(max_length=100)
    contacto = forms.CharField(max_length=20, required=False)
    username = forms.CharField(max_length=150)
    password = forms.CharField(max_length=128, widget=forms.PasswordInput, required=False)
    role = forms.ChoiceField(choices=[('admin', 'Admin'), ('bibliotecario', 'Bibliotecario'), ('membro', 'Membro')])

    def __init__(self, *args, **kwargs):
        self.user_instance = kwargs.pop('user_instance', None)
        super().__init__(*args, **kwargs)

    def clean_username(self):
        username = self.cleaned_data['username']
        if self.user_instance and username != self.user_instance.username:
            if User.objects.filter(username=username).exists():
                raise forms.ValidationError("Já existe um utilizador com esse username.")
        return username

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if password:  # Só valida se o campo não estiver vazio
            if len(password) < 8:
                raise forms.ValidationError("A password deve ter pelo menos 8 caracteres.")
            if not re.search(r'[A-Z]', password):
                raise forms.ValidationError("A password deve conter pelo menos uma letra maiúscula.")
            if not re.search(r'[a-z]', password):
                raise forms.ValidationError("A password deve conter pelo menos uma letra minúscula.")
            if not re.search(r'\d', password):
                raise forms.ValidationError("A password deve conter pelo menos um número.")
            if not re.search(r'[!@#$%^&*()\-\_=+\[\]{};:,.<>?]', password):
                raise forms.ValidationError("A password deve conter pelo menos um símbolo especial: !@#$%^&*()-_=+[]{};:,.<>?")
        return password

class SignupForm(forms.Form):
    nome = forms.CharField(max_length=100)
    contacto = forms.CharField(max_length=20, required=False)
    username = forms.CharField(max_length=150)
    password = forms.CharField(max_length=128, widget=forms.PasswordInput, required=True)

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Já existe um utilizador com esse username.")
        return username

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if password:  # Só valida se o campo não estiver vazio
            if len(password) < 8:
                raise forms.ValidationError("A password deve ter pelo menos 8 caracteres.")
            if not re.search(r'[A-Z]', password):
                raise forms.ValidationError("A password deve conter pelo menos uma letra maiúscula.")
            if not re.search(r'[a-z]', password):
                raise forms.ValidationError("A password deve conter pelo menos uma letra minúscula.")
            if not re.search(r'\d', password):
                raise forms.ValidationError("A password deve conter pelo menos um número.")
            if not re.search(r'[!@#$%^&*()\-\_=+\[\]{};:,.<>?]', password):
                raise forms.ValidationError("A password deve conter pelo menos um símbolo especial: !@#$%^&*()-_=+[]{};:,.<>?")
        return password
