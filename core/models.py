from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Carrito(models.Model):
    cliente = models.ForeignKey(User, on_delete=models.CASCADE)
    producto = models.IntegerField()
    cantidad = models.IntegerField()
    vigente = models.BooleanField()

    def __str__(self):
        return self.cliente.username
    
class Sucursal(models.Model):
    nombre = models.CharField(max_length=60)
    def __str__(self):
        return self.nombre
    
class Compra(models.Model):
    codigo = models.CharField(max_length=20)
    cliente = models.ForeignKey(User, on_delete=models.CASCADE)
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)
    retiro = models.BooleanField()
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE, blank=True, null=True)
    direccion = models.CharField(max_length=200, blank=True)
    contacto = models.CharField(max_length=50, blank=True)
    fecha = models.DateField()

    def __str__(self):
        return self.codigo
    
class Boleta(models.Model):
    codigo = models.CharField(max_length=20)
    total = models.IntegerField()
    def __str__(self):
        return self.codigo
    
