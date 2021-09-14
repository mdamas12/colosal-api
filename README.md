# Levantar el entorno

1. Clonar el proyecto

2. cd rutaPrincipalDelProyecto/

3. El archivo .env.example duplicarlo y quitarle el .example o renombrarlo

5. Escribir en la terminal docker-compose up --build

6. Correr las migraciones con docker-compose run web python manage.py migrate


# Comandos de ayuda

### Comandos de ayuda con docker.

1. Levantar todos los contenedores ``docker-compose up --build``
2. Preparar migraciones ``docker-compose run web python manage.py makemigrations``
3. Correr migraciones ``docker-compose run web python manage.py migrate``
3. Crear carpeta ``docker-compose run web python manage.py startapp nombreCarpeta``

### Crear una carpeta dentro de una carpeta

Vamos a suponer que necesitamos crear dentro de panel la carpeta brand, por ende:

1.    Primero creamos la carpeta brand ``mkdir panel/brand``.
2.    Creamos brands dentro de panel ``docker-compose run web python manage.py startapp brands panel/brands``.
3.    Agregamos brands a INSTALLED_APPS.


```python
    INSTALLED_APPS = [
        'panel.brands'
    ]
```
4.    Preparamos las migraciones ``docker-compose run web python manage.py makemigrations brands``.
5.    Corremos las migraciones ``docker-compose run web python manage.py migrate brands``.
6.    Agregar la ruta a urls.

```python
    urlpatterns = [
        path('brands/',include('panel.brands.urls'),
    ]
```

