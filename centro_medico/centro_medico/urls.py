"""
URL configuration for centro_medico project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from pacientes import views  
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Rutas para Pacientes
    path('pacientes/', views.pacientes_lista, name='pacientes_lista'),
    path('pacientes/nuevo/', views.pacientes_nuevo, name='pacientes_nuevo'),
    path('pacientes/<int:id>/editar/', views.pacientes_editar, name='pacientes_editar'),
    path('pacientes/<int:id>/eliminar/', views.pacientes_eliminar, name='pacientes_eliminar'),
    path('pacientes/buscar/', views.pacientes_buscar, name='pacientes_buscar'),

    # Rutas para Médicos
    path('medicos/', views.medicos_lista, name='medicos_lista'),
    path('medicos/nuevo/', views.medicos_nuevo, name='medicos_nuevo'),
    path('medicos/<int:id>/editar/', views.medicos_editar, name='medicos_editar'),
    path('medicos/<int:id>/eliminar/', views.medicos_eliminar, name='medicos_eliminar'),

    # Rutas para Citas Médicas
    path('citas/', views.citas_lista, name='citas_lista'),
    path('citas/nueva/', views.citas_nueva, name='citas_nueva'),
    path('citas/<int:id>/editar/', views.citas_editar, name='citas_editar'),
    path('citas/<int:id>/cancelar/', views.citas_cancelar, name='citas_cancelar'),

    # Rutas para Consultas Médicas
    path('consultas/', views.consultas_lista, name='consultas_lista'),
    path('consultas/nueva/', views.consultas_nueva, name='consultas_nueva'),

    # Rutas para Gestión de Usuarios (administrador, secretarias, etc.)
    path('usuarios/', views.usuarios_lista, name='usuarios_lista'),
    path('usuarios/nuevo/', views.usuarios_nuevo, name='usuarios_nuevo'),
    path('usuarios/<int:id>/editar/', views.usuarios_editar, name='usuarios_editar'),
    path('usuarios/<int:id>/eliminar/', views.usuarios_eliminar, name='usuarios_eliminar'),

    # Ruta para acceder al panel de administración
    path('admin/', admin.site.urls),
]

# Configuración para servir archivos estáticos 
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

