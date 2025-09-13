from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from utilizadores.forms import SignupForm
from utilizadores.mongo_utils import inserir_utilizador
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    return render(request, "index.html")

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            inserir_utilizador(
                nome=form.cleaned_data['nome'],
                contacto=form.cleaned_data['contacto'],
                django_user_id=user.id,
                role='membro'
            )
            return redirect('login')
    else:
        form = SignupForm()
    return render(request, 'registration/signup.html', {'form': form})