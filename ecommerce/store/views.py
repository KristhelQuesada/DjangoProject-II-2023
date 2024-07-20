'''
Kristhel Quesada
Este archivo lo crea django por default. Sirve para
renderizar nuestros archivos html, es decir, asociar
dichos archivos a vistas especificas. En palabras mas
sencillas, es el que se encarga de desplegar en panta-
lla como se vera cierto path. Al este mismo, le debemos
asociad un archivo html, tal archivo contiene el design
de la pagina. Este archivo es como decir el link entre
el backend y el frontend (html) del asunto.

La notacion de .models se usa . porque views.py y
models.py estan en el mismo directorio.

Las variables context me permiten utilizar los
atributos de models para desplegarlas directamente
manipulando el html. De manera menos formal, las
varibles context albergan en modo de diccionarios
la informacion que le queremos pasar a una vista especifica.

Si un usuario no esta loggeado entonces la pagina muestra
un error no deseado. Para corregir eso se plantea el else
que crea manualmente un carrito por default. Sin embargo
toda la logica fue transferdia a utils.py pues se necesi-
taba repetir el codigo muchas veces.

Todo lo que tenga que ver con cartData funciona de la
siguiente manera: esto permite que la cantidad de items
agregados al carrito de compras pueda visualizarse en el
path en que nos encontremos
'''

from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
import datetime
from .models import Product, Order, OrderItem, ShippingAddress
from .utils import cartData
# from django.forms import inlineformset_factory
# from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def store(request):
    '''
    Metodo que se encarga de la presentacion de la pagina
    principal de la tienda. Pasa como informacion las variables
    llamadas:
    - data y cartItems: se encargan del manejo de los cookies
    tal que se almacenen los datos de las compras que se realicen
    en dicha pagina.
    - products: que es la informacion de todos los productos dis-
    ponibles.
    '''

    data = cartData(request)
    cartItems = data['cartItems']
    products = Product.objects.all()
    context = {
        'products': products,
        'cartItems': cartItems
    }

    return render(request, 'store/store.html', context)


def cart(request):
    '''
    Metodo que se encarga de pasar la informacion necesaria
    para la vista de el path del carrito de compras.
    '''

    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {
        'items': items,
        'order': order,
        'cartItems': cartItems
    }

    return render(request, 'store/cart.html', context)


@login_required(login_url='login')
def checkout(request):
    '''
    Metodo que se encarga de la vista al querer hacer
    checkout, pasa la informacion necesaria. Asimismo
    el @login_required es una restriccion que le dice
    al programa que solo puede ejecutar este metodo
    si el usuario esta loggeado, de lo contrario, lo
    redirige a la pagina de login.
    '''
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {
        'items': items,
        'order': order,
        'cartItems': cartItems
    }

    return render(request, 'store/checkout.html', context)


def updateItem(request):
    '''
    El siguiente codigo habilita la funcion de agregar elementos
    al carrito desde el homepage con el boton: add to cart
    '''

    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(
        customer=customer,
        complete=False
    )

    orderItem, created = OrderItem.objects.get_or_create(
        order=order,
        product=product
    )

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    # el proceso de ordenar funciona solo para un usuario
    # que se encuentre logeado, pero como hay restriccion
    # entonces siempre deberia ejecutarse
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer,
            complete=False
        )
        total = float(data['form']['total'])
        order.transaction_id = transaction_id

        if total == order.get_cart_total:
            order.complete = True
            order.save()

        # Esto existe para que si el producto es fisico
        # entonces que si se realice el proceso de envio.
        if order.shipping is True:
            ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address=data['shipping']['address'],
                distrito=data['shipping']['distrito'],
                canton=data['shipping']['canton'],
                provincia=data['shipping']['provincia'],
                zipcode=data['shipping']['zipcode'],
            )
    else:
        # Esto nunca se debe imprimir ya que tiene una restriccion
        print('User is not logged in...')

    return JsonResponse('Encargo hecho..', safe=False)


# Vistas para manupulacion del usuario
def registerPage(request):
    '''
    Se encarga de registrar a un usuario. Aca se presenta un error
    que no se pudo solucionar. El ususario se crea pero no se crea
    un costumer como tal, si costumer no existe, hacer login con el
    aunque el user se haya creado, genera un error, pues la cookies
    necesitan de que haya un costumer.
    '''
    if request.user.is_authenticated:
        return redirect('store')
    else:
        form = CreateUserForm()

        if request.method == 'POST':
            form = CreateUserForm(request.POST)

            if form.is_valid():
                form.save()

                # Para desplegar el mensaje de exito
                user = form.cleaned_data.get('username')
                messages.success(
                    request,
                    'Account was created for: ' + user)

                return redirect('login')

        context = {'form': form}
        return render(request, 'store/register.html', context)


def loginPage(request):
    '''
    Se encarga del encvio de informacion para la pagina de login
    '''
    if request.user.is_authenticated:
        return redirect('store')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(
                request,
                username=username,
                password=password
            )

            if user is not None:
                login(request, user)
                return redirect('store')
            else:
                messages.info(request, 'Username or password is incorrect.')

        context = {}
        return render(request, 'store/login.html', context)


def logoutUser(request):
    '''
    Se encarga de cerrar sesion y redirigir a la pagina
    inicial si sucede.
    '''
    logout(request)
    return redirect('store')


# vistas para cada categoria de producto
'''
el codigo es muy repetitivo para cada producto pero basicamente
se obtiene cada objeto mediante la etiqueta que tenga definido
en estilo segun lo haya realizado el administrador. Esa fue la
forma en que evitamos utilizar un modelo para cada producto.
'''


def camisas(request):
    data = cartData(request)
    cartItems = data['cartItems']
    camisas = Product.objects.filter(estilo__style="Shirt")
    context = {
        'cartItems': cartItems,
        'camisas': camisas
    }

    return render(request, 'store/shirts.html', context)


def pantalones(request):
    data = cartData(request)
    cartItems = data['cartItems']
    pantalones = Product.objects.filter(estilo__style="Pant")
    context = {
        'cartItems': cartItems,
        'pantalones': pantalones
    }

    return render(request, 'store/pants.html', context)


def vestidos(request):
    data = cartData(request)
    cartItems = data['cartItems']
    vestidos = Product.objects.filter(estilo__style="Dress")
    order = data['order']
    items = data['items']
    context = {
        'cartItems': cartItems,
        'vestidos': vestidos,
        'order': order,
        'items': items
    }

    return render(request, 'store/dresses.html', context)


# VISTA PARA LA BARRA DE BUSQUEDA
'''
Esta es la vista para cuando uno busca un objeto en la barra
de busqueda, se logro hacerlo por palabras claves mediante el
uso del atributo description del modelo Product, ya que con
la linea 307 decimos que queremos filtrar aquello que en la
descripcion contenga lo que se busco.
'''


def search(request):
    data = cartData(request)
    cartItems = data['cartItems']

    if request.method == 'POST':
        searched = request.POST['searched']
        elementos = Product.objects.filter(description__contains=searched)

        context = {
            'searched': searched,
            'elementos': elementos,
            'cartItems': cartItems
        }
        return render(request, 'store/search.html', context)
    else:
        context = {
            'cartItems': cartItems
        }
        return render(request, 'store/search.html', context)


# VISTA PARA LA LISTA DE PRODUCTOS
def list_products(request):
    '''
    La primer linea del metodo almacena a todos los productos
    los cuales son objetos Modelos, y definido en models.py
    '''
    data = cartData(request)
    cartItems = data['cartItems']

    list_products = Product.objects.all()
    context = {
        'list_products': list_products,
        'cartItems': cartItems
    }

    return render(request, 'store/productos.html', context)


# VISTA PARA UN UNICO PRODUCTO
# el id es basicamente el primary key 'pk' de cada producto
# la cual es asignada automaticamente por Django
def viewProduct(request, product_id):
    product = Product.objects.get(pk=product_id)
    data = cartData(request)
    cartItems = data['cartItems']

    context = {
        'product': product,
        'cartItems': cartItems
    }

    return render(request, 'store/view_product.html', context)


# VISTA PARA LAS ORDENES QUE HA REALIZADO UN USUARIO
def viewOrders(request):
    '''
    user es la variable que almacena al usuario que solicita la
    informacion, es decir, el que se encuentra interactuando con
    la pagina, por ello, se filtran las ordenes tal que solo se
    desplieguen aquellas que esten asociadas al perfil que hace
    request.
    En filter cada __ accede a un nivel, por ejemplo, filtra para
    todos los objetos de OrderItem que en su atributo order, tengan
    por atributo interno customer el atributo interno user igual
    a la variable user que obtuvimos por request. Esto se hace asi
    puesto que cada nivel esta representado por una clase.
    '''
    user = request.user
    orders = OrderItem.objects.filter(order__customer__user=user)
    data = cartData(request)
    cartItems = data['cartItems']

    context = {
        'orders': orders,
        'cartItems': cartItems
    }

    return render(request, 'store/view_orders.html', context)
