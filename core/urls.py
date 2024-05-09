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

]
