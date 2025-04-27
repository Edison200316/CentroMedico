from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages 
from .models import Paciente, Medico, Cita, Consulta, Usuario
from .forms import PacienteForm, MedicoForm, CitaForm, ConsultaForm, UsuarioForm

# Vistas para Pacientes
def pacientes_lista(request):
    pacientes = Paciente.objects.all()
    return render(request, 'pacientes/lista.html', {'pacientes': pacientes})

def pacientes_nuevo(request):
    if request.method == 'POST':
        form = PacienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Paciente registrado exitosamente.")
            return redirect('pacientes_lista')
    else:
        form = PacienteForm()
    return render(request, 'pacientes/nuevo.html', {'form': form})

def pacientes_editar(request, id):
    paciente = get_object_or_404(Paciente, id=id)
    if request.method == 'POST':
        form = PacienteForm(request.POST, instance=paciente)
        if form.is_valid():
            form.save()
            messages.success(request, "Paciente actualizado exitosamente.")
            return redirect('pacientes_lista')
    else:
        form = PacienteForm(instance=paciente)
    return render(request, 'pacientes/editar.html', {'form': form, 'paciente': paciente})

def pacientes_eliminar(request, id):
    paciente = get_object_or_404(Paciente, id=id)
    if request.method == 'POST':
        paciente.delete()
        messages.success(request, "Paciente eliminado exitosamente.")
        return redirect('pacientes_lista')
    return render(request, 'pacientes/eliminar.html', {'paciente': paciente})

def pacientes_buscar(request):
    query = request.GET.get('q', '')
    pacientes = Paciente.objects.filter(nombre__icontains=query)
    return render(request, 'pacientes/buscar.html', {'pacientes': pacientes, 'query': query})

# Vistas para Médicos
def medicos_lista(request):
    medicos = Medico.objects.all()
    return render(request, 'medicos/lista.html', {'medicos': medicos})

def medicos_nuevo(request):
    if request.method == 'POST':
        form = MedicoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Médico registrado exitosamente.")
            return redirect('medicos_lista')
    else:
        form = MedicoForm()
    return render(request, 'medicos/nuevo.html', {'form': form})

def medicos_editar(request, id):
    medico = get_object_or_404(Medico, id=id)
    if request.method == 'POST':
        form = MedicoForm(request.POST, instance=medico)
        if form.is_valid():
            form.save()
            messages.success(request, "Médico actualizado exitosamente.")
            return redirect('medicos_lista')
    else:
        form = MedicoForm(instance=medico)
    return render(request, 'medicos/editar.html', {'form': form, 'medico': medico})

def medicos_eliminar(request, id):
    medico = get_object_or_404(Medico, id=id)
    if request.method == 'POST':
        medico.delete()
        messages.success(request, "Médico eliminado exitosamente.")
        return redirect('medicos_lista')
    return render(request, 'medicos/eliminar.html', {'medico': medico})

# Vistas para Citas Médicas
def citas_lista(request):
    citas = Cita.objects.all()
    return render(request, 'citas/lista.html', {'citas': citas})

def citas_nueva(request):
    if request.method == 'POST':
        form = CitaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Cita agendada exitosamente.")
            return redirect('citas_lista')
    else:
        form = CitaForm()
    return render(request, 'citas/nueva.html', {'form': form})

def citas_editar(request, id):
    cita = get_object_or_404(Cita, id=id)
    if request.method == 'POST':
        form = CitaForm(request.POST, instance=cita)
        if form.is_valid():
            form.save()
            messages.success(request, "Cita actualizada exitosamente.")
            return redirect('citas_lista')
    else:
        form = CitaForm(instance=cita)
    return render(request, 'citas/editar.html', {'form': form, 'cita': cita})

def citas_cancelar(request, id):
    cita = get_object_or_404(Cita, id=id)
    if request.method == 'POST':
        cita.delete()
        messages.success(request, "Cita cancelada exitosamente.")
        return redirect('citas_lista')
    return render(request, 'citas/cancelar.html', {'cita': cita})

# Vistas para Consultas Médicas
def consultas_lista(request):
    consultas = Consulta.objects.all()
    return render(request, 'consultas/lista.html', {'consultas': consultas})

def consultas_nueva(request):
    if request.method == 'POST':
        form = ConsultaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Consulta registrada exitosamente.")
            return redirect('consultas_lista')
    else:
        form = ConsultaForm()
    return render(request, 'consultas/nueva.html', {'form': form})

# Vistas para Usuarios
def usuarios_lista(request):
    usuarios = Usuario.objects.all()
    return render(request, 'usuarios/lista.html', {'usuarios': usuarios})

def usuarios_nuevo(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Usuario registrado exitosamente.")
            return redirect('usuarios_lista')
    else:
        form = UsuarioForm()
    return render(request, 'usuarios/nuevo.html', {'form': form})

def usuarios_editar(request, id):
    usuario = get_object_or_404(Usuario, id=id)
    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, "Usuario actualizado exitosamente.")
            return redirect('usuarios_lista')
    else:
        form = UsuarioForm(instance=usuario)
    return render(request, 'usuarios/editar.html', {'form': form, 'usuario': usuario})

def usuarios_eliminar(request, id):
    usuario = get_object_or_404(Usuario, id=id)
    if request.method == 'POST':
        usuario.delete()
        messages.success(request, "Usuario eliminado exitosamente.")
        return redirect('usuarios_lista')
    return render(request, 'usuarios/eliminar.html', {'usuario': usuario})

