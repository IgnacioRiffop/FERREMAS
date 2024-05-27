from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm  
from .models import *

class RegistroForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

class CantidadForm (ModelForm):
    cantidad = forms.IntegerField(min_value=1 ,widget=forms.NumberInput(attrs={"placeholder":"Ingrese Cantidad"}))

    class Meta:
        model = Carrito
        fields = ['cantidad']

class MensajeContactoForm(forms.ModelForm):
    class Meta:
        model = MensajeContacto
        fields = ['nombre', 'correo', 'telefono', 'asunto', 'mensaje']   

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class PagoForm (ModelForm):
    class Meta:
        model = Boleta
        fields = ['codigo', 'total', 'transferencia', 'validacion', 'imagen']

class ProductoForm(forms.Form):
    nombre = forms.CharField(min_length=5, max_length=100)
    id_marca = forms.IntegerField()
    nombre_marca = forms.CharField(required=False)
    precio = forms.IntegerField(min_value=1)
    stock = forms.IntegerField(min_value=0)
    imagen = forms.ImageField(required=False)