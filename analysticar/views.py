
from django.shortcuts import render, redirect
from analysticar.models import *
from analysticar.forms import *
from django.http import HttpResponseRedirect, HttpResponse
from watson_developer_cloud import VisualRecognitionV3 as VisualRecognition
from django.http import HttpResponseServerError
from watson_developer_cloud import AssistantV1
from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from analysticar.models import User
from django.views.generic import ListView
from django.views.generic.edit import UpdateView
from io import BytesIO
from http.client import HTTPSConnection
from base64 import b64encode
from django.contrib import messages
from django.db.models import Q
import errno
import datetime
import json
import os
import requests
import base64
from django.utils import timezone
from django.conf import settings
from django.core.files import temp as tempfile
from django.core.files.base import File
from django.utils.encoding import force_str
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import zipfile


# API Key del servicio de Visual Recognition en Bluemix
API_KEY_VISUAL = 'iM10sei5P9VeEyEraNLXFGNvW5uNagfefkkqq5-FLwuy'

# Lista con los ID de los modelos usados
clasificadores = ['Analyticar_1124825301']

# Creamos una instancia del servicio de Visual Recognition
visual_recognition = VisualRecognition('2018-03-19',iam_apikey=API_KEY_VISUAL)

conversation = AssistantV1(
    version='2018-07-10',
    ## url is optional, and defaults to the URL below. Use the correct URL for your region.
    url='https://gateway.watsonplatform.net/assistant/api',
    iam_apikey='XMhojkQjclmpi53yFvOzMAuNCr52CKPA5jdM9hNpKi6O')

workspace_id = '796c9c34-4909-45a1-8195-56a586476843'

#Archivos Temporales
__all__ = ('UploadedFile', 'TemporaryUploadedFile', 'InMemoryUploadedFile',
           'SimpleUploadedFile')

client_id=b'1e7f65f8-063e-4804-bffa-9dc9c0e7aa7a'
client_secret=b'389dd14d21968e2d9185c59a42f896b7d21446be'
url = "https://us-south.dynamic-dashboard-embedded.cloud.ibm.com/daas/v1/session"

#-------- Vista de la página principal --------#
def home(request):
  return render(request, 'index.html')


#--------- Vista para el inicio de sesión de usuarios al sistema --------#
def iniciarSesion(request):
  if request.method == 'POST':
    form = iniciarSesionForm(request.POST)

    if form.is_valid():
      # Verifico si el usuario existe, esté activo o no
      user = authenticate(username = form.cleaned_data['identificacion'], password = form.cleaned_data['clave'])
      if user is not None:
        if user.is_active:
          login(request, user)

          # Verificaciones para cuando se redirige a esta vista por requerimiento de loggeo
          if not(request.GET.get('next')):
            print('hola')
            if user.perfil == 3:
              return redirect('patrones')
            elif user.perfil == 2:
              return redirect('perfil')
            else:
              return redirect('/')
          else:
            print('data')  
            return redirect(request.GET.get('next'))
        else:
          msg = "Su usuario se encuentra inactivo."
          return render(request, 'inicio_sesion.html', {'form': form, 'msg': msg, 'color': rojo})
      else:
        msg = "Usuario o contraseña incorrecta."
        return render(request, 'inicio_sesion.html', {'form': form, 'msg': msg, 'color': rojo})
  else:
    form = iniciarSesionForm()
  return render(request, 'inicio_sesion.html', {'form': form})

#-------- Vista para cerrar sesión de usuarios en el sistema --------#
def cerrarSesion(request):
  logout(request)

  return redirect('/')



#-------- Vista para el registro de nuevos usuarios --------#
def registrarUsuario(request):
  if request.method == 'POST':
    form = registrarUsuarioForm(request.POST)
  
    if form.is_valid():
      ident = form.cleaned_data['ident']
      # user.pareja = 1
      # user.hijos = 1
      # print(user.fechaNac)
      print(ident)
      print(User.objects)
      if User.objects.filter(ident=ident).exists():
        print("Hola")
        msg = "Esta cédula ya se encuentra registrada."
        return render(request,'registrar_usuario.html',{'form' : form,'formubi' : formubi, 
                             'msg' : msg,
                             'color': rojo})

      if form.cleaned_data['password1']!= form.cleaned_data['password2']:
        msg = "Las contraseñas no coinciden. Intente de nuevo."
        return render(request,'registrar_usuario.html',{'form' : form,'formubi' : formubi, 
                             'msg' : msg,
                             'color': rojo})

      # Creamos el objeto User nativo de Django
    
      # raw_password = form.cleaned_data.get('password1')
      # user = authenticate(username=ident, password=raw_password)
      form.save()

      messages.success(request, "El usuario fue registrado exitosamente.")
      return redirect('iniciarSesion')
    else:
      print(">>>>>",form.errors)
  else:
    form = registrarUsuarioForm()
    

  return render(request, 'registrar_usuario.html', {'form': form})

# Updates the response text using the intent confidence
#
# Parámetros:
#           inputW The request to the watson_assistant service
#           response The response from the watson_assistant service
# @return {Object}          The response with the updated message
def updateMessage(inputW, response):
  responseText = ""
  if not(response['output']):
    response['output'] = {}
  else:
    return response

  if response['intents'] and response['intents'][0]:
    intent = response['intents'][0]

    if intent['confidence'] >= 0.75:
      responseText = 'I understood your intent was ' + intent['intent']
    elif intent['confidence'] >= 0.5:
      responseText = 'I think your intent was ' + intent['intent']
    else:
      responseText = 'I did not understand your intent'

  response['output']['text'] = responseText
  return response

@csrf_exempt
def apiMessage(request):
  global conversation, workspace_id

  if request.method == 'POST':
    json_str=((request.body).decode('utf-8'))
    json_obj=json.loads(json_str)

    print(json_obj)
    if not('input' in json_obj):
        inputW = {'text': ''}
        if not('context' in json_obj):
            context = {}
        else:
            context = json_obj['context']
    else:
        inputW = json_obj['input']
        context = json_obj['context']
    
    #Para agregar datos del usuario al contexto
    if request.user.is_authenticated():
      context['name'] = request.user.first_name
    
    payload = {
            'workspace_id': workspace_id,
            'context': context,
            'input': inputW
    }
    
  
    if inputW != {}:  
      if 'tipo_inspeccion' in payload['context']:
        payload['context'].pop('tipo_inspeccion', None)
      elif 'redes_sociales' in payload['context']:
        payload['context'].pop('redes_sociales', None)            

    response = conversation.message(workspace_id=workspace_id, input=inputW, context=context)

    return JsonResponse(updateMessage(payload, response))

# Función para determinar el número de reporte, aprobación y orden

def perfil(request):
  # print(usuario)
  usuario = User.objects.filter(ident=request.user)
  return render(request, 'perfil.html', {'usuario': usuario})



#------- Vista para el reporte de siniestros -------#

userAndPass = b64encode(b"%s:%s" % (
              client_id,
              client_secret
          )).decode("ascii")

def patrones(request):
  payload = "{\r\n  \"expiresIn\": 3600,\r\n  \"webDomain\": \"http://localhost:8000/\"\r\n}"
  headers = {
    'accept': "application/json",
    'Content-Type': "application/json",
    'Authorization' : 'Basic %s' %  userAndPass
    }

  response = requests.request("POST", url, data=payload, headers=headers)

  json_data = response.text

  python_obj = json.loads(json_data)

  sessionCode = python_obj["sessionCode"]
  print(python_obj["sessionCode"])
  # return response.json()
  return render(request, 'patrones.html',{'sessionCode': sessionCode})

def siniestralidad(request):
  payload = "{\r\n  \"expiresIn\": 3600,\r\n  \"webDomain\": \"http://localhost:8000/\"\r\n}"
  headers = {
    'accept': "application/json",
    'Content-Type': "application/json",
    'Authorization': "Basic MWU3ZjY1ZjgtMDYzZS00ODA0LWJmZmEtOWRjOWMwZTdhYTdhOjM4OWRkMTRkMjE5NjhlMmQ5MTg1YzU5YTQyZjg5NmI3ZDIxNDQ2YmU="
    }

  response = requests.request("POST", url, data=payload, headers=headers)

  json_data = response.text

  python_obj = json.loads(json_data)

  sessionCode = python_obj["sessionCode"]
  print(python_obj["sessionCode"])
  # return response.json()
  return render(request, 'siniestralidad.html',{'sessionCode': sessionCode})

def alertas(request):
  payload = "{\r\n  \"expiresIn\": 3600,\r\n  \"webDomain\": \"http://localhost:8000/\"\r\n}"
  headers = {
    'accept': "application/json",
    'Content-Type': "application/json",
    'Authorization': "Basic MWU3ZjY1ZjgtMDYzZS00ODA0LWJmZmEtOWRjOWMwZTdhYTdhOjM4OWRkMTRkMjE5NjhlMmQ5MTg1YzU5YTQyZjg5NmI3ZDIxNDQ2YmU="
    }

  response = requests.request("POST", url, data=payload, headers=headers)

  json_data = response.text

  python_obj = json.loads(json_data)

  sessionCode = python_obj["sessionCode"]
  print(python_obj["sessionCode"])
  # return response.json()
  return render(request, 'alertas.html',{'sessionCode': sessionCode})

# def migrar(request):
#   titles = json.loads(open('initial_data.json').read())
#     # # Create a Django model object for each object in the JSON 
#   for title in titles['Estado']:
#     if Municipio.objects.filter(id=title['pk']).exists():
#       break
#     Municipio.objects.create(id=title['pk'], Nombre=title['estado'])

#   for title in titles['Ciudad']:
#     if Urbanizacion.objects.filter(id=title['pk']).exists():
#       break
#     Urbanizacion.objects.create(id=title['pk'], Nombre=title['ciudad'],municipio_id=title['estado'])
#   return render(request, 'registrar_usuario.html', {'form': form})
