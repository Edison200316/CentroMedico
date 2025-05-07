from django import forms
from .models import Paciente, Medico, Cita, Consulta, Usuario, Especialidad, Factura
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# Formulario para Paciente
class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ['nombre', 'apellido', 'cedula', 'direccion', 'telefono', 'correo', 'fecha_nacimiento']
    
    # Validación del número de cédula
    def clean_cedula(self):
        cedula = self.cleaned_data.get('cedula')
        if Paciente.objects.filter(cedula=cedula).exists():
            raise ValidationError('Ya existe un paciente con este número de cédula.')
        return cedula

    # Validación del número de teléfono
    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        if len(telefono) != 10:
            raise ValidationError('El número de teléfono debe contener exactamente 10 dígitos.')
        return telefono

# Formulario para Médico
class MedicoForm(forms.ModelForm):
    especialidades = forms.ModelMultipleChoiceField(
        queryset=Especialidad.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label="Especialidades"
    )

    class Meta:
        model = Medico
        fields = ['nombre', 'apellido', 'especialidades', 'telefono', 'correo', 'horario_inicio', 'horario_fin']
    
    # Validación del correo electrónico
    def clean_correo(self):
        correo = self.cleaned_data.get('correo')
        if Medico.objects.filter(correo=correo).exists():
            raise ValidationError('Este correo ya está registrado para otro médico.')
        return correo

    # Validación del número de teléfono
    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        if len(telefono) != 10:
            raise ValidationError('El número de teléfono debe contener exactamente 10 dígitos.')
        return telefono

# Formulario para Cita
class CitaForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = ['paciente', 'medico', 'fecha', 'hora', 'estado']
    
    # Validación de disponibilidad de la cita
    def clean(self):
        cleaned_data = super().clean()
        medico = cleaned_data.get('medico')
        fecha = cleaned_data.get('fecha')
        hora = cleaned_data.get('hora')

        if Cita.objects.filter(medico=medico, fecha=fecha, hora=hora).exists():
            raise ValidationError('El médico ya tiene una cita agendada en esta fecha y hora.')
        return cleaned_data

# Formulario para Consulta
class ConsultaForm(forms.ModelForm):
    class Meta:
        model = Consulta
        fields = ['cita', 'diagnostico', 'receta', 'indicaciones']

    # Validación del campo 'motivo' en la cita asociada
    def clean(self):
        cleaned_data = super().clean()
        cita = cleaned_data.get('cita')
        if not cita.motivo:  # Esto verifica que el motivo de la cita esté presente
            raise ValidationError("El motivo de la cita es obligatorio.")
        return cleaned_data

# Formulario para Factura
class FacturaForm(forms.ModelForm):
    class Meta:
        model = Factura
        fields = ['consulta', 'total', 'estado_pago', 'fecha_vencimiento']

    def clean_total(self):
        total = self.cleaned_data.get('total')
        if total <= 0:
            raise forms.ValidationError("El total de la factura debe ser mayor a cero.")
        return total

    def clean_estado_pago(self):
        estado_pago = self.cleaned_data.get('estado_pago')
        if estado_pago not in ['Pagado', 'Pendiente']:
            raise forms.ValidationError("El estado de pago debe ser 'Pagado' o 'Pendiente'.")
        return estado_pago

    def clean_fecha_vencimiento(self):
        fecha_vencimiento = self.cleaned_data.get('fecha_vencimiento')
        if fecha_vencimiento and fecha_vencimiento <= self.cleaned_data['fecha']:
            raise ValidationError("La fecha de vencimiento debe ser posterior a la fecha de la factura.")
        return fecha_vencimiento

# Formulario para Usuario (administradores, secretarias, etc.)
class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nombre', 'correo', 'rol', 'contrasena']

    def clean_correo(self):
        correo = self.cleaned_data.get('correo')
        if Usuario.objects.filter(correo=correo).exists():
            raise ValidationError('Este correo electrónico ya está registrado.')
        return correo

# Formulario para Especialidad
class EspecialidadForm(forms.ModelForm):
    class Meta:
        model = Especialidad
        fields = ['nombre']

    # Validación para evitar duplicados de especialidades
    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if Especialidad.objects.filter(nombre__iexact=nombre).exists():
            raise ValidationError('Ya existe una especialidad con este nombre.')
        return nombre

class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Correo electrónico")

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
