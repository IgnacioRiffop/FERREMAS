from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User,Group
import json
import requests
from django.core.paginator import Paginator



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
    url = "http://127.0.0.1:5000/productos"
    productos = requests.get(url).json()

    respuesta = requests.get('https://mindicador.cl/api/dolar').json()
    valor_usd = respuesta['serie'][0]['valor']

    for producto in productos:
        producto['preciousd'] = producto['precio']/valor_usd

    page = request.GET.get('page', 1) # OBTENEMOS LA VARIABLE DE LA URL, SI NO EXISTE NADA DEVUELVE 1
    
    try:
        paginator = Paginator(productos, 9)
        productos = paginator.page(page)
    except:
        raise Http404

    data = {
        'listado': productos,
        'paginator': paginator,
        'valorusd' : valor_usd
    }
    
    # Renderiza el template 'productos.html' y pasa la lista de productos como contexto
    return render(request, 'core/producto.html', data)


def detalleProducto(request):
    return render(request,'core/detalleProducto.html')

def carrito(request):
    return render(request,'core/carrito.html')

def datosTransferencia(request):
    return render(request,'core/datosTransferencia.html')

def misPedidos(request):
    return render(request,'core/misPedidos.html')

def bodega(request):
    return render(request,'core/bodega.html')

def formularioDespacho(request):
    return render(request,'core/formularioDespacho.html')

#CRUD
     #AGREGAR
def agregarBodeguero(request):
    return render(request,'core/agregarBodeguero.html')
def agregarContador(request):
    return render(request,'core/agregarContador.html')
def agregarProducto(request):
    return render(request,'core/agregarProducto.html')
def agregarVendedor(request):
    return render(request,'core/agregarVendedor.html')

    #MODIFICAR
def modificarBodeguero(request):
    return render(request,'core/modificarBodeguero.html')
def modificarContador(request):
    return render(request,'core/modificarContador.html')
def modificarProducto(request):
    return render(request,'core/modificarProducto.html')
def modificarVendedor(request):
    return render(request,'core/modificarVendedor.html')




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


def peticion_post(request):
    producto = {
        "id_producto": 4,
        "nombre": "Pintura",
        "id_marca": 1,
        "nombre_marca": "bosch",
        "precio": 10000,
        "stock": 6
    }
    url = "http://127.0.0.1:5000/productos"
    headers = {'Content-Type': 'application/json'}  # Especifica el tipo de contenido JSON
    
    # Convierte el diccionario producto a JSON y realiza la solicitud POST
    response = requests.post(url, data=json.dumps(producto), headers=headers)
    
    return render(request, 'core/index.html')


def peticion_put(request, id_producto):
    # Datos del producto actualizado
    producto_actualizado = {
        "nombre": "Pintura metalica",
        "id_marca": 1,
        "nombre_marca": "bosch",
        "precio": 15000,
        "stock": 10
    }
    
    url = f"http://127.0.0.1:5000/productos/{id_producto}"
    headers = {'Content-Type': 'application/json'}  # Especifica el tipo de contenido JSON
    
    # Convierte el diccionario producto_actualizado a JSON y realiza la solicitud PUT
    response = requests.put(url, data=json.dumps(producto_actualizado), headers=headers)
    
    return render(request, 'core/index.html')


def peticion_delete(request, id_producto):
    url = f"http://127.0.0.1:5000/productos/{id_producto}"
    
    # Realiza la solicitud DELETE
    response = requests.delete(url)
    
    if response.status_code == 200:
        # Si la solicitud DELETE se realizó con éxito, muestra un mensaje de éxito
        print("Producto eliminado correctamente")
    else:
        # Si la solicitud DELETE no se realizó con éxito, muestra un mensaje de error
        print("Error al eliminar el producto")
    
    return render(request, 'core/index.html')


def peticion_patch(request, id_producto):
    # Datos del producto actualizado
    producto_actualizado = {
        "nombre": "Escalera",
        "id_marca": 1,
        "nombre_marca": "bosch",
        "precio": 200000,
        "stock": 8
    }
    
    url = f"http://127.0.0.1:5000/productos/{id_producto}"
    headers = {'Content-Type': 'application/json'}  # Especifica el tipo de contenido JSON
    
    # Convierte el diccionario producto_actualizado a JSON y realiza la solicitud PATCH
    response = requests.patch(url, data=json.dumps(producto_actualizado), headers=headers)
    
    return render(request, 'core/index.html')
