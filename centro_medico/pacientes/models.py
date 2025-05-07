from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from datetime import date
import re

# Validación personalizada para correo electrónico
def validate_email(value):
    if not re.match(r"[^@]+@[^@]+\.[^@]+", value):
        raise ValidationError(f"El correo '{value}' no tiene un formato válido.")

# Validación personalizada para teléfono (10 dígitos)
def validate_telefono(value):
    if not re.match(r"^\d{10}$", value):
        raise ValidationError(f"El número de teléfono '{value}' debe contener exactamente 10 dígitos.")

# Validación personalizada para cédula (solo números)
def validate_cedula(value):
    if not re.match(r"^\d+$", value):
        raise ValidationError(f"La cédula '{value}' debe contener únicamente números.")

# Validación para fecha de nacimiento
def validate_fecha_nacimiento(value):
    if value > timezone.now().date():
        raise ValidationError("La fecha de nacimiento no puede ser en el futuro.")

# Modelo para Especialidades
class Especialidad(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre

# Modelo para Pacientes
class Paciente(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    cedula = models.CharField(max_length=10, unique=True)
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=10)
    correo = models.EmailField()
    fecha_nacimiento = models.DateField()
    fecha_registro = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

# Modelo para Médicos
class Medico(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    especialidades = models.ManyToManyField(Especialidad, related_name='medicos')  # Relación ManyToMany
    telefono = models.CharField(max_length=10, validators=[validate_telefono])
    correo = models.EmailField()
    horario_inicio = models.TimeField(default="08:00:00",
        help_text="Hora de inicio del turno (ejemplo: 09:00 AM)")
    horario_fin = models.TimeField(
        help_text="Hora de fin del turno (ejemplo: 05:00 PM)",
        null=True,
        blank=True
    )
    # Validación para el horario de atención
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        especialidades = ", ".join([especialidad.nombre for especialidad in self.especialidades.all()])
        return f"Dr. {self.nombre} {self.apellido} ({especialidades})"

    def obtener_turnos_disponibles(self, fecha):
        """
        Devuelve una lista de turnos disponibles y ocupados para una fecha específica.
        """
        from datetime import timedelta, datetime

        # Convertir el horario de inicio y fin en intervalos de 30 minutos
        turnos = []
        hora_actual = datetime.combine(fecha, self.horario_inicio)
        hora_fin = datetime.combine(fecha, self.horario_fin)

        while hora_actual < hora_fin:
            turnos.append(hora_actual.time())
            hora_actual += timedelta(minutes=30)

        # Obtener las citas agendadas para este médico en la fecha
        citas = Cita.objects.filter(medico=self, fecha=fecha)

        # Marcar los turnos ocupados
        turnos_ocupados = [cita.hora for cita in citas]
        turnos_disponibles = [
            {"hora": turno, "ocupado": turno in turnos_ocupados} for turno in turnos
        ]

        return turnos_disponibles

# Modelo para Citas Médicas
class Cita(models.Model):
    paciente = models.ForeignKey('Paciente', on_delete=models.CASCADE)
    medico = models.ForeignKey('Medico', on_delete=models.CASCADE)
    fecha = models.DateTimeField(default=timezone.now)
    hora = models.TimeField()
    estado = models.CharField(
        max_length=20, 
        choices=[('Pendiente', 'Pendiente'), ('Confirmada', 'Confirmada'), ('Cancelada', 'Cancelada')], 
        default='Pendiente'
    )
    motivo = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cita de {self.paciente} con {self.medico} en {self.fecha.strftime('%Y-%m-%d')} a las {self.hora.strftime('%H:%M')}"

    def clean(self):
        if self.fecha < timezone.now():
            raise ValidationError("La fecha de la cita no puede ser en el pasado.")
        if not self.motivo:
            raise ValidationError("El motivo de la cita es obligatorio.")
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE)
    fecha = models.DateField()
    hora = models.TimeField()
    estado = models.CharField(
        max_length=20,
        choices=[('Pendiente', 'Pendiente'), ('Confirmada', 'Confirmada'), ('Cancelada', 'Cancelada')],
        default='Pendiente'
    )
    motivo = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cita de {self.paciente} con {self.medico} en {self.fecha} a las {self.hora}"

# Modelo para Consultas Médicas
class Consulta(models.Model):
    cita = models.ForeignKey(Cita, on_delete=models.CASCADE)
    diagnostico = models.TextField()
    receta = models.TextField()
    indicaciones = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Consulta para {self.cita.paciente} - {self.diagnostico}"

    def clean(self):
        if not self.diagnostico or not self.receta:
            raise ValidationError("El diagnóstico y la receta son obligatorios.")
        if not self.indicaciones or len(self.indicaciones.strip()) == 0:
            raise ValidationError("Las indicaciones son obligatorias.")

# Modelo para Facturas
class Factura(models.Model):
    consulta = models.ForeignKey(Consulta, on_delete=models.CASCADE)
    fecha = models.DateField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    estado_pago = models.CharField(max_length=20, choices=[('Pagado', 'Pagado'), ('Pendiente', 'Pendiente')])
    fecha_vencimiento = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Factura de {self.consulta.cita.paciente} - Total: {self.total} - Estado: {self.estado_pago}"

    def clean(self):
        if self.estado_pago not in ['Pagado', 'Pendiente']:
            raise ValidationError("El estado de pago debe ser 'Pagado' o 'Pendiente'.")

# Modelo para Usuarios del Sistema
class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    correo = models.EmailField()
    rol = models.CharField(max_length=50, choices=[('Secretaria', 'Secretaria'), ('Medico', 'Medico'), ('Administrador', 'Administrador')])
    contrasena = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nombre} ({self.rol})"

def disponibilidad_medico(request, medico_id):
    medico = get_object_or_404(Medico, id=medico_id)
    fecha = request.GET.get('fecha', date.today())  # Obtener la fecha de la consulta o usar la fecha actual
    turnos = medico.obtener_turnos_disponibles(fecha)

    return render(request, 'medicos/disponibilidad.html', {
        'medico': medico,
        'fecha': fecha,
        'turnos': turnos,
    })




