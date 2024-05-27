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
    fecha = models.DateField()

    def __str__(self):
        return self.codigo
    
class Boleta(models.Model):
    codigo = models.CharField(max_length=20)
    total = models.IntegerField()
    transferencia = models.BooleanField(default=False)
    validacion = models.BooleanField(blank=True, null=True,default=False)
    imagen = models.ImageField(null=True, blank=True,default=None)
    aceptado = models.BooleanField(default=False)
    bodeguero = models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank=True,default=None)

    def __str__(self):
        return self.codigo
    
    
class MensajeContacto(models.Model):
    nombre = models.CharField(max_length=100)
    correo = models.EmailField()
    telefono = models.CharField(max_length=15)
    asunto = models.CharField(max_length=200)
    mensaje = models.TextField()

    def __str__(self):
        return self.asunto