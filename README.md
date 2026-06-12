# Proyecto API de Device Systems
## version 2.0
Este es un proyecto de API REST construido con FastAPI para gestionar dispositivos, que mediante endpoints permite Hacer GET a los siguentes peticiones:
* get users
* get users:id
* get users?role=admin
* get users?is_active=true
* post users
* put user:id
* patch user:id
* delete user:id

### Herramientas utilizadas
* FastAPI
* UVicorn
* SwaggerUI


### Estructura de proyecto

```bash
device_systems_python/
│── app/
│   │── main.py
│   │── data/
│   │   └── users_db.py
│   │── dependencies/
│   │   └── user_dependencies.py
│   │── schemas/
│   │   └── user_schema.py
│   │── routes/
│   │   └── user_routes.py
│   └── services/
│       └── user_service.py
│── requirements.txt
└── README.md
```


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
| PUT    | /users/{id}           | Editar los datos de un usuario |
| PATCH  | /users/{id}           | Editar pacialmente un datos de ususario|
| DELETE | /users/{id}           | Eliminar los datos de un usuario|


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

##### 5. Editar los datos de un usuario
```bash
curl -X PUT "http://localhost:8000/users/1" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "pass54321",
    "role": "user",
    "is_active": false
  }'
```

##### 6. Editar el dato de un usuario
```bash
curl -X PATCH "http://localhost:8000/users/2" \
  -H "Content-Type: application/json" \
  -d '{
       "is_active": true
   }'
```

##### 7. Eliminar un usuario por id
```bash
curl -X DELETE "http://localhost:8000/users/3"
```

##### 8. Crear un nuevo usuario
```bash
curl -X POST "http://localhost:8000/users" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "james",
    "email": "james@example.com",
    "password": "password123",
    "role": "user",
    "is_active": true
  }'
```

##### 9. Respuestas
###### 1: respuesta 200 OK
obtener usuarios
```bash
[
  {
    "id": 1,
    "name": "Juan",
    "email": "juan@example.com",
    "role": "admin",
    "is_active": true
  },
  {
    "id": 2,
    "name": "Maria",
    "email": "maria@example.com",
    "role": "user",
    "is_active": false
  },
  {
    "id": 3,
    "name": "Pedro",
    "email": "pedro@example.com",
    "role": "user",
    "is_active": false
  },
  {
    "id": 5,
    "name": "Luis",
    "email": "luis@example.com",
    "role": "support",
    "is_active": true
  }
]

```

###### 2: respuesta 200 OK
obtener por id
```bash
{
  "id": 2,
  "name": "Maria",
  "email": "maria@example.com",
  "role": "user",
  "is_active": false
}
```

###### 3: respuesta 200 OK
obtener por rol
```bash
{
  "id": 2,
  "name": "Maria",
  "email": "maria@example.com",
  "role": "user",
  "is_active": false
}
```

###### 4: respuesta 200 OK
obtener por is_active
```bash
  {
    "id": 1,
    "name": "Juan",
    "email": "juan@example.com",
    "role": "admin",
    "is_active": true
  },
  {
    "id": 4,
    "name": "Ana",
    "email": "ana@example.com",
    "role": "viewer",
    "is_active": true
  },
  {
    "id": 5,
    "name": "Luis",
    "email": "luis@example.com",
    "role": "support",
    "is_active": true
  }
```
###### 5: respuesta 200 OK
editar datos d usuario
```bash
{
  "id": 1,
  "name": "jhon_doe",
  "email": "jhon@example.com",
  "role": "user",
  "is_active": false
}
```

###### 6: respuesta 200 OK
edicion de dato parcial
```bash
{
  "id": 2,
  "name": "Maria",
  "email": "maria@example.com",
  "role": "user",
  "is_active": true
}
```

###### 7: respuesta 200 OK
eliminar usuario
```bash
{
  "error": false,
  "message": "Usuario con ID 3 eliminado correctamente",
  "status_code": 200
}
```

###### 8: respuesta 200 OK
creacion de ususario
```bash
{
  "id": 6,
  "name": "james",
  "email": "james@example.com",
  "role": "user",
  "is_active": true
}
```

#### 9. Evidencias de capturas
##### 1. Swagger UI

![Swagger UI](/images/SwaggerUI/UI1.png)

##### 2. Metodos en swaggerIU

###### 2.1 Todos los usuarios

![Todos los usuarios](/images/SwaggerUI/get_users.png)

###### 2.2 Usuario por ID

![Usuario por ID](/images/SwaggerUI/get_id.png)


###### 2.3 Crear usuario

![Crear usuario](/images/SwaggerUI/post_user.png)

###### 2.4 Actualizar usuario

![Crear usuario](/images/SwaggerUI/put_user.png)

###### 2.5 Actilizacion parcial de un usuario
![Crear usuario](/images/SwaggerUI/patch_user.png)

###### 2.6 Eliminar usuario
![Crear usuario](/images/SwaggerUI/delete_user.png)

###### 2.7 Error con correo duplicado
![Crear usuario](/images/Errores/error_correo.png)

#### 10. Explicación breve del uso de Depends()
Depends() es una función de FastAPI (y de typing en conjunto con FastAPI) usada para inyección de dependencias.

Su uso principal es:
* Reutilizar lógica común (autenticación, validaciones, acceso a BD).
* Compartir objetos entre rutas (sesiones de BD, cliente HTTP).
* Evitar código repetido.


Ejemplo de validacion de roles:
```bash
def validate_role(role: Optional[str] = Query(default=None)) -> Optional[str]:
    """
    Dependencia para validar el parámetro de filtro 'role' en GET /users.
    Si se pasa un rol inválido, lanza 400.
    """
    if role is not None and role not in ALLOWED_ROLES:
        raise HTTPException(
            status_code=400,
            detail={
                "error": True,
                "message": f"Rol no permitido. Roles válidos: {sorted(ALLOWED_ROLES)}",
                "status_code": 400,
            },
        )
    return role
```

#### 11. Codigo de estados
|Ecenario |Codigo | Mensaje |
|---------|-----------|--------|
|usuario no encontrado| 404 | 'usuario  no encontrado'|
|Vereficar Rol | 400 | 'Rol no permitido' |
|Email duplicado | 400 | 'El correo {email} ya esta registrado' |

#### 12. Reflexion sobre el uso de FastAPI para construir APIs rest

FastAPI es un framework moderno y rápido para construir APIs con Python. Me gustó mucho por su simplicidad y eficiencia. Al usar type hints, FastAPI puede validar automáticamente los datos de entrada y salida, lo que reduce errores y mejora la calidad del código. Además, la documentación automática con Swagger UI es muy útil para probar y entender las APIs. La velocidad de desarrollo es increíble, ya que no necesitas escribir tanta lógica de validación manual. En resumen, FastAPI es una excelente opción para construir APIs modernas y eficientes.


## ------------------------------------------------------------------
# Fase Integracion del SQLALCHEMY


### Capturas

#### Estructura del proyecto
![estrura](/images/fase_3/estructura.png)

#### Base de datos
![database](/images/fase_3/database.png)

#### Swagger IU
![Swagger IU](/images/fase_3/SwIU.png)

#### Endpoints probados
* Metodo GET
![get](/images/fase_3/Get.png)

* Metodo POST
![post](/images/fase_3/post.png)

* Metodo GET ID
![get_id](/images/fase_3/getid.png)

* Metodo PUT
![put](/images/fase_3/put.png)

* Metodo PATCH
![patch](/images/fase_3/patch.png)

* Metodo DELETE
![delete](/images/fase_3/delete.png)


#### Errores controlados
- Error sobre usuario no encontrado
![error 1](/images/fase_3/errors/error1.png)

- Error sobre el formato valido de roles
![error 2](/images/fase_3/errors/error2.png)

- Error sobre correos duplicados
![error 3](/images/fase_3/errors/error3.png)

### Explicacion sobre las diferencios entre SQLAlchemy y Schema Pydantic
SQLAlchemy se encarga de trabajar con la base de datos. Permite crear tablas, guardar información, actualizar registros, eliminarlos y consultar los datos almacenados.

Por otro lado, Pydantic Schema se utiliza para validar la información que recibe o envía la aplicación. Su objetivo es comprobar que los datos tengan el formato correcto antes de ser procesados o enviados al usuario.

### Reflexion final
Durante el desarrollo de este proyecto fue posible comprender mejor cómo organizar una aplicación utilizando diferentes herramientas para cada tarea. También se aprendió la importancia de validar la información antes de almacenarla y de mantener una buena estructura en el código para facilitar su mantenimiento.
#### Link del video de explicacion
https://www.loom.com/share/aeddb09c80c8458786d80b74b000cae2

#### Link parte 2;
https://www.loom.com/share/e7075bf1c1c6493891621e42516b140f
