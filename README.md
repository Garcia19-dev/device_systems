## Proyecto API de Device Systems

Este es un proyecto de API REST construido con FastAPI para gestionar dispositivos, que mediante endpoints permite Hacer GET a los siguentes peticiones:
* get Users
* get Users:id
* get users?role=admin
* get users?is_active=true
* post users

### Herramientas utilizadas
* FastAPI
* UVicorn
* Postman

### Instalación de dependencias
Las dependencias nos permiten ejecutar el proyecto de forma local, para instalarlas ejecuta los siguientes comandos:

#### 1. Clonar el repocitorio

```bash
git clone https://github.com/Garcia19-Dev/device_systems_python.git
```

#### 2. Verifica que tienes Python instalado

```bash
python --version
```
#### 3. Creacion del entorno virtual

```bash
python -m venv fastapi_env
```
#### 4. Activacion del entorno virtual
Con windows, Command Prompt

```bash
fastapi_env\Scripts\activate.bat
```

con Mac o Linux, Terminal

```bash
source fastapi_env/bin/activate
```

#### 5. Instala las dependencias

```bash
pip install -r requirements.txt
```

#### 6. Ejecutar el proyecto

```bash
python -m uvicorn app.main:app --reload
```

#### 7. Tabla de endpoints

| Método | Endpoint              | Descripción                |
| --------| -----------------------| ----------------------------|
| GET    | /users                | Obtener todos los usuarios |
| GET    | /users/{id}           | Obtener un usuario por ID  |
| GET    | /users?role=admin     | Obtener usuarios por rol   |
| GET    | /users?is_active=true | Obtener usuarios activos   |
| POST   | /users                | Crear un nuevo usuario     |


#### 8. Ejemplos de peticiones

##### 1. Obtener todos los usuarios
```bash
curl -X GET "http://localhost:8000/users"
```

##### 2. Obtener un usuario por ID
```bash
curl -X GET "http://localhost:8000/users/1"
```

##### 3. Obtener usuarios por rol
```bash
curl -X GET "http://localhost:8000/users?role=admin"
```

##### 4. Obtener usuarios activos
```bash
curl -X GET "http://localhost:8000/users?is_active=true"
```

##### 5. Crear un nuevo usuario
```bash
curl -X POST "http://localhost:8000/users" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "password123",
    "role": "user",
    "is_active": true
  }'
```
#### 9. Evidencias de capturas
##### 1. Swagger UI

![Swagger UI](/images/SwaggerUI/image.png)

##### 2. Postman

###### 2.1 Todos los usuarios

![Todos los usuarios](/images/Postman/get_users.png)

###### 2.2 Usuario por ID

![Usuario por ID](/images/Postman/get_by_id.png)

###### 2.3 Usuario por rol

![Usuario por rol](/images/Postman/get_role_admin.png)

###### 2.4 Usuario activo

![Usuario activo](/images/Postman/get_is_true.png)

###### 2.5 Crear usuario

![Crear usuario](/images/Postman/post_new_user.png)

###### 2.6 Error al obtener usuarios

![Error al obtener usuarios](/images/Errores/errores_user.png)

###### 2.7 Error al crear usuario con datos inválidos

![Error al crear usuario con datos inválidos](/images/Errores/errores_create.png)


#### 10. Reflexion sobre el uso de FastAPI para construir APIs rest

FastAPI es un framework moderno y rápido para construir APIs con Python. Me gustó mucho por su simplicidad y eficiencia. Al usar type hints, FastAPI puede validar automáticamente los datos de entrada y salida, lo que reduce errores y mejora la calidad del código. Además, la documentación automática con Swagger UI es muy útil para probar y entender las APIs. La velocidad de desarrollo es increíble, ya que no necesitas escribir tanta lógica de validación manual. En resumen, FastAPI es una excelente opción para construir APIs modernas y eficientes.

