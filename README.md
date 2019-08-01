# Seol
1) Crear un ambiente virtual para el proyecto (Recomendado)
2) Clonar el proyecto en el ambiente virtual creado anteriormente
3) Ingresar al proyecto hasta la carpeta _datos_iniciales y copiar el archivo secrets.json en la carpeta raíz del proyecto django
    En el archivo secrets.json se encuentra la configuración de conexión a la BD. Se deben modificar los valores que correspondan del archivo para que el proyecto se pueda conectar a la base de datos que usted defina. La base de datos por defecto que se sugiere es reserva_espacios.
4) Copiar el archivo settings.py ubicado en la carpeta _datos_iniciales dentro de la carpeta 'reserva_espacios' ubicada dentro de la carpeta raíz del proyecto django
5) Ejecutar el siguiente comando para instalar los paquetes inciales del proyecto ubicados en el archivo requirements.txt
    pip install -r requirements.txt
6) Debido a que las carpetas migrations de las apps del proyecto se ignoran en el seguimiento que realiza git, es necesario crear para cada app una carpeta denominada migrations y dentro de esta un archivo denominado __ init __.py
    Nota: Esto se debe realizar cada vez que se clona el proyecto o que por alguna razón no esten estas carpetas en las apps del proyecto django
7) Ejecutar los siguientes comandos para efectuar los cambios realizados en los modelos a la base de datos
    python manage.py makemigrations
    python manage.py migrate   
8) Por último, para correr el proyecto ejecutar el siguiente comando:
    python manage.py runserver

9) Como el settings no se sube al repositorio, cada vez que alguien haga alguna modificación en el settings debe informas a los demás

    