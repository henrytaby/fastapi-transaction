# FastAPI - Transaction System

API REST para un sistema de transacciones desarrollado con FastAPI y Python.

Este proyecto permite gestionar clientes, planes y transacciones, así como sus relaciones, proporcionando una interfaz robusta y documentada.

## Características

- **Gestión de Clientes (Customers):** Crear, leer, actualizar y eliminar clientes.
- **Gestión de Planes (Plans):** Administración de planes de servicio.
- **Gestión de Transacciones (Transactions):** Registro y consulta de transacciones.
- **Relaciones:**
  - Asignación de planes a clientes.
  - Registro de transacciones asociadas a un cliente.
- **Seguridad:** Autenticación básica (HTTPBasic) en endpoints de verificación.
- **Logging:** Sistema de registro de logs para auditoría y errores.

## Instalación

Sigue estos pasos para configurar el proyecto en tu entorno local utilizando un entorno virtual (`venv`).

### Prerrequisitos

- Python 3.8 o superior

### Pasos

1. **Clonar el repositorio**

   ```bash
   git clone <URL_DEL_REPOSITORIO>
   cd fastapi-transaction
   ```

2. **Crear el entorno virtual**

   ```bash
   python -m venv venv
   ```

3. **Activar el entorno virtual**

   - En **Windows**:
     ```bash
     .\venv\Scripts\activate
     ```
   - En **macOS/Linux**:
     ```bash
     source venv/bin/activate
     ```

4. **Instalar dependencias**

   ```bash
   pip install fastapi uvicorn sqlmodel
   # O si tienes un archivo de requerimientos:
   # pip install -r requirements.txt
   ```

## Ejecución

Para iniciar el servidor de desarrollo:

```bash
uvicorn app.main:app --reload
```

El servidor estará disponible en `http://127.0.0.1:8000`.

## Documentación

Puedes acceder a la documentación interactiva generada automáticamente:

- **Swagger UI:** `/docs`
- **ReDoc:** `/redoc`

## License

MIT