from django.urls import path, include
from.views import *
from rest_framework import routers

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
    path('crudUsuarios/', crudUsuarios, name="crudUsuarios"),
    path('crudClientes/', crudClientes, name="crudClientes"),
    path('contacto', contacto, name="contacto"),
    path('perfil', perfil, name="perfil"),
    path('formularioDespacho', formularioDespacho, name="formularioDespacho"),
    path('producto', producto, name="producto"),
    path('detalleProducto', detalleProducto, name="detalleProducto"),
    path('carrito', carrito, name="carrito"),
    path('peticion_get', peticion_get, name="peticion_get"),
    path('peticion_get_producto/<id_producto>', peticion_get_producto, name="peticion_get_producto"),
    path('peticion_post', peticion_post, name="peticion_post"),
    path('peticion_put/<id_producto>', peticion_put, name="peticion_put"),
    path('peticion_delete/<id_producto>', peticion_delete, name="peticion_delete"),
    path('peticion_patch/<id_producto>', peticion_patch, name="peticion_patch"),

]
