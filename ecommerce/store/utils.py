'''
Este es un archivo creado por Kristhel Quesada
Nace bajo la necesidad de no repetir el codigo
que se muestra a continuacion. El cual se encar-
ga de la logica de los cookies, almacenamiento
de datos cuando un usuario no esta loggeado, etc.
'''

import json
from . models import Product, Order


def cookieCart(request):
    # Esto para inicializar el formato de la cantidad
    # de compras, en modo de cookies.
    try:
        cart = json.loads(request.COOKIES['cart'])
    except Exception:
        cart = {}

    print('Cart:', cart)
    items = []
    order = {
        'get_cart_total': 0,
        'get_cart_items': 0,
        'shipping': False
    }
    cartItems = order['get_cart_items']

    # Se encarga de desplegar el numero de items
    # total de compra cuando el usuario no esta
    # loggeado. Donde i es el item del carrito
    for i in cart:
        try:
            cartItems += cart[i]["quantity"]

            product = Product.objects.get(id=i)
            total = (product.price * cart[i]["quantity"])

            order['get_cart_total'] += total
            order['get_cart_items'] += cart[i]["quantity"]

            item = {
                'product': {
                    'id': product.id,
                    'name': product.name,
                    'price': product.price,
                    'imageURL': product.imageURL,
                    },
                'quantity': cart[i]["quantity"],
                'get_total': total
                }

            items.append(item)

            if product.digital is False:
                order['shipping'] = True
        except Exception:
            pass

    return {
        'cartItems': cartItems,
        'order': order,
        'items': items
    }

# esto es para almacenar los datos o productos
# que se van agregando al carrito. Se crea bajo
# la necesidad de que cuando naveguemos por la
# pagina, para cada url se almacene siempre
# igual que para el caso anterior.


def cartData(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer,
            complete=False
        )
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']

    return {
        'cartItems': cartItems,
        'order': order,
        'items': items
    }
