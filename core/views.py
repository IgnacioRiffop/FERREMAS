from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User,Group


# Create your views here.
def index(request):
    return render(request,'core/index.html')

def nosotros(request):
    return render(request,'core/nosotros.html')

def registro(request):
    data = {
        'form': RegistroForm()
    }

    if request.method == 'POST':
        formulario = RegistroForm(data=request.POST) # OBTIENE LA DATA DEL FORMULARIO
        if formulario.is_valid():
            formulario.save()
            user = authenticate(username = formulario.cleaned_data["username"], password = formulario.cleaned_data["password1"])
            login(request, user)
            grupo = Group.objects.get(name='cliente')
            user.groups.add(grupo)
            #redirigir al home
            return redirect(to="index")
        data["form"]=formulario
    return render(request, 'core/registro.html', data)