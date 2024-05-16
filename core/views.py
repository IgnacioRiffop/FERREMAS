from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User,Group
import requests


# Create your views here.
def index(request):
    return render(request,'core/index.html')

def nosotros(request):
    return render(request,'core/nosotros.html')

def administracion(request):
    return render(request,'core/administracion.html')

def crudUsuarios(request):
    return render(request,'core/crudUsuarios.html')

def crudClientes(request):
    return render(request,'core/crudClientes.html')

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

def contacto(request):
    return render(request,'core/contacto.html')

def perfil(request):
    return render(request,'core/perfil.html')

def formularioDespacho(request):
    return render(request,'core/formularioDespacho.html')

def producto(request):
    return render(request,'core/producto.html')

def detalleProducto(request):
    return render(request,'core/detalleProducto.html')

def carrito(request):
    return render(request,'core/carrito.html')


#views del API

def peticion_get(request):
    url = "http://127.0.0.1:5000/productos"
    productos = requests.get(url)
    for p in productos.json():
        print(p['id_producto'])
    return render(request,'core/index.html')

def peticion_get_producto(request, id_producto):
    url = f"http://127.0.0.1:5000/productos/{id_producto}"
    producto = requests.get(url)
    producto = producto.json()
    print(producto['nombre'])  # Puedes acceder a los atributos del producto si es necesario
    return render(request, 'core/index.html')




"""
def peticion_post():
    producto = {
        "id_producto" : 4
    }
    requests.post("http://127.0.0.1:5000/productos", producto)
"""