# -*- coding: utf-8 -*-
from django.db import models
from django.db.models.fields import TextField
from django.contrib.auth.models import Group, Permission
from django.dispatch.dispatcher import receiver
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_migrate
from datetime import datetime
import pytz
from django.utils import timezone
import json

# Create your models here.
class MyUserManager(BaseUserManager):
    """
    A custom user manager to deal with emails as unique identifiers for auth
    instead of usernames. The default that's used is "UserManager"
    """
    def _create_user(self, ident, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not ident:
            raise ValueError('The Email must be set')
        ident = self.normalize_email(ident)
        user = self.model(ident=ident, **extra_fields)
        user.set_password(password)

        user.save()
        return user

    def create_superuser(self, ident, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        user = self._create_user(ident, password,
                                 fechaNac = datetime.strptime("25/03/1993", "%d/%M/%Y"),
                                 direccion = "",
                                 telefono = "",
                                 estadoCivil = "soltero",
                                 pareja = 0,
                                 hijos = 0,
                                 **extra_fields)
        return user

def get_image_path(instance, filename):
    return os.path.join('photos', str(instance.id), filename)


class Municipio(models.Model):
    Nombre = models.CharField(max_length = 1000)

    def __str__(self):
        return self.Nombre

class Urbanizacion(models.Model):
    Nombre = models.CharField(max_length = 1000)
    municipio = models.ForeignKey(Municipio, related_name="urbanizaciones")

    def __str__(self):
        return "%s, %s"%(self.Nombre, self.municipio)


class User(AbstractBaseUser, PermissionsMixin):
    
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    
    ident = models.CharField(max_length = 30, unique=True)
    PerfilBin = ((1, 'Proveedor'), (2, 'Cliente'))
    
    perfil = models.PositiveIntegerField(choices=PerfilBin, blank=True, null=True, default=2)
    email = models.EmailField(unique=True, null=True)
    is_superuser = models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')
    verified     = models.BooleanField(default=False)
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)
    first_name   = models.CharField(blank=True, max_length=30, verbose_name='first name')
    last_name    = models.CharField(blank=True, max_length=30, verbose_name='last name')
    
    direccion = models.TextField(max_length = 1000)
    urbanizacion = models.ForeignKey(Urbanizacion, null=True)
    telefono = models.CharField(blank = True, null = True, max_length = 50)
    fechaNac = models.DateField()

    opcionesEstadoC = (('soltero', 'Soltero'), ('casado', 'Casado'), ('divorciado', 'Divorciado'))
    estadoCivil = models.CharField(choices = opcionesEstadoC, max_length = 20)

    opcionesBin = ((1, 'Si'), (0, 'No'))
    pareja = models.PositiveIntegerField(choices = opcionesBin)
    hijos = models.PositiveIntegerField(choices = opcionesBin)
    # validation_status =

    USERNAME_FIELD = 'ident'
    objects = MyUserManager()

    def __str__(self):
        return self.ident

    def get_full_name(self):
        return self.first_name + " " + self.last_name

    def get_short_name(self):
        return self.first_name

    @property
    def get_direccion(self):
        return "%s, %s, %s"%(self.direccion, self.urbanizacion, self.urbanizacion.municipio)
