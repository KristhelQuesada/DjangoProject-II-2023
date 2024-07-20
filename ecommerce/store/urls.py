'''
Kristhel Quesada
Este archivo no fue creado por Django, sino por mi persona.
Funciona para incluir los URLs asociados a la aplicacion
store. La segunda importacion sirve para incluir las vistas
creadas en el archivo views.py. En resumen, se crean los
URL para cada vista de views.py.
En palabras menos tecnicas, aca se definen los urls que
se escriben en la barra de navegacion.
Notacion
path(<el path que se deplegara en el buscardor>,
<el metodo asociado que definimos en views.py>,
<nombre indicador>)
'''

from django.urls import path
from . import views

urlpatterns = [
    path('', views.store, name='store'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),

    path('list_products/', views.list_products, name='list_products'),
    path('view_orders/', views.viewOrders, name='view_orders'),
    path('view_product/<product_id>', views.viewProduct, name='view_product'),
    path('search/', views.search, name='search'),

    path('login/', views.loginPage, name='login'),
    path('register/', views.registerPage, name='register'),
    path('logout/', views.logoutUser, name='logout'),

    path('shirts/', views.camisas, name='shirts'),
    path('pants/', views.pantalones, name='pants'),
    path('dresses/', views.vestidos, name='dresses'),

    path('update_item/', views.updateItem, name='update_item'),
    path('process_order/', views.processOrder, name='process_order'),
]
