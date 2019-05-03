from django.http import JsonResponse

from analysticar.models import *


def get_urbanizacion(request):
    municipio_id = request.GET.get('municipio_id')
    urbanizacions = Urbanizacion.objects.none()
    options = '<option value="" selected="selected">---------</option>'
    if municipio_id:
        urbanizacions = Urbanizacion.objects.filter(municipio_id=municipio_id)
    else:
        users = models.User.objects.all()   
    for urbanizacion in urbanizacions:
        options += '<option value="%s">%s</option>' % (
            urbanizacion.pk,
            urbanizacion.Nombre
        )
    response = {}
    response['urbanizacion'] = options
    return JsonResponse(response)

def get_taller(request):
    print('este')
    provincia_id = request.GET.get('provincia_id')
    urbani = Urbanizacion.objects.filter(id=provincia_id)
    tallers = Taller.objects.none()
    cidads = Urbanizacion.objects.none()
    options = '<option value="0" selected="selected">---------</option>'
    optionsC = ''
    if provincia_id:
        tallers = Taller.objects.filter(urbanizacion_id=provincia_id)
        cidads = Municipio.objects.filter(pk__in=urbani.values('municipio'))
    else:
        users = models.User.objects.all()   

    for taller in tallers:
        options += '<option value="%s">%s</option>' % (
            taller.pk,
            taller.nombre
        )
    for ciudades in cidads:
        optionsC += '<option value="%s">%s</option>' % (
            ciudades.pk,
            ciudades.Nombre
        )
    response = {}
    responseC = {}
    response['taller'] = options
    responseC['ciudades'] = optionsC
    respuesta = response.copy()
    respuesta.update(responseC)
    return JsonResponse(respuesta)

def get_ciudad(request):
    ciudad_id = request.GET.get('ciudad_id')
    urbani = Urbanizacion.objects.filter(municipio_id=ciudad_id).distinct()
    tallers = Taller.objects.none()
    options = '<option value="0" selected="selected">Seleccione el Municipio</option>'
    optionsC = '<option value="0" selected="selected">---------</option>'
    if ciudad_id:
        urbaniz = Urbanizacion.objects.filter(municipio_id=ciudad_id,talleres__isnull=False).distinct()
        tallers = Taller.objects.filter(pk__in=urbaniz.values('talleres'))
    else:
        users = models.User.objects.all()   

    # for taller in tallers:
    #     options += '<option value="0">%s</option>' % (
    #         taller.pk,
    #         taller.nombre
    #     )
    for provincias in urbaniz:
        optionsC += '<option value="%s">%s</option>' % (
            provincias.pk,
            provincias.Nombre
        )
    response = {}
    responseC = {}
    response['taller'] = options
    responseC['provincias'] = optionsC
    respuesta = response.copy()
    respuesta.update(responseC)
    return JsonResponse(respuesta)