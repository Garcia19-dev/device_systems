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

## ------------------------------------------------------------------
# Fase Integracion de migraciones

### Comandos ejecutados
#### iniciar migraciones
```bash
alembic init alembic
```
![alembic init](/images/fase_4/alembic_init.png)

#### Crear primera migracion
```bash
alembic revision --autogenerate -m "create devices and loans tables"
```
* Se creo el archivo de migracion en la carpeta alembic/versions, pero me aparace asi por que yo ya la habia creado anteriormente.

![alembic revision](/images/fase_4/alembic_generate.png)


#### Aplicar migracion
```bash
alembic upgrade head
```
* lo mismo para esta captura, ya que la habia ejecutado anteriormente.
![alembic upgrade](/images/fase_4/alembic_head.png)

#### Verificar migracion
```bash
alembic history
```
![alembic history](/images/fase_4/alembic_his.png)


### Captura de las tablas creadas
![tablas creadas](/images/fase_4/tablas_generadas.png)

### Captura del Swagger
![swagger](/images/fase_4/SwaggerIU.png)

### Captura de la creacion de Usuario, Dispositivo y Prestamo
* Creacion de Usuario
![creacion](/images/fase_4/create_user.png)
* Creacion de Dispositivo
![creacion](/images/fase_4/create_device.png)
* Creacion de Prestamo
![creacion](/images/fase_4/create_loans.png)

### Captura de Filtros aplicados y consulta con join
* Consulta con join de loans
![consulta](/images/fase_4/get_loans_joins.png)
* Filtro por estado activo
![consulta](/images/fase_4/joins_loans_active.png)

### Captura de devolucion de prestamo
* Devolucion de prestamo
![consulta](/images/fase_4/return_loans.png)

### Reflexión sobre la importancia de migraciones, relaciones y consultas avanzadas.
Este proyecto permitió comprender mejor la organización de una aplicación mediante el uso de herramientas específicas para cada capa. Se destacó la importancia de las migraciones para gestionar cambios en la base de datos, así como el valor de definir relaciones claras entre entidades y emplear consultas avanzadas que optimicen el rendimiento.

También se reafirmó la necesidad de validar los datos antes de almacenarlos, y de mantener un código bien estructurado para asegurar su mantenibilidad y escalabilidad a futuro.

## ------------------------------------------------------------------
# Fase Integracion de seguridad y autenticacion

### Estructura del proyecto

![estructura](/images/fase_5/estruc_1.png)
![estructura](/images/fase_5/estruc_2.png)

### Migracion con alembic
![alembic](/images/fase_5/alem_migr.png)
![alembic](/images/fase_5/alem_head.png)

### Registro de usuario
![registro](/images/fase_5/create_user.png)

### Login de usuario mas token generado
![login](/images/fase_5/login_jwt.png)

### El GET /me
![me](/images/fase_5/get_me.png)

### acceso sin token
![acceso sin token](/images/fase_5/get_no_token.png)


### Acceso sin rol permitido
![acceso sin rol](/images/fase_5/role_not.png)

### Captura del Swagger con seguridad
![swagger con seguridad](/images/fase_5/swaggerIU.png)

### Cabeceras de moddleware
![cabeceras](/images/fase_5/middlewares.png)


### Aplicacion del Rite Limit
![rate limit](/images/fase_5/rate_limit.png)


### Explicacion de CORS configurados
Los cors configurados son los siguientes:
* Origen: http://localhost:3000
* Metodos: GET, POST, PUT, DELETE, OPTIONS
* Headers: Content-Type, Authorization
* Expose Headers: Content-Type, 

Explicacion: 
* Origen: http://localhost:3000 - Permite que la aplicacion frontend se conecte al backend solo para esas urls o si lo quieres modificar puedes agregar mas urls o poner todas con ["*"] para permitir todas las urls
* Metodos: GET, POST, PUT, DELETE, OPTIONS - Permite todos los metodos HTTP
* Headers: Content-Type, Authorization - Permite los headers Content-Type y Authorization
* Expose Headers: Content-Type, - Expose los headers Content-Type y Authorization

# reflexion final

La seguridad en APIs REST no es un complemento opcional, sino un pilar fundamental que debe integrarse desde el inicio del desarrollo, porque cada endpoint expuesto representa una puerta de entrada a datos sensibles que debemos proteger. A lo largo de este proceso hemos comprendido que la autenticación con JWT, el control de acceso basado en roles, el rate limiting y el hash seguro de contraseñas no son medidas aisladas, sino capas que trabajan en conjunto para crear un sistema robusto bajo el principio de defensa en profundidad, donde la validación constante de tokens y permisos en cada petición nos recuerda que nunca debemos confiar ciegamente en el cliente. Los errores cometidos —como no enviar correctamente el token en el header `Authorization`, confundir autenticación con autorización o descuidar el rate limiting— nos han enseñado que los detalles aparentemente pequeños tienen grandes implicaciones en la seguridad. Sin embargo, esto es solo el comienzo, porque en producción la seguridad exige HTTPS, monitoreo continuo, logs de auditoría y renovación periódica de claves, reflejando que la seguridad no es un destino sino un proceso evolutivo donde cada decisión de diseño cuenta y donde proteger los datos del usuario no es solo una obligación técnica, sino un compromiso ético que define la confianza depositada en nuestro sistema.
#### Link del video de explicacion
https://www.loom.com/share/aeddb09c80c8458786d80b74b000cae2

#### Link parte 2;
https://www.loom.com/share/e7075bf1c1c6493891621e42516b140f

#### Link parte 3
https://www.loom.com/share/a3d7f8d9d7ba4caf8af19650c7a44c0c

#### Link parte 4;
https://www.loom.com/share/a79e7fcb1776442ba49b550cc334b9db
