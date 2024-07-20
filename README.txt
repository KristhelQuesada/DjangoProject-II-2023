Kristhel Quesada, C06153

Dentro de esta carpeta se encuentra la pagina web creada. Para ello considere toda
la carpeta llamada ecommerce. A continuacion se le brindan unos MUST DO antes de
realizar cualquier ejecucion, con el fin de que pueda correr el programa con exito.

---------------------------------------------------------------------------------------
IMPORTANTE: La instalacion de virtualenvwrapper fue utilizando la version Python 3.10.12
Verifique la version corriendo el comando: python3 -V
En caso que no lo tenga instalado ejecute: sudo apt install python3.10
Luego, para usar los comando pip3 ejecute: sudo apt install python3-pip
Hasta aca deberia tener todo setteado para proceder.
---------------------------------------------------------------------------------------

Continuando con el primer parrafo...
Para ello se le sugiere crear un virtual environment en caso de que la compatibilidad
de las versiones de los programas que vaya a ejecutar choquen con sus programas existentes.
Para ello proceda a ejecutar los siguientes comandos en la terminal:

sudo pip3 install virtualenvwrapper

Modifique al pie del documento .bashrc lo siguiente (Este es un archivo adjunto usualmente ubicado en su home directory)
export WORKON_HOME=$HOME/.virtualenvs
export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3
export VIRTUALENVWRAPPER_VIRTUALENV_ARGS=' -p /usr/bin/python3 '
export PROJECT_HOME=$HOME/Devel
source /usr/local/bin/virtualenvwrapper.sh

Luego, para aplicar cambios ejecute: source ~/.bashrc
Hasta aca deberia tener instalado lo necesario para crear un entorno virtual.


CREACION DEL ENTORNO VIRTUAL
Para ello ejecute el comando: mkvirtualenv entorno1
(entorno1 es el nombre del entorno virtual, usted puede modificarlo si quiere)


INSTALACION DE DJANGO
Para ello se utilizo la version 4.2 de Django, para instalarla ejecute: python3 -m pip install django~=4.2
Corrobore su instalacion con: python3 -m django --version
Deberia tener un resultado similar a 4.2.7

INFORMACION ADICIONAL
Al crear el entorno virtual deberia aparecer el nombre de al costado izquierdo de su terminal indicando que
esta activo. A mi al crearlo, me lo activo automaticamente, en dado caso que no puede activarlo con el
siguiente comando:
source /home/<usuario>/.virtualenvs/entorno1/bin/activate

notese que se utilizo el nombre de entorno1, pero si usted definio otro sustituyalo en ese mismo campo. En
caso que quisiera desactivar el entorno, nada mas ejecute: deactivate

Por ultimo, instale lo siguiente (dentro del virtual environment): python -m pip install Pillow
Esta ultima para el procesamiento de imagenes.

-----------------------------------------------------------------------------------------------------
PARA EJECUTAR EL CODIGO
Para ejecutar el programa debe posicionarse tal que se encuentre en el directorio donde se encuentra
manage.py. Este se encuentra dentro de la carpeta de ../proyecto/ecommerce/
Una vez estando en el mismo directorio que manage.py ejecute: python3 manage.py runserver
Deberia desplegarse un par de lineas pero primordialmente la direccion: http://127.0.0.1:8000/


-----------------------------------------------------------------------------------------------------
CUENTAS DE SUPERUSUARIO
No estoy muy segura si los usuarios que se crearon son locales, incluyendo mi superusuario, para ingresar
a la pagina de administrador se necesita un super usuario, mi cuenta es la siguiente
username: KristhelQuesada
password: electricA2409

de no funcionar se comprueba que solo se guarda localmente. Entonces proceda a crear su propia cuenta
ejecutando el comando: python3 manage.py createsuperuser

Siga los pasos y con eso ya deberia ser capaz de acceder a la pagina de admin: http://127.0.0.1:8000/admin

Esto seria todo en cuestion de funcionamiento. Una vez ingresado al link deberia ser capaz de acceder a
la pagina. Nada mas tome en cuenta lo visto en el video con relacion a los errores que no pudieron ser
solucionados, mas que todo en el registro de costumer a nivel de admin.

Entonces, solo recuerde que si registra su cuenta aun con un superusuario, si la pagina no le funciona
entonces dirigase al url de admin, vaya a costumer y agregue su usuario, ya con eso le deberia correr
el login para su cuenta.
