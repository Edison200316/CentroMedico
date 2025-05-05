from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
import re

# Validación personalizada para correo electrónico
def validate_email(value):
    if not re.match(r"[^@]+@[^@]+\.[^@]+", value):
        raise ValidationError(f"El correo '{value}' no tiene un formato válido.")

# Validación personalizada para teléfono
def validate_telefono(value):
    if not re.match(r"^\+?\d{1,3}?[ -]?\(?\d{1,5}\)?[ -]?\d{1,4}[ -]?\d{1,4}[ -]?\d{1,4}$", value):
        raise ValidationError(f"El número de teléfono '{value}' no es válido. Debe tener un formato adecuado.")

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
    documento_identidad = models.CharField(max_length=20, unique=True) 
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=15, validators=[validate_telefono])
    correo = models.EmailField(validators=[validate_email])
    fecha_nacimiento = models.DateField(validators=[validate_fecha_nacimiento])
    fecha_registro = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

    def clean(self):
        if not self.nombre or not self.apellido:
            raise ValidationError("El nombre y apellido son obligatorios.")
        if not self.documento_identidad:
            raise ValidationError("El documento de identidad es obligatorio.")
        if not self.telefono:
            raise ValidationError("El teléfono es obligatorio.")
        if not self.correo:
            raise ValidationError("El correo electrónico es obligatorio.")

# Modelo para Médicos
class Medico(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    especialidad = models.ForeignKey(Especialidad, on_delete=models.CASCADE)
    telefono = models.CharField(max_length=15, validators=[validate_telefono])
    correo = models.EmailField(validators=[validate_email])
    disponibilidad = models.TextField(help_text="Ejemplo: Lunes a Viernes, 9:00 AM - 5:00 PM")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Dr. {self.nombre} {self.apellido} ({self.especialidad})"

    def clean(self):
        if not self.nombre or not self.apellido:
            raise ValidationError("El nombre y apellido del médico son obligatorios.")
        if not self.especialidad:
            raise ValidationError("La especialidad es obligatoria.")
        if not self.telefono:
            raise ValidationError("El teléfono es obligatorio.")
        if not self.correo:
            raise ValidationError("El correo electrónico es obligatorio.")

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
    fecha = models.DateTimeField(default=timezone.now)
    hora = models.TimeField()
    estado = models.CharField(max_length=20, choices=[('Pendiente', 'Pendiente'), ('Confirmada', 'Confirmada'), ('Cancelada', 'Cancelada')], default='Pendiente')
    motivo = models.TextField(null=True, blank=True)  # Agregado el campo 'motivo'
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cita de {self.paciente} con {self.medico} en {self.fecha}"

    def clean(self):
        if self.fecha < timezone.now():
            raise ValidationError("La fecha de la cita no puede ser en el pasado.")
        if not self.motivo:
            raise ValidationError("El motivo de la cita es obligatorio.")

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
        if len(self.indicaciones) == 0:
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
        if self.total <= 0:
            raise ValidationError("El total de la factura debe ser mayor a cero.")
        if self.estado_pago not in ['Pagado', 'Pendiente']:
            raise ValidationError("El estado de pago debe ser 'Pagado' o 'Pendiente'.")

# Modelo para Usuarios del Sistema
class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    correo = models.EmailField(validators=[validate_email])
    rol = models.CharField(max_length=50, choices=[('Secretaria', 'Secretaria'), ('Medico', 'Medico'), ('Administrador', 'Administrador')])
    contrasena = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nombre} ({self.rol})"

    def clean(self):
        if not self.nombre or not self.correo or not self.rol or not self.contrasena:
            raise ValidationError("Todos los campos son obligatorios.")
        if self.rol not in ['Secretaria', 'Medico', 'Administrador']:
            raise ValidationError("El rol debe ser 'Secretaria', 'Medico' o 'Administrador'.")




