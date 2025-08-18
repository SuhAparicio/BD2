from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import ReservaForm
from .models import Reserva

@login_required
def reserva_list(request):
    try:
        reservas = Reserva.objects.all()
        return render(request, 'reservas/list.html', {'reservas': reservas})
    except Exception as e:
        print(f"Erro na view reserva_list: {e}")
        return render(request, 'reservas/list.html', {'error': str(e)})

@login_required
def reserva_detail(request, pk):
    try:
        reserva = get_object_or_404(Reserva, pk=pk)
        return render(request, 'reservas/detail.html', {'reserva': reserva})
    except Exception as e:
        print(f"Erro na view reserva_detail: {e}")
        return render(request, 'reservas/detail.html', {'error': str(e)})

@login_required
def reserva_create(request):
    try:
        if request.method == 'POST':
            form = ReservaForm(request.POST)
            if form.is_valid():
                reserva = form.save(commit=False)
                if reserva.data_retirada:
                    reserva.livro.disponivel = False
                    reserva.livro.save()
                reserva.save()
                return redirect('reservas:reserva_list')
        else:
            form = ReservaForm()
        return render(request, 'reservas/create.html', {'form': form})
    except Exception as e:
        print(f"Erro na view reserva_create: {e}")
        return render(request, 'reservas/create.html', {'form': form, 'error': str(e)})

@login_required
def reserva_update(request, pk):
    try:
        reserva = get_object_or_404(Reserva, pk=pk)
        if request.method == 'POST':
            form = ReservaForm(request.POST, instance=reserva)
            if form.is_valid():
                reserva_anterior = Reserva.objects.get(pk=pk)
                reserva = form.save()
                if reserva.data_retirada and not reserva_anterior.data_retirada:
                    reserva.livro.disponivel = False
                    reserva.livro.save()
                return redirect('reservas:reserva_list')
        else:
            form = ReservaForm(instance=reserva)
        return render(request, 'reservas/update.html', {'form': form})
    except Exception as e:
        print(f"Erro na view reserva_update: {e}")
        return render(request, 'reservas/update.html', {'form': form, 'error': str(e)})

@login_required
def reserva_delete(request, pk):
    try:
        reserva = get_object_or_404(Reserva, pk=pk)
        if request.method == 'POST':
            if not reserva.concluida:
                reserva.livro.disponivel = True
                reserva.livro.save()
            reserva.delete()
            return redirect('reservas:reserva_list')
        return render(request, 'reservas/delete.html', {'reserva': reserva})
    except Exception as e:
        print(f"Erro na view reserva_delete: {e}")
        return render(request, 'reservas/delete.html', {'reserva': reserva, 'error': str(e)})