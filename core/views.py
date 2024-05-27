from asyncio.log import logger
from pyexpat.errors import messages
from django.shortcuts import render, redirect,  get_object_or_404
import openpyxl
from .models import *
from .forms import *
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User,Group
import json
import requests
from django.core.paginator import Paginator
import uuid
import datetime
from django.core.exceptions import MultipleObjectsReturned
from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Carrito
from .forms import CantidadForm
import json
from django.urls import reverse
from django.core.mail import send_mail
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table
import io
import pandas as pd
from django.http import HttpResponse
from django.contrib.auth.models import User, Group
from django.db.models import Q
import openpyxl
from .models import Boleta
from django.http import JsonResponse
import logging
logger = logging.getLogger(__name__)
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
import random
import os
from django.core.files import File


def group_required(*group_names):
    """Requires user membership in at least one of the groups passed in."""
    def in_groups(u):
        if u.is_authenticated:
            if bool(u.groups.filter(name__in=group_names)) | u.is_superuser:
                return True
        raise PermissionDenied
    return user_passes_test(in_groups)

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
 
    grupo_cliente = Group.objects.get(name='cliente')

    clientes = User.objects.filter(groups__in=[grupo_cliente])

    return render(request,'core/crudClientes.html',{'clientes': clientes})

def crudVendedores(request):

    grupo_vendedor = Group.objects.get(name='vendedor')


    vendedores = User.objects.filter(groups__in=[grupo_vendedor])

    # Imprimir para verificar en la consola
    return render(request,'core/crudVendedores.html',{'vendedores': vendedores})

def crudBodegueros(request):
    grupo_bodeguero = Group.objects.get(name='bodeguero')

    bodegueros = User.objects.filter(groups__in=[grupo_bodeguero])

    return render(request,'core/crudBodegueros.html',{'bodegueros': bodegueros})

def crudContadores(request):
    grupo_contador = Group.objects.get(name='contador')

    contadores = User.objects.filter(groups__in=[grupo_contador])

    return render(request,'core/crudContadores.html',{'contadores': contadores})


def estadoPedido(request):
    return render(request,'core/estadoPedido.html') 


def informes(request):
    # Genera la lista de años desde el año actual hasta 10 años atrás
    anios = list(range(datetime.datetime.now().year, datetime.datetime.now().year - 10, -1))

    # Lista de meses
    meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']

    data = {
        'anios': anios,
        'meses': meses
    }
    return render(request,'core/informes.html', data) 


def generate_pdf(request):
    if request.method == 'POST':
        mes_nombre = request.POST.get('mes')
        anio = int(request.POST.get('anio'))

        # Mapeo de nombres de meses en español a números
        meses = {
            'enero': 1, 'febrero': 2, 'marzo': 3, 'abril': 4, 'mayo': 5, 'junio': 6,
            'julio': 7, 'agosto': 8, 'septiembre': 9, 'octubre': 10, 'noviembre': 11, 'diciembre': 12
        }

        # Convertir el nombre del mes a un número
        mes = meses[mes_nombre.lower()]

        # Filtrar las compras por mes y año
        compras = Compra.objects.filter(
            Q(fecha__year=anio) & Q(fecha__month=mes)
        )

        boletas_compras = list()
        codigos_agregados = set()
        for compra in compras:
            boleta = Boleta.objects.get(codigo=compra.codigo)
            if boleta.codigo not in codigos_agregados:
                boletas_compras.append((boleta, compra))
                codigos_agregados.add(boleta.codigo)


        sales_data = []
        total_sum = 0
        for boleta, compra in boletas_compras:
            sales_data.append({
                "Código de Compra": boleta.codigo,
                "Retiro en Sucursal": "" if compra.sucursal is None else compra.sucursal.nombre,
                "Envio a domicilio": "No aplica" if compra.direccion is None else compra.direccion,
                "Metodo de Pago": "Transferencia" if boleta.transferencia else "Paypal",
                "Total": boleta.total
            })
            total_sum += boleta.total

        # Agregar el total al final de sales_data
        sales_data.append({
            "Código de Compra": "",
            "Retiro en Sucursal": "",
            "Envio a domicilio": "",
            "Metodo de Pago": "",
            "Total": total_sum
        })

        # Crear el objeto PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="Informe_Ventas_{mes_nombre}_{anio}.pdf"'
        pdf = SimpleDocTemplate(response, pagesize=letter)
        
        # Crear la tabla para los datos de ventas
        table_data = [["Código de Compra", "Retiro en Sucursal", "Envio a domicilio", "Metodo de Pago", "Total"],]
        for sale in sales_data:
            table_data.append([sale["Código de Compra"], sale["Retiro en Sucursal"], sale["Envio a domicilio"], sale["Metodo de Pago"], sale["Total"]])

        table = Table(table_data)

        # Estilo de la tabla
        style = [('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)]

        table.setStyle(style)

        # Construir el PDF y devolverlo como una respuesta HTTP
        pdf.build([table])
        return response

def generate_excel(request):
    if request.method == 'POST':
        mes_nombre = request.POST.get('mes')
        anio = int(request.POST.get('anio'))

        # Mapeo de nombres de meses en español a números
        meses = {
            'enero': 1, 'febrero': 2, 'marzo': 3, 'abril': 4, 'mayo': 5, 'junio': 6,
            'julio': 7, 'agosto': 8, 'septiembre': 9, 'octubre': 10, 'noviembre': 11, 'diciembre': 12
        }

        # Convertir el nombre del mes a un número
        mes = meses[mes_nombre.lower()]

        # Filtrar las compras por mes y año
        compras = Compra.objects.filter(
            Q(fecha__year=anio) & Q(fecha__month=mes)
        )

        boletas_compras = list()
        codigos_agregados = set()
        for compra in compras:
            boleta = Boleta.objects.get(codigo=compra.codigo)
            if boleta.codigo not in codigos_agregados:
                boletas_compras.append((boleta, compra))
                codigos_agregados.add(boleta.codigo)


        sales_data = []
        total_sum = 0
        for boleta, compra in boletas_compras:
            sales_data.append({
                "Código de Compra": boleta.codigo,
                "Retiro en Sucursal": "" if compra.sucursal is None else compra.sucursal.nombre,
                "Envio a domicilio": "No aplica" if compra.direccion is None else compra.direccion,
                "Metodo de Pago": "Transferencia" if boleta.transferencia else "Paypal",
                "Total": boleta.total
            })
            total_sum += boleta.total

        # Agregar el total al final de sales_data
        sales_data.append({
            "Código de Compra": "",
            "Retiro en Sucursal": "",
            "Envio a domicilio": "",
            "Metodo de Pago": "",
            "Total": total_sum
        })

        # Crear un DataFrame de pandas con los datos de ventas
        df = pd.DataFrame(sales_data)

        # Crear un objeto BytesIO para almacenar el archivo Excel
        excel_file = io.BytesIO()

        # Escribir el DataFrame en el objeto BytesIO como un archivo Excel
        df.to_excel(excel_file, index=False)

        # Mover el puntero al inicio del archivo
        excel_file.seek(0)

        # Cargar el archivo de Excel con openpyxl
        workbook = openpyxl.load_workbook(excel_file)

        # Obtener la hoja activa
        sheet = workbook.active

        # Ajustar el texto de todas las celdas
        for column in sheet.columns:
            max_length = 0
            column = [cell for cell in column]
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(cell.value)
                except:
                    pass
            adjusted_width = (max_length + 2)
            sheet.column_dimensions[column[0].column_letter].width = adjusted_width

        # Guardar el archivo de Excel en un nuevo objeto BytesIO
        excel_file_adjusted = io.BytesIO()
        workbook.save(excel_file_adjusted)

        # Configurar la respuesta HTTP para descargar el archivo Excel
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename="Informe_Ventas_{mes_nombre}_{anio}.xlsx"'
        response.write(excel_file_adjusted.getvalue())

        return response

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
    if request.method == 'POST':
        form = MensajeContactoForm(request.POST)
        if form.is_valid():
            form.save()

            nombre = form.cleaned_data['nombre']
            correo = form.cleaned_data['correo']
            telefono = form.cleaned_data['telefono']
            asunto = form.cleaned_data['asunto']
            mensaje = form.cleaned_data['mensaje']

            mensaje_email = f"Nombre: {nombre}\nCorreo: {correo}\nTeléfono: {telefono}\nAsunto: {asunto}\nMensaje: {mensaje}"
            send_mail(
                'Nuevo mensaje de contacto',
                mensaje_email,
                correo, 
                ['fvera891@gmail.com'],
                fail_silently=False,
            )

            return redirect('index') 
    else:
        form = MensajeContactoForm()
    return render(request, 'core/contacto.html', {'form': form})

@login_required
def perfil(request):
    cliente = User.objects.get(username=request.user.username)

    data = {
        'cliente': cliente
    }
    return render(request,'core/perfil.html', data)

@login_required
def perfilEditar(request):
    if request.method == 'POST':
        form = UserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('perfilEditar')
    else:
        form = UserForm(instance=request.user)
    return render(request, 'core/perfilEditar.html', {'form': form})

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

def verProducto(request, id_producto):
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
    }
    

    return render(request,'core/verProducto.html', data)



def crudProductos(request):
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
    return render(request, 'core/crudProductos.html', data)

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
        Boleta.objects.create(codigo=codigo,total=total,transferencia=False,validacion=True,imagen=None)
    return redirect(to='compras')

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

def compra(request, codigo):
    try:
        compra = Compra.objects.get(codigo=codigo)
    except MultipleObjectsReturned:
        compra = Compra.objects.filter(codigo=codigo).first()
    except Compra.DoesNotExist:
        compra = None
    boleta = Boleta.objects.get(codigo=codigo)

    if request.method == 'POST':
        # Accede al archivo subido a través de request.FILES
        comprobante = request.FILES.get('comprobante')
        if comprobante:
            # Actualiza el campo imagen de la boleta con el archivo subido
            boleta.imagen = comprobante
            boleta.save()
            # Redirige al usuario a la misma página (o a donde quieras) después de subir el archivo
            return redirect(reverse('compra', args=[codigo]))

    data = {
        'compra' : compra,
        'boleta' : boleta
    }
    return render(request, 'core/compra.html', data)


def compras(request):
    cliente = User.objects.get(username=request.user.username)
    comprasCliente = Compra.objects.filter(cliente=cliente).order_by('-id')
    existe = comprasCliente.exists()

    page = request.GET.get('page', 1) # OBTENEMOS LA VARIABLE DE LA URL, SI NO EXISTE NADA DEVUELVE 1

    productos = list()
    for compra in comprasCliente:
        id_producto = compra.carrito.producto
        url = f"http://127.0.0.1:5000/productos/{id_producto}"
        producto = requests.get(url).json()
        productos.append(producto)

    listadocp = list(zip(comprasCliente, productos))

    try:
        paginator = Paginator(listadocp, 3)
        listadocp = paginator.page(page)
    except:
        raise Http404

    data = {
        'listadocp' : listadocp,
        'productos': productos,
        'listado': comprasCliente,
        'existe': existe,
        'paginator': paginator
    }
    return render(request,'core/compras.html', data)


def datosTransferencia(request):
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
        Boleta.objects.create(codigo=codigo,total=total,transferencia=True,validacion=False,imagen=None)
    return render(request,'core/datosTransferencia.html')

def misPedidos(request):
    return render(request,'core/misPedidos.html')

@group_required('vendedor')
def bodega(request):
    return render(request,'core/bodega.html')

def formularioDespacho(request):
    return render(request,'core/formularioDespacho.html')

def crudPedidos(request):
    return render(request,'core/crudPedidos.html')

@group_required('bodeguero')
def pedidosBodeguero(request):
    boletas_no_aceptadas = Boleta.objects.filter(aceptado=False, validacion=True)
    return render(request, 'core/pedidosBodeguero.html', {'boletas': boletas_no_aceptadas})

def aceptarPedido(request, codigo):
    boleta = get_object_or_404(Boleta, codigo=codigo)
    boleta.aceptado = True
    boleta.bodeguero = request.user
    boleta.save()
    return redirect('pedidosBodeguero')

@group_required('bodeguero')
def pedidos_tomados(request):
    boletas = Boleta.objects.filter(bodeguero=request.user)
    boleta_compras = []
    for boleta in boletas:
        compra = Compra.objects.filter(codigo=boleta.codigo).first()
        boleta_compras.append((boleta, compra))
    return render(request, 'core/pedidos_tomados.html', {'boleta_compras': boleta_compras})



def asignarPedidos(request):
    return render(request,'core/asignarPedidos.html')

#CRUD
#AGREGAR
def generate_random_id():
    return random.randint(100, 1000000)


def agregarProducto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            imagen_file = request.FILES.get('imagen')
            if imagen_file:
                imagen_filename = imagen_file.name
                # Usa os.path.join para construir la ruta del archivo
                base_dir = os.path.dirname(os.path.abspath(__file__))  # obtén el directorio del archivo actual
                imagen_path = os.path.join(base_dir, 'static', 'core', 'img', imagen_filename)
                with open(imagen_path, 'wb+') as destination:
                    for chunk in imagen_file.chunks():
                        destination.write(chunk)
            else:
                imagen_filename = ''
            
            producto = {
                "id_producto": generate_random_id(),
                "nombre": request.POST.get('nombre'),
                "id_marca": request.POST.get('id_marca'),
                "nombre_marca": "bosch",
                "precio": request.POST.get('precio'),
                "stock": request.POST.get('stock'),
                "imagen": imagen_filename
            }

            url = "http://127.0.0.1:5000/productos"
            headers = {'Content-Type': 'application/json'}  # Especifica el tipo de contenido JSON
            
            # Convierte el diccionario producto a JSON y realiza la solicitud POST
            response = requests.post(url, data=json.dumps(producto), headers=headers)
            
            # Aquí puedes manejar el resto de los datos del formulario
            # Cuando hagas la solicitud a la API, usa imagen_filename en lugar de form.cleaned_data['imagen']
    else:
        form = ProductoForm()
    return render(request,'core/agregarProducto.html', {'form': form})


def modificarProducto(request,id_producto):
    url = f"http://127.0.0.1:5000/productos/{id_producto}"
    producto = requests.get(url).json()

    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            imagen_file = request.FILES.get('imagen')
            if imagen_file:
                imagen_filename = imagen_file.name
                # Usa os.path.join para construir la ruta del archivo
                base_dir = os.path.dirname(os.path.abspath(__file__))  # obtén el directorio del archivo actual
                imagen_path = os.path.join(base_dir, 'static', 'core', 'img', imagen_filename)
                with open(imagen_path, 'wb+') as destination:
                    for chunk in imagen_file.chunks():
                        destination.write(chunk)
            else:
                imagen_filename = ''
            
            producto = {
                "nombre": request.POST.get('nombre'),
                "id_marca": request.POST.get('id_marca'),
                "nombre_marca": "bosch",
                "precio": request.POST.get('precio'),
                "stock": request.POST.get('stock'),
                "imagen": imagen_filename
            }
            
            url = f"http://127.0.0.1:5000/productos/{id_producto}"
            headers = {'Content-Type': 'application/json'}  # Especifica el tipo de contenido JSON
            
            # Convierte el diccionario producto_actualizado a JSON y realiza la solicitud PUT
            response = requests.put(url, data=json.dumps(producto), headers=headers)
            
            # Aquí puedes manejar el resto de los datos del formulario
            # Cuando hagas la solicitud a la API, usa imagen_filename en lugar de form.cleaned_data['imagen']
    else:
        data = {
            'nombre': producto['nombre'],
            'id_marca': producto['id_marca'],
            'nombre_marca': producto.get('nombre_marca', ''),  # Usar get() en caso de que 'nombre_marca' no exista
            'precio': producto['precio'],
            'stock': producto['stock'],
            # 'imagen': producto['imagen'],  # No puedes prellenar un ImageField con un valor de texto
        }
        
        # Construye la ruta al archivo de la imagen
        base_dir = os.path.dirname(os.path.abspath(__file__))  # obtén el directorio del archivo actual
        imagen_path = os.path.join(base_dir, 'static', 'core', 'img', producto['imagen'])
        
        try:
            # Intenta abrir el archivo de imagen y crear un objeto File
            with open(imagen_path, 'rb') as f:
                imagen_file = File(f)
                imagen_file.name = producto['imagen']  # Establece el atributo 'name' del objeto File
                data['imagen'] = imagen_file
        except FileNotFoundError:
            # Si el archivo de imagen no existe, deja data['imagen'] como None
            data['imagen'] = None

        # Pasa el diccionario de datos al constructor del formulario
        form = ProductoForm(data)
    return render(request,'core/modificarProducto.html', {'form': form})


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


def deleteProducto(request, id_producto):
    url = f"http://127.0.0.1:5000/productos/{id_producto}"
    
    # Realiza la solicitud DELETE
    response = requests.delete(url)
    
    return redirect(to="crudProductos")


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


def sales_report(request):
    # Lógica para obtener los datos de ventas y mostrarlos en una plantilla HTML
    # Aquí puedes hacer consultas a la base de datos o cualquier otra operación necesaria
    # Por simplicidad, aquí se proporcionan datos de ejemplo
    sales_data = [
        {"producto": "Martillo", "cantidad": 10, "precio": "$15"},
        {"producto": "Destornillador", "cantidad": 20, "precio": "$10"},
        {"producto": "Sierra", "cantidad": 5, "precio": "$30"}
    ]
    context = {"sales_data": sales_data}
    return render(request, 'sales_report.html', context)



def agregarVendedor(request):
    data = {
        'form': RegistroForm()
    }

    if request.method == 'POST':
        formulario = RegistroForm(data=request.POST) # OBTIENE LA DATA DEL FORMULARIO
        if formulario.is_valid():
            formulario.save()
            user = User.objects.get(username=formulario.cleaned_data["username"])
            grupo = Group.objects.get(name='vendedor')
            user.groups.add(grupo)
            #redirigir al home
            return redirect(to="index")
        data["form"]=formulario
    return render(request, 'core/agregarVendedor.html', data)

def agregarContador(request):
    data = {
        'form': RegistroForm()
    }

    if request.method == 'POST':
        formulario = RegistroForm(data=request.POST) # OBTIENE LA DATA DEL FORMULARIO
        if formulario.is_valid():
            formulario.save()
            user = User.objects.get(username=formulario.cleaned_data["username"])
            grupo = Group.objects.get(name='contador')
            user.groups.add(grupo)
            #redirigir al home
            return redirect(to="index")
        data["form"]=formulario
    return render(request, 'core/agregarContador.html', data)

def agregarBodeguero(request):
    data = {
        'form': RegistroForm()
    }

    if request.method == 'POST':
        formulario = RegistroForm(data=request.POST) # OBTIENE LA DATA DEL FORMULARIO
        if formulario.is_valid():
            formulario.save()
            user = User.objects.get(username=formulario.cleaned_data["username"])
            login(request, user)
            grupo = Group.objects.get(name='bodeguero')
            user.groups.add(grupo)
            #redirigir al home
            return redirect(to="index")
        data["form"]=formulario
    return render(request, 'core/agregarBodeguero.html', data)

def agregarClientes(request):
    data = {
        'form': RegistroForm()
    }

    if request.method == 'POST':
        formulario = RegistroForm(data=request.POST) # OBTIENE LA DATA DEL FORMULARIO
        if formulario.is_valid():
            formulario.save()
            user = User.objects.get(username=formulario.cleaned_data["username"])
            grupo = Group.objects.get(name='cliente')
            user.groups.add(grupo)
            #redirigir al home
            return redirect(to="index")
        data["form"]=formulario
    return render(request, 'core/agregarClientes.html', data)


def modificarVendedor(request, id):
    vendedor = get_object_or_404(User, id=id)

    if request.method == 'POST':
        form = UserForm(request.POST, instance=vendedor)
        if form.is_valid():
            form.save()
            return redirect('crudVendedores')
    else:
        form = UserForm(instance=vendedor)
    
    return render(request, 'core/modificarVendedor.html', {'form': form})

def modificarContador(request, id):
    contador = get_object_or_404(User, id=id)

    if request.method == 'POST':
        form = UserForm(request.POST, instance=contador)
        if form.is_valid():
            form.save()
            return redirect('crudContadores')
    else:
        form = UserForm(instance=contador)
    
    return render(request, 'core/modificarContador.html', {'form': form})



def modificarBodeguero(request, id):
    bodeguero = get_object_or_404(User, id=id)

    if request.method == 'POST':
        form = UserForm(request.POST, instance=bodeguero)
        if form.is_valid():
            form.save()
            return redirect('crudBodegueros')
    else:
        form = UserForm(instance=bodeguero)
    
    return render(request, 'core/modificarBodeguero.html', {'form': form})

def modificarCliente(request, id):
    cliente = get_object_or_404(User, id=id)

    if request.method == 'POST':
        form = UserForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('crudClientes')
    else:
        form = UserForm(instance=cliente)
    
    return render(request, 'core/modificarCliente.html', {'form': form})


def eliminarCliente(request, id):
    cliente = get_object_or_404(User, id=id)
    cliente.delete()
    messages.success(request, 'Cliente eliminado correctamente')
    return redirect('crudClientes')

@group_required('contador')
def crudPagos(request):
    boletas = Boleta.objects.all()
    boleta_compras = []
    for boleta in boletas:
        compra = Compra.objects.filter(codigo=boleta.codigo).first()
        boleta_compras.append((boleta, compra))
    return render(request, 'core/crudPagos.html', {'boleta_compras': boleta_compras})	 

def modificarPago(request,codigo):
    pago = get_object_or_404(Boleta, codigo=codigo)

    if request.method == 'POST':
        form = PagoForm(request.POST, instance=pago)
        if form.is_valid():
            form.save()
            return redirect('crudPagos')
    else:
        form = PagoForm(instance=pago)
    return render(request, 'core/modificarPago.html', {'form': form})	 



def guardar_cambios_en_bd(request):
    logger.info('Llamada a la vista guardar_cambios_en_bd')

    if request.method == 'POST' and request.is_ajax():
        numero_pago = request.POST.get('numeroPago')
        nueva_fecha = request.POST.get('nuevaFecha')
        nuevo_monto = request.POST.get('nuevoMonto')
        nuevo_metodo = request.POST.get('nuevoMetodo')

        logger.info('Datos recibidos: número de pago=%s, nueva fecha=%s, nuevo monto=%s, nuevo método=%s', numero_pago, nueva_fecha, nuevo_monto, nuevo_metodo)

        try:
            boleta = get_object_or_404(Boleta, pk=numero_pago)
            boleta.fecha = nueva_fecha
            boleta.total = nuevo_monto
            boleta.transferencia = (nuevo_metodo == 'Transferencia')
            boleta.save()
            logger.info('Cambios guardados correctamente')
            return JsonResponse({'exito': True})
        except Exception as e:
            logger.error('Error al guardar los cambios: %s', str(e))
            return JsonResponse({'exito': False, 'mensaje': str(e)})
    else:
        logger.error('Método no permitido')
        return JsonResponse({'exito': False, 'mensaje': 'Método no permitido'})
    


def eliminarContador(request, id):
    contador = get_object_or_404(User, id=id)
    contador.delete()
    messages.success(request, 'Contador eliminado correctamente')
    return redirect('crudContadores')

def eliminarVendedor(request, id):
    try:
        vendedor = get_object_or_404(User, id=id)
    except Http404:
        messages.error(request, 'Vendedor no encontrado')
        return redirect('crudVendedores')

    vendedor.delete()
    messages.success(request, 'Vendedor eliminado correctamente')
    return redirect('crudVendedores')

def eliminarBodeguero(request, id):
    contador = get_object_or_404(User, id=id)
    contador.delete()
    messages.success(request, 'Bodeguero eliminado correctamente')
    return redirect('crudBodegueros')

