# CentroMedicoWeb

Este es un sistema de gestión para un centro médico, desarrollado con Django. Permite gestionar pacientes, médicos, citas, consultas y usuarios.

## Requisitos previos

Asegúrate de tener instalados los siguientes programas en tu sistema:
- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Virtualenv (opcional, pero recomendado)

## Instalación

1. **Clonar el repositorio**:
   ```bash
   git clone https://github.com/tu-usuario/CentroMedico.git
   cd CentroMedico
   ```

2. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configurar la base de datos**:
   Edita el archivo `settings.py` para configurar la base de datos según tus necesidades.

4. **Aplicar migraciones**:
   ```bash
   python manage.py migrate
   ```

5. **Iniciar el servidor de desarrollo**:
   ```bash
   python manage.py runserver
   ```

## Personalización

Este proyecto utiliza el paquete `django-admin-interface` para personalizar la interfaz de administración de Django. Puedes instalarlo ejecutando:
```bash
pip install django-admin-interface
