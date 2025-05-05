from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages 
from .models import Paciente, Medico, Cita, Consulta, Usuario
from .forms import PacienteForm, MedicoForm, CitaForm, ConsultaForm, UsuarioForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout

@login_required
def inicio(request):
    # Si el usuario está autenticado, muestra la página de inicio
    return render(request, 'inicio.html')

# Vista no autenticada redirige al login
def home(request):
    return redirect('login')

# Vista para el login
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirigir según el rol
                if user.is_superuser:
                    return redirect('inicio_admin')  # Redirigir a la página de admin
                else:
                    return redirect('inicio_usuario')  # Redirigir a la página de usuario normal
            else:
                form.add_error(None, 'Usuario o contraseña incorrectos.')
    else:
        form = AuthenticationForm()

    return render(request, 'usuarios/login.html', {'form': form})

@login_required
def inicio(request):
    return render(request, 'inicio.html')
def es_admin(user):
    return user.rol == 'admin'

@login_required
def inicio(request):
    if request.user.is_staff:
        # Código para el administrador
        return render(request, 'admin_inicio.html')
    else:
        # Código para usuarios normales
        return render(request, 'usuario_inicio.html')

def dashboard(request):
    return render(request, 'dashboard.html')

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
# Listar Citas
def citas_lista(request):
    citas = Cita.objects.all()
    return render(request, 'citas/lista.html', {'citas': citas})

# Crear Nueva Cita
def citas_nueva(request):
    pacientes = Paciente.objects.all()
    medicos = Medico.objects.all()

    if request.method == 'POST':
        paciente_id = request.POST['paciente']
        medico_id = request.POST['medico']
        fecha = request.POST['fecha']
        hora = request.POST['hora']
        estado = request.POST['estado']
        motivo = request.POST['motivo']

        cita = Cita(
            paciente_id=paciente_id,
            medico_id=medico_id,
            fecha=fecha,
            hora=hora,
            estado=estado,
            motivo=motivo
        )
        cita.save()
        messages.success(request, "Cita creada correctamente.")
        return redirect('citas_lista')

    return render(request, 'citas/nueva.html', {'pacientes': pacientes, 'medicos': medicos})

# Editar Cita
def citas_editar(request, cita_id):
    cita = get_object_or_404(Cita, id=cita_id)
    pacientes = Paciente.objects.all()
    medicos = Medico.objects.all()

    if request.method == 'POST':
        cita.paciente_id = request.POST['paciente']
        cita.medico_id = request.POST['medico']
        cita.fecha = request.POST['fecha']
        cita.hora = request.POST['hora']
        cita.estado = request.POST['estado']
        cita.motivo = request.POST['motivo']
        cita.save()
        messages.success(request, "Cita actualizada correctamente.")
        return redirect('citas_lista')

    return render(request, 'citas/editar.html', {
        'cita': cita,
        'pacientes': pacientes,
        'medicos': medicos
    })

# cancelar Cita
def citas_cancelar(request, cita_id):
    cita = get_object_or_404(Cita, id=cita_id)
    if request.method == 'POST':
        cita.estado = 'Cancelada'
        cita.save()
        messages.success(request, "La cita fue cancelada correctamente.")
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

def consultas_editar(request, id):
    consulta = get_object_or_404(Consulta, id=id)
    if request.method == 'POST':
        form = ConsultaForm(request.POST, instance=consulta)
        if form.is_valid():
            form.save()
            messages.success(request, "Consulta actualizada exitosamente.")
            return redirect('consultas_lista')
    else:
        form = ConsultaForm(instance=consulta)
    return render(request, 'consultas/editar.html', {'form': form, 'consulta': consulta})

def consultas_eliminar(request, id):
    consulta = get_object_or_404(Consulta, id=id)
    if request.method == 'POST':
        consulta.delete()
        messages.success(request, "Consulta eliminada exitosamente.")
        return redirect('consultas_lista')
    return render(request, 'consultas/eliminar_confirmar.html', {'consulta': consulta})


# Vistas para Usuarios
def usuarios_lista(request):
    usuarios = Usuario.objects.all()
    return render(request, 'usuarios/lista.html', {'usuarios': usuarios})

def usuarios_eliminar(request, id):
    usuario = get_object_or_404(Usuario, id=id)
    if request.method == 'POST':
        usuario.delete()
        messages.success(request, "Usuario eliminado exitosamente.")
        return redirect('usuarios_lista')
    return render(request, 'usuarios/eliminar.html', {'usuario': usuario})

