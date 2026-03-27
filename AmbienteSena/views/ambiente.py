from django.contrib import messages
from django.db import connection
from django.shortcuts import render, redirect

from AmbienteSena.Models.ambiente import Ambiente


def RegistrarAmbiente(request):
    if request.method == 'POST':
        ## Validación de datos ##
        if request.POST.get('nombre') and request.POST.get('tipo') and request.POST.get('observacion'):           
            ## Variables ##
            nombre = request.POST.get('nombre')
            tipo = request.POST.get('tipo')
            observacion = request.POST.get('observacion')
            ## Guardar en BD ##
            try:
                ambiente = Ambiente()
                ambiente.NombreAmbiente = nombre
                ambiente.TipoAmbiente = tipo
                ambiente.Observacion = observacion
                ambiente.save()
                messages.success(request, 'Ambiente de formación registrado correctamente')
            except Exception as e:
                messages.error(request, 'Ocurrió un error en el sistema. Inténtelo más tarde')
            return render(request, 'Ambientes/ListaAmbientes.html')
    else:
        return render(request, 'Ambientes/RegistrarAmbiente.html')
    
###Consultar Ambientes de Formaciom###
def ListarAmbientes(request):
    try:
        ListarAmbientes = Ambiente.objects.all()
    except Exception as e:
        messages.error(request,'Ocurrio un error en el sistema')
        return render(request,'Ambientes/ListaAmbientes.html')
    return render(request,'Ambientes/ListaAmbientes.html', {'ambientes': ListarAmbientes})

##Eliminar un amniente de formacion en el sistema##
def EliminarAmbiente(request):
    if request.method == 'POST':
        try: 
            ambiente = Ambiente.objects.filter(id = request.POST.get('id'))
            ambiente.delete()
            messages.success(request,'Se Elimino el Ambiente de Formacion Exitosamente')
        except Exception as e:
            messages.error(request,f'Ocurrio un error en el sistema: { e }')
        return redirect('/Ambientes/ListaAmbientes')
    
##Editar un ambiente de formacion##
def ActualizarAmbiente(request, id_ambiente):
    if request.method == 'POST':
        try:
            ambiente = Ambiente.objects.get(id = id_ambiente)
            ambiente.NombreAmbiente = request.POST.get('nombre')
            ambiente.TipoAmbiente = request.POST.get('tipo')
            ambiente.Observacion = request.POST.get('observacion')
            ambiente.save()                                                    
            messages.success(request,'Ambiente actualizo Exitosamente')
        except Exception as e:
            messages.error(request,'Error en el sistema , Vuelva mas tarde')
        return redirect('/Ambientes/ListaAmbientes')
    try:
        ambiente = Ambiente.objects.filter(id = id_ambiente)
        return render(request,'Ambientes/ActualizarAmbiente.html', {'ambiente': ambiente})
    except Exception as e:
        messages.error(request, 'Error en el sistema')
        return redirect('/Ambientes/ListaAmbientes')