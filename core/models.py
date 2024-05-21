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
    
class Compras(models.Model):
    codigo = models.CharField(max_length=20)
    cliente = models.ForeignKey(User, on_delete=models.CASCADE)
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)
    direccion = models.CharField(max_length=50)
    contacto = models.CharField(max_length=50)
    fecha = models.DateField()

    def __str__(self):
        return self.codigo
    
