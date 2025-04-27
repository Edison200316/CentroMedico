from django.contrib import admin
from .models import Paciente, Medico, Cita, Consulta, Factura, Usuario, Especialidad

# Personalización para especialidades
class EspecialidadAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)
    list_filter = ('nombre',)

# Personalización para pacientes
class PacienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'documento_identidad', 'telefono', 'correo', 'fecha_nacimiento', 'fecha_registro')
    search_fields = ('nombre', 'apellido', 'documento_identidad')
    list_filter = ('fecha_registro', 'fecha_nacimiento')

# Personalización para médicos
class MedicoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'especialidad', 'telefono', 'correo')
    search_fields = ('nombre', 'apellido', 'especialidad')
    list_filter = ('especialidad',)

# Personalización para citas médicas
class CitaAdmin(admin.ModelAdmin):
    list_display = ('paciente', 'medico', 'fecha', 'estado')
    search_fields = ('paciente__nombre', 'medico__nombre', 'motivo')
    list_filter = ('estado', 'fecha')

# Personalización para consultas médicas
class ConsultaAdmin(admin.ModelAdmin):
    list_display = ('cita', 'diagnostico', 'receta')
    search_fields = ('cita__paciente__nombre', 'diagnostico')
    list_filter = ['cita__fecha']

# Personalización para facturas
class FacturaAdmin(admin.ModelAdmin):
    list_display = ('consulta', 'fecha', 'total', 'estado_pago')
    search_fields = ('consulta__cita__paciente__nombre', 'estado_pago')
    list_filter = ('estado_pago', 'fecha')

# Personalización para usuarios del sistema
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'correo', 'rol')
    search_fields = ('nombre', 'correo', 'rol')
    list_filter = ('rol',)

# Registro de los modelos en el panel de administración
admin.site.register(Paciente, PacienteAdmin)
admin.site.register(Medico, MedicoAdmin)
admin.site.register(Cita, CitaAdmin)
admin.site.register(Consulta, ConsultaAdmin)
admin.site.register(Factura, FacturaAdmin)
admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Especialidad, EspecialidadAdmin)

