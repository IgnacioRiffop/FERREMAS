from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User,Group
import json
import requests
from django.core.paginator import Paginator
import uuid
import datetime




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
        producto['preciousd'] = round(producto['precio'] / valor_usd, 2)

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


import requests
from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Carrito
from .forms import CantidadForm
import json

def detalleProducto(request, id_producto):
    # Obtener producto desde la API
    url = f"http://127.0.0.1:5000/productos/{id_producto}"
    producto = requests.get(url).json()

    # Obtener el valor del USD
    respuesta = requests.get('https://mindicador.cl/api/dolar').json()
    valor_usd = respuesta['serie'][0]['valor']
    producto['preciousd'] = round(producto['precio'] / valor_usd, 2)

    # Obtener el cliente actual
    try:
        cliente = User.objects.get(username=request.user.username)
    except User.DoesNotExist:
        cliente = None

    # Datos a pasar al contexto
    data = {
        'producto': producto,
        'usuario': request.user.username,
        'form': CantidadForm(initial={'cantidad': 1})
    }

    if request.method == 'POST':
        formulario = CantidadForm(request.POST, files=request.FILES)  # Obtener la data del formulario
        if formulario.is_valid():
            cantidad = int(formulario.cleaned_data["cantidad"])
            try:
                CarritoCP = Carrito.objects.get(cliente=cliente, producto=id_producto, vigente=True)
                cantidadstock = CarritoCP.cantidad + producto['stock']
                CarritoCP.cantidad += cantidad

                if CarritoCP.cantidad > cantidadstock:
                    CarritoCP.cantidad = cantidadstock
                    CarritoCP.save()
                    producto['stock'] = 0
                else:
                    CarritoCP.save()
                    producto['stock'] -= cantidad
            except Carrito.DoesNotExist:
                if cantidad > producto['stock']:
                    # Crear el carrito con la cantidad máxima disponible
                    carrito = Carrito.objects.create(cliente=cliente, producto=id_producto, cantidad=producto['stock'], vigente=True)
                    producto['stock'] = 0
                else:
                    carrito = Carrito.objects.create(cliente=cliente, producto=id_producto, cantidad=cantidad, vigente=True)
                    producto['stock'] -= cantidad
        
        # Actualizando stock
        producto_actualizado = {
            "id_producto": producto['id_producto'],
            "nombre": producto['nombre'],
            "id_marca": producto['id_marca'],
            "nombre_marca": producto['nombre_marca'],
            "precio": producto['precio'],
            "stock": producto['stock'],
            "imagen": producto['imagen']
        }
        url_put = f"http://127.0.0.1:5000/productos/{id_producto}"
        headers = {'Content-Type': 'application/json'}  # Especifica el tipo de contenido JSON
        # Convierte el diccionario producto_actualizado a JSON y realiza la solicitud PUT
        response = requests.put(url_put, data=json.dumps(producto_actualizado), headers=headers)

    return render(request,'core/detalleProducto.html', data)

def carrito(request):
    cliente = User.objects.get(username=request.user.username)
    CarritoCliente = Carrito.objects.filter(cliente=cliente, vigente=True)
    existe = CarritoCliente.exists()
    respuesta = requests.get('https://mindicador.cl/api/dolar').json()
    valor_usd = respuesta['serie'][0]['valor']

    #Subtotal Carrito
    productos = list()
    total = 0
    for carrito in CarritoCliente:
        id_producto = carrito.producto
        url = f"http://127.0.0.1:5000/productos/{id_producto}"
        producto = requests.get(url).json()
        total+= producto['precio']*carrito.cantidad
        producto['cantidad'] = carrito.cantidad
        producto['subtotal'] = producto['precio']*carrito.cantidad
        producto['subtotalusd'] = round(producto['subtotal']/valor_usd, 2)
        producto['preciousd'] = round(producto['precio']/valor_usd, 2)
        productos.append(producto)
    total_usd = round(total/valor_usd, 2)

    # Obtener las sucursales desde la base de datos
    sucursales = Sucursal.objects.all()

    data = {
        'listado': productos,
        'valorusd': valor_usd,
        'totalusd': total_usd,
        'total': total,
        'existe': existe,
        'sucursales': sucursales  # Añadir sucursales al contexto
        #'form': envioForm()
    }
    return render(request, 'core/carrito.html', data)


def generar_id_random():
    id_random = str(uuid.uuid4())[:5]
    while Compra.objects.filter(codigo=id_random).exists():
        id_random = str(uuid.uuid4())[:5]
    return id_random


def agregarCompra(request):
    cliente = User.objects.get(username=request.user.username)
    carritoCliente = Carrito.objects.filter(cliente=cliente, vigente=True)

    #Subtotal Carrito
    total = 0
    for carrito in carritoCliente:
        id_producto = carrito.producto
        url = f"http://127.0.0.1:5000/productos/{id_producto}"
        producto = requests.get(url).json()
        total+= producto['precio']*carrito.cantidad

    if request.method == 'POST':
        delivery_option = request.POST.get('delivery')
        codigo = generar_id_random()
        for carrito in carritoCliente:
            if delivery_option == 'retiro':
                sucursal_id = request.POST.get('sucursal')
                sucursal = Sucursal.objects.get(id=sucursal_id)
                Compra.objects.create(codigo=codigo,cliente=cliente, carrito=carrito, retiro=True, sucursal=sucursal, direccion="", fecha = datetime.datetime.now())
            elif delivery_option == 'despacho':
                calle = request.POST.get('calle')
                Compra.objects.create(codigo=codigo,cliente=cliente, carrito=carrito, retiro=False, sucursal=None, direccion=calle, fecha = datetime.datetime.now())
            carrito.vigente = False
            carrito.save()
        Boleta.objects.create(codigo=codigo,total=total)
    return redirect(to='/')

def deleteCarrito(request, id_producto):
    cliente = User.objects.get(username=request.user.username)
    itemCarrito = Carrito.objects.filter(cliente=cliente, producto=id_producto, vigente=True)[0]

    url = f"http://127.0.0.1:5000/productos/{id_producto}"
    producto = requests.get(url).json()

    nuevostock=producto['stock']+itemCarrito.cantidad

    # Actualizando stock
    producto_actualizado = {
        "id_producto": producto['id_producto'],
        "nombre": producto['nombre'],
        "id_marca": producto['id_marca'],
        "nombre_marca": producto['nombre_marca'],
        "precio": producto['precio'],
        "stock": nuevostock,
        "imagen": producto['imagen']
    }
    url_put = f"http://127.0.0.1:5000/productos/{id_producto}"
    headers = {'Content-Type': 'application/json'}  # Especifica el tipo de contenido JSON
    # Convierte el diccionario producto_actualizado a JSON y realiza la solicitud PUT
    response = requests.put(url_put, data=json.dumps(producto_actualizado), headers=headers)

    itemCarrito.delete()
    return redirect(to='carrito')


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
