'''
Kristhel Quesada
Este es un archivo creado por Django.
Tiene el proposito de permitirnos importar los modelos
creados en ../store/models.py a la pagina del adminisrador.

La primera importacion fue creada por Django
La segunda por mi persona y permite importar los modelos de
las carpetas que tengan por nombre asociado models. El * se
usa para indicar que vamor a importar todos los modelos.

Se iba a usar from .models import * para importar todos los
modelos, pero flake8 alertaba que tenia que especificarlos.
'''

from django.contrib import admin
from .models import Customer, Product, Order, ShippingAddress
from .models import OrderItem, Marca, Estilo

# Register your models here.


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'email', 'phone')


admin.site.register(Customer, CustomerAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'talla', 'estilo', 'marca')
    list_filter = ('estilo', 'talla', 'marca')


admin.site.register(Product, ProductAdmin)


class OrderAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'customer', 'complete', 'date_ordered')


admin.site.register(Order, OrderAdmin)


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'order', 'quantity', 'date_added', 'status')
    list_filter = ('order', 'product', 'status')


admin.site.register(OrderItem, OrderItemAdmin)


class ShipAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'customer', 'order', 'zipcode')


admin.site.register(ShippingAddress, ShipAdmin)


admin.site.register(Marca)


admin.site.register(Estilo)

'''
Si quiere ver como funcionan estos modelos, descomentelos.
Los modelos fueron planteado incialmente para asociar un
url especifico a un tipo de modelo, no obstente se termino
por utilizar un modelo general llamado Product, sin embargo,
ciertas logicas de estos modelos utilizados sirvieron para
terminar darle mas formato y complejidad al producto.

class VestidoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'talla', 'marca', 'display_estilo')
admin.site.register(Vestido, VestidoAdmin)

class BlusaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'talla', 'marca', 'display_estilo')
admin.site.register(Blusa, BlusaAdmin)

class PantalonAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'talla', 'marca', 'display_estilo')
admin.site.register(Pantalon, PantalonAdmin)


admin.site.register(VestidoInstance)
admin.site.register(BlusaInstance)
admin.site.register(PantalonInstance)
'''
