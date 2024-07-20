'''
Archivo creado inicialmente por Django
Modificado despues de la linea 13 por mi persona.
En este se crean los modelos de la pagina, como por
ejemplo los productos e informacion pertinente a ellos.
'''

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
# import uuid # se iba a importar para generar ids unicos

# Create your models here.
# METODOS INCLUIDOS POR MI PERSONA


class Marca(models.Model):
    brand = models.CharField(
        max_length=100,
        unique=True,
        help_text='Registre una marca.'
    )

    # para retornar un url especifico del modelo
    def get_absolute_url(self):
        return reverse('marca', args=[str(self.id)])

    # string que representa al modelo
    def __str__(self):
        return self.brand


class Estilo(models.Model):
    style = models.CharField(
        max_length=50,
        unique=True,
        help_text='Añada un estilo (Blusa, vestido, pantalon...)'
    )

    # para retornar un url especifico del modelo
    def get_absolute_url(self):
        return reverse('Estilo', args=[str(self.id)])

    # string que representa al modelo
    def __str__(self):
        return self.style


class Customer(models.Model):
    '''
    -user tiene una relacion OneToOneField porque un cliente deberia
    tener un unico user asociado, asi como un user solo debe estar
    asociado a un unico cliente. On_delete activado en cascada para
    eliminar todo lo que este asociado al cliente si este es decide
    borrar su cuenta

    -nombre es un CharField ya que en una entrada de caracteres
    -email se define como CharField ya que por el momento no se
    decidio trabajar con verificacion de email
    -phone se decide como CharField tambien
    '''
    user = models.OneToOneField(
        User,
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=200, null=True, blank=True)
    email = models.CharField(max_length=200, null=True, blank=True)
    phone = models.CharField(
        max_length=8,
        null=True,
        blank=True,
        help_text='Ingrese su numero en formato de 8 digitos.'
    )

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200, null=True)
    price = models.FloatField()
    image = models.ImageField(null=True, blank=True)
    digital = models.BooleanField(default=False, null=True, blank=True)
    estilo = models.ForeignKey(
        Estilo,
        on_delete=models.SET_NULL,
        null=True,
        help_text='Seleccione el o los estilos de este articulo.'
    )
    talla = models.CharField(
        max_length=10,
        null=True,
        blank=True,
        help_text='Agregue la talla de la prenda.'
    )
    marca = models.ForeignKey(
        Marca,
        on_delete=models.SET_NULL,
        null=True,
        help_text='Seleccione la marca de este articulo.'
    )
    description = models.CharField(
        max_length=100,
        null=True,
        help_text='Agregue una descripcion al articulo.'
    )

    def __str__(self):
        return self.name

    # @property nos deja accesar a esto como un atributo
    # mas que como un metodo
    # Esto maneja el error de cuando un objeto no tiene
    # una imagen
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except Exception:
            url = ''
        return url


class Order(models.Model):
    '''
    Customer tiene ForeignKey porque este puede tener multiples
    ordenes pero una orden solo puede tener asociado un cliente
    Complete es un indicador para saber cuando finaliza la orden
    oficialmente.

    Order en una orden, conjunto de items comprados
    '''
    customer = models.ForeignKey(
        Customer,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(
        default=False
    )
    transaction_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.id)

    '''
    El siguiente metodo es para la seccion de shipping
    esta pensado bajo la logica que pueden haber produ-
    tos digitales y fisicos. El metodo revisa si es
    fisico o digital y con base a eso habilita la posi-
    bilidad de hacer ship del producto.
    '''
    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()

        for i in orderitems:
            if i.product.digital is False:
                shipping = True
        return shipping

    '''
    Los dos siguientes metodos es para calcular el total de
    items para una orden al igual que su precio.
    '''

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total


class OrderItem(models.Model):
    '''
    OrderItem es un item o producto dentro de una orden
    Es decir, una sola orden puede tener multiples items
    de compra.
    '''
    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.SET_NULL,
        null=True
    )
    quantity = models.IntegerField(
        default=0,
        null=True,
        blank=True
    )
    date_added = models.DateTimeField(auto_now_add=True)

    ENCARGO_STATUS = (
        ('w', 'En solicitud'),
        ('d', 'Declinado'),
        ('c', 'Encargado'),
    )

    status = models.CharField(
        max_length=1,
        choices=ENCARGO_STATUS,
        blank=True,
        default='w',
        help_text='Estado del producto'
    )

    # Metodo para calcular el total de un item basado en
    # su cantidad
    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total


class ShippingAddress(models.Model):
    customer = models.ForeignKey(
        Customer,
        on_delete=models.SET_NULL,
        null=True
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.SET_NULL,
        null=True
    )
    address = models.CharField(
        'Direccion exacta',
        max_length=200,
        unique=True,
        null=False
    )
    distrito = models.CharField(max_length=200, unique=True, null=False)
    canton = models.CharField(max_length=200, unique=True, null=False)
    provincia = models.CharField(max_length=200, unique=True, null=False)
    zipcode = models.CharField(max_length=200, unique=True, null=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address
