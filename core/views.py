from django.shortcuts import render, redirect,  get_object_or_404
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
from django.http import HttpResponse
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
        mes = request.POST.get('mes')
        anio = request.POST.get('anio')
        print(mes, anio)
    # Aquí deberías obtener los datos reales de ventas de tu base de datos o cualquier otra fuente
    # Por simplicidad, aquí se proporcionan datos de ejemplo
    sales_data = [
        {"producto": "Martillo", "cantidad": 10, "precio": "$15"},
        {"producto": "Destornillador", "cantidad": 20, "precio": "$10"},
        {"producto": "Sierra", "cantidad": 5, "precio": "$30"}
    ]

    # Crear el objeto PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="informe_ventas.pdf"'
    pdf = SimpleDocTemplate(response, pagesize=letter)
    
    # Crear la tabla para los datos de ventas
    table_data = [["Producto", "Cantidad", "Precio"]]
    for sale in sales_data:
        table_data.append([sale["producto"], sale["cantidad"], sale["precio"]])

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

def perfil(request):
    cliente = User.objects.get(username=request.user.username)

    data = {
        'cliente': cliente
    }
    return render(request,'core/perfil.html', data)

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

def bodega(request):
    return render(request,'core/bodega.html')

def formularioDespacho(request):
    return render(request,'core/formularioDespacho.html')

#CRUD
#AGREGAR
def agregarProducto(request):
    return render(request,'core/agregarProducto.html')


def modificarProducto(request):
    return render(request,'core/modificarProducto.html')



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
            user = authenticate(username = formulario.cleaned_data["username"], password = formulario.cleaned_data["password1"])
            login(request, user)
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
            user = authenticate(username = formulario.cleaned_data["username"], password = formulario.cleaned_data["password1"])
            login(request, user)
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
            user = authenticate(username = formulario.cleaned_data["username"], password = formulario.cleaned_data["password1"])
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
            user = authenticate(username = formulario.cleaned_data["username"], password = formulario.cleaned_data["password1"])
            login(request, user)
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
            return redirect('index')
    else:
        form = UserForm(instance=vendedor)
    
    return render(request, 'core/modificarVendedor.html', {'form': form})

def modificarContador(request, id):
    contador = get_object_or_404(User, id=id)

    if request.method == 'POST':
        form = UserForm(request.POST, instance=contador)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = UserForm(instance=contador)
    
    return render(request, 'core/modificarContador.html', {'form': form})



def modificarBodeguero(request, id):
    bodeguero = get_object_or_404(User, id=id)

    if request.method == 'POST':
        form = UserForm(request.POST, instance=bodeguero)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = UserForm(instance=bodeguero)
    
    return render(request, 'core/modificarBodeguero.html', {'form': form})

def modificarCliente(request, id):
    cliente = get_object_or_404(User, id=id)

    if request.method == 'POST':
        form = UserForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = UserForm(instance=cliente)
    
    return render(request, 'core/modificarCliente.html', {'form': form})
