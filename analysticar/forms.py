# -*- coding: utf-8 -*-

from django import forms
from django.core.validators import RegexValidator
from analysticar.models import *
from django.forms.models import modelformset_factory, inlineformset_factory
from django.forms import ModelChoiceField
from django.utils.translation import ugettext, ugettext_lazy as _
from django.forms.extras.widgets import SelectDateWidget
from django.contrib.auth.forms import UserCreationForm
import datetime
from functools import partial

class iniciarSesionForm(forms.Form):
  identificacion = forms.CharField(
              max_length = 50,
              required = True,
              label = "Nº de Identificación",
              widget = forms.TextInput(attrs={'style': 'width:100%'})
          )

  clave = forms.CharField(
              max_length = 25,
              required = True,
              label = "Contraseña",
              widget = forms.PasswordInput(attrs={'style': 'width:100%'})
      )


class registrarUsuarioForm(UserCreationForm):
  DateInput = partial(forms.DateInput, {'class': 'datepicker'})
  ident = forms.CharField(
              max_length = 50,
              required = True,
              label = "Nº de Identificación",
              widget = forms.TextInput(attrs={'style': 'width:100%;'}))

  password1 = forms.CharField(
              max_length = 25,
              required = True,
              label = "Contraseña",
              widget = forms.PasswordInput(attrs={'style': 'width:100%;'}))

  password2 = forms.CharField(
              max_length = 25,
              required = True,
              label = "Ingrese nuevamente la contraseña",
              widget = forms.PasswordInput(attrs={'style': 'width:100%;'}))

  first_name = forms.CharField(max_length = 30, 
          required = True, 
          label = "Nombre", 
          widget=forms.TextInput(attrs={'style': 'width:100%'}),
          validators = [
              RegexValidator(
                regex = '^[a-zA-ZáéíóúñÑÁÉÍÓÚ][a-zA-ZáéíóúñÑÁÉÍÓÚ ]+$',
                message = 'Solo debe contener letras.'
            )])

  last_name = forms.CharField(max_length = 30, 
          required = True, 
          label = "Apellido", 
          widget=forms.TextInput(attrs={'style': 'width:100%'}),
          validators = [
              RegexValidator(
                regex = '^[a-zA-ZáéíóúñÑÁÉÍÓÚ][a-zA-ZáéíóúñÑÁÉÍÓÚ ]+$',
                message = 'Solo debe contener letras.'
            )
          ])

  email = forms.EmailField(required = True, 
              label = "Correo electrónico", 
              widget=forms.EmailInput(attrs={'style': 'width:100%;'}))

  direccion = forms.CharField(required = True,
                max_length = 500,
                label = "Calle",
                widget = forms.TextInput(attrs={'style': 'width:100%;'}))

  telefono = forms.CharField(required = True,
                 max_length = 50,
                 label = "Teléfono",
                 widget = forms.TextInput(attrs={'style': 'width:100%;'}))

  fechaNac = forms.DateField(
            label = "Fecha de nacimiento",
            required = True,
            widget = DateInput(),
            input_formats = ['%d/%m/%Y']
      )

  opcionesEstadoC = (('soltero', 'Soltero'), ('casado', 'Casado'), ('divorciado', 'Divorciado'))
  estadoCivil = forms.ChoiceField(required = True, 
          choices = opcionesEstadoC, 
          widget = forms.Select(attrs={'style': 'width:100%; background-color:white'}), 
          label = "Estado civil")

  opcionesBin = ((1, 'Si'), (0, 'No'))

  pareja = forms.ChoiceField(required = True, 
          choices = opcionesBin, 
          widget = forms.Select(attrs={'style': 'width:100%; background-color:white'}), 
          label = "En pareja")

  hijos = forms.ChoiceField(required = True, 
          choices = opcionesBin, 
          widget = forms.Select(attrs={'style': 'width:100%; background-color:white'}), 
          label = "Hijos")
  municipio = forms.ModelChoiceField(
    label=u'Municipio',
    widget=forms.Select(attrs={'style': 'width:100%'}), 
    queryset=Municipio.objects.all()
  )
  urbanizacion = forms.ModelChoiceField(
      label=u'Urbanizacion',
      widget=forms.Select(attrs={'style': 'width:100%'}), 
      queryset=Urbanizacion.objects.all()
  )


  def __init__(self, *args, **kwargs):
    super(registrarUsuarioForm, self).__init__(*args, **kwargs)
    for i in self.fields:
        self.fields[i].widget.attrs.update({'class' : 'form-control'})

  def clean_email(self):
    return self.cleaned_data['email'].lower()
  
  def clean_first_name(self):
    return self.cleaned_data['first_name'].title()
  
  def clean_last_name(self):
    return self.cleaned_data['last_name'].title()
  

  

  class Meta:
    model = User
    fields = ( 'ident',
               'email',
               'password1',
               'password2',
               'first_name',
               'last_name' ,
               'urbanizacion',
               'direccion',
               'telefono',
               'fechaNac',
               'estadoCivil',
               'pareja',
               'hijos')

widget = forms.Select(attrs={'style': 'width:100%; background-color:white'}),


class UbicacionForm(forms.Form):
    municipio = forms.ModelChoiceField(
        label=u'Estado',
        widget=forms.Select(attrs={'style': 'width:100%'}), 
        queryset=Municipio.objects.all()
    )
    urbanizacion = forms.ModelChoiceField(
        label=u'Municipio',
        widget=forms.Select(attrs={'style': 'width:100%'}), 
        queryset=Urbanizacion.objects.all()
    )

    def __init__(self, *args, **kwargs):
        super(UbicacionForm, self).__init__(*args, **kwargs)
        # self.fields['urbanizacion'].queryset = Urbanizacion.objects.none()