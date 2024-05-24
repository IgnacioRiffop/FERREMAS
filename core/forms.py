from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm  
from .models import *

class RegistroForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2']

class CantidadForm (ModelForm):
    cantidad = forms.IntegerField(min_value=1 ,widget=forms.NumberInput(attrs={"placeholder":"Ingrese Cantidad"}))

    class Meta:
        model = Carrito
        fields = ['cantidad']

class MensajeContactoForm(forms.ModelForm):
    class Meta:
        model = MensajeContacto
        fields = ['nombre', 'correo', 'telefono', 'asunto', 'mensaje']   