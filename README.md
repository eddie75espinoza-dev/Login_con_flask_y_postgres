# Login con Flask, PostgreSQL (Backend)

Implementación de **backend** para login con Flask y PostgreSQL.


Repositorio incluye CI/CD con **GitHub** _Actions_.

Ejecutar consultas Postman u otra herramienta similar. 


## Entorno Virtual

Ejecute bajo un entorno virtual.

### Comandos relacionados con la gestión de entornos virtuales
Crear un entorno virtual nuevo.

En Windows, y asumiendo que Python está incluido dentro de las variables del sistema:
```bash
C:\>python -m venv c:\ruta\al\entorno\virtual
```

En macOS y Linux:
```bash
$ python -m venv ruta/al/entorno/virtual
```

Es recomendado que la carpeta para el entorno virtual sea una subcarpeta del proyecto Python al que está asociado.

### Activar un entorno virtual

En Windows:
```bash
C:\>.\ruta\al\entorno\virtual\scripts\activate
```

En macOS y Linux:
```bash
$ source ruta/al/entorno/virtual/bin/activate
```

Sea cual sea nuestro sistema operativo sabremos que el entorno virtual se ha activado porque su nombre aparece entre paréntesis delante del promt.

### Desactivar un entorno virtual
Este comando es idéntico para Windows, macOS y Linux:

```bash
$ deactivate
```

### Eliminar un entorno virtual
En Windows:
```bash
C:\>rmdir c:\ruta\al\entorno\virtual /s
```

En macOS y Linux:
```bash
$ rm -rf ruta/al/entorno/virtual
```

## APP

La app tiene 3 puntos de entrada:

- /new_user 'POST' para registrar nuevos usuarios.
- /login 'POST' para generar un token al validar als credenciales de usuario.
- /protegido 'GET' ingreso a la ruta solo con el token autorizado.