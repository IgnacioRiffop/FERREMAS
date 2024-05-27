from django.urls import path, include
from.views import *
from rest_framework import routers
from . import views

# CREAMOS LAS RUTAS DEL API
router = routers.DefaultRouter()

## SE VAN A CREAR TODAS LAS URLS
urlpatterns = [
    #API
    path('api/', include(router.urls)),
    #RUTAS
    path('', index, name="index"),
    path('nosotros', nosotros, name="nosotros"),
    path('registro/', registro, name="registro"),
    path('administracion/', administracion, name="administracion"),
    path('crudUsuarios', crudUsuarios, name="crudUsuarios"),
    path('crudClientes/', crudClientes, name="crudClientes"),
    path('crudVendedores', crudVendedores, name="crudVendedores"),
    path('crudBodegueros', crudBodegueros, name="crudBodegueros"),
    path('crudContadores', crudContadores, name="crudContadores"),
    path('estadoPedido', estadoPedido, name="estadoPedido"),
    path('informes', informes, name="informes"),
    path('contacto', contacto, name="contacto"),
    path('perfil', perfil, name="perfil"),
    path('formularioDespacho', formularioDespacho, name="formularioDespacho"),
    path('producto', producto, name="producto"),
    path('detalleProducto/<id_producto>', detalleProducto, name="detalleProducto"),
    path('carrito', carrito, name="carrito"),
    path('peticion_get', peticion_get, name="peticion_get"),
    path('peticion_get_producto/<id_producto>', peticion_get_producto, name="peticion_get_producto"),
    path('peticion_post', peticion_post, name="peticion_post"),
    path('peticion_put/<id_producto>', peticion_put, name="peticion_put"),
    path('peticion_delete/<id_producto>', peticion_delete, name="peticion_delete"),
    path('peticion_patch/<id_producto>', peticion_patch, name="peticion_patch"),
    path('bodega', bodega, name="bodega"),
    path('aceptarPedido/<codigo>', aceptarPedido, name="aceptarPedido"),
    path('modificarPago/<codigo>', modificarPago, name="modificarPago"),


    path('datosTransferencia', datosTransferencia, name="datosTransferencia"),
    path('agregarCompra', agregarCompra, name="agregarCompra"),
    path('deleteCarrito/<id_producto>', deleteCarrito, name="deleteCarrito"),
    path('compras', compras, name="compras"),
    path('compra/<codigo>', compra, name="compra"),
    path('generate_pdf', generate_pdf, name="generate_pdf"),
    path('generate_excel', generate_excel, name='generate_excel'),
    path('perfilEditar', perfilEditar, name='perfilEditar'),
    path('crudPagos', crudPagos, name='crudPagos'),
    path('crudProductos', crudProductos, name='crudProductos'),
    path('verProducto/<id_producto>', verProducto, name='verProducto'),
    path('crudPedidos', crudPedidos, name='crudPedidos'),
    path('pedidosBodeguero', pedidosBodeguero, name='pedidosBodeguero'),
    path('pedidos_tomados', pedidos_tomados, name='pedidos_tomados'),
    path('asignarPedidos', asignarPedidos, name='asignarPedidos'),
    #CRUD
    #AGREGAR
    path('agregarBodeguero', agregarBodeguero, name="agregarBodeguero"),
    path('agregarContador', agregarContador, name="agregarContador"),
    path('agregarProducto', agregarProducto, name="agregarProducto"),
    path('agregarVendedor', agregarVendedor, name="agregarVendedor"),
    path('agregarClientes', agregarClientes, name="agregarClientes"),
    
    #MODIFICAR
    path('modificarBodeguero/<int:id>/', views.modificarBodeguero, name='modificarBodeguero'),
    path('modificarContador/<int:id>/', views.modificarContador, name='modificarContador'),
    path('modificarProducto', modificarProducto, name="modificarProducto"),
    path('modificarVendedor/<int:id>/', views.modificarVendedor, name='modificarVendedor'),
    path('modificarCliente/<int:id>/', views.modificarCliente, name='modificarCliente'),
    #ELIMINAR
    path('eliminarCliente/<int:id>/', eliminarCliente, name='eliminarCliente'),
    path('eliminarContador/<int:id>/', eliminarContador, name='eliminarContador'),
    path('eliminarVendedor/<int:id>/', eliminarVendedor, name='eliminarVendedor'),
    path('eliminarBodeguero/<int:id>/', eliminarBodeguero, name='eliminarBodeguero'),
]
