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
  
]
