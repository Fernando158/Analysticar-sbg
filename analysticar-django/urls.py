"""analysticar URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from . import settings
from analysticar import views
from django.conf.urls.static import static
from analysticar.ajax import get_urbanizacion,get_taller,get_ciudad
# from analysticar_django.settings import MEDIA_URL, MEDIA_ROOT
# from analysticar.ajax import get_urbanizacion,get_taller,get_ciudad
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.home, name="home"),
    url(r'^iniciar-sesion/$', views.iniciarSesion, name="iniciarSesion"),
    url(r'^cerrar-sesion/$', views.cerrarSesion, name="cerrarSesion"),
    url(r'^registrar-usuario/$', views.registrarUsuario, name="registrarUsuario"),
    url(r'^perfil$', views.perfil, name="perfil"),
    url(r'^patrones', views.patrones, name="patrones"),
    url(r'^siniestralidad', views.siniestralidad, name="siniestralidad"),
    url(r'^alertas$', views.alertas, name="alertas"),
    url(r'^ajax/get_urbanizacion/$', get_urbanizacion, name='get_urbanizacion'),
    url(r'^ajax/get_taller/$', get_taller, name='get_taller'),
    url(r'^ajax/get_ciudad/$', get_ciudad, name='get_ciudad'),
]
