from django.db import models
from django.utils.translation import gettext_lazy as _
from PIL import Image
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
# Create your models here.


class CustomUser(AbstractUser):
    class Meta:
        db_table = 'user'
        verbose_name = _("Usuário")
        verbose_name_plural = _("Usuários")
        
    @property
    def is_customer(self):
        return hasattr(self, 'customer')

    @property
    def is_employee(self):
        return hasattr(self, 'employee')
    

class Address(models.Model):
    street = models.CharField(max_length=255, verbose_name=_("Rua"))
    number = models.CharField(max_length=20, verbose_name=_("Número"))
    complement = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("Complemento"))
    city = models.CharField(max_length=100, verbose_name=_("Cidade"))
    state = models.CharField(max_length=100, verbose_name=_("Estado"))
    zip_code = models.CharField(max_length=20, verbose_name=_("CEP"))
    country = models.CharField(max_length=100, verbose_name=_("País"))
    
    class Meta:
        db_table = 'address'
        verbose_name = _("Endereço")
        verbose_name_plural = _("Endereços")

class Customer(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='customer', verbose_name=_("Usuário"))
    address = models.ForeignKey(Address, on_delete=models.PROTECT, verbose_name=_("Endereço"))
    active = models.BooleanField(default=True, verbose_name=_("Ativo"))

    def total_amount_spent(self):
        """
        Retorna o total gasto pelo cliente em pedidos confirmados.
        """
        return self.order_set.filter(status='confirmed').aggregate(total=models.Sum('confirmed_total'))['total'] or 0.0
    
    def last_order(self):
        """
        Retorna o último pedido do cliente.
        """
        return self.order_set.filter(status='confirmed').order_by('-order_date').first()
    
    def total_orders_confirmed(self):
        """
        Retorna o total de pedidos feitos pelo cliente.
        """
        return self.order_set.filter(status='confirmed').count()
    
    def __str__(self):
        return self.user.get_full_name()

    class Meta:
        db_table = 'customer'
        ordering = ['user__first_name','user__last_name']
        verbose_name = _("Cliente")
        verbose_name_plural = _("Clientes")
    # @property
    # def active_customers_percentage(cls):
    #     total_customers = cls.objects.count()
    #     if total_customers == 0:
    #         return 0
    #     active_customers = cls.objects.filter(active=True).count()
    #     return (active_customers / total_customers) * 100



class Product(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='products/', blank=True, null=True, default='default.jpg')
    
    
    def save(self, *args, **kwargs):
        # Salva o modelo primeiro
        super().save(*args, **kwargs)


        if self.image:
            self._resize_image()


    def _resize_image(self):
        try:
            image_path = self.image.path
            img = Image.open(image_path)

            max_width = 800
            max_height = 800


            if img.height > max_height or img.width > max_width:
                img.thumbnail((max_width, max_height), Image.ANTIALIAS)
                img.save(image_path)
        except Exception as e:
            # Log ou tratamento de erro, se necessário
            print(f"Erro ao redimensionar imagem: {e}")
            
            
    def is_in_stock(self):
        return self.stock > 0
    
    def update_stock(self, quantity):
        
        if quantity < 0 and abs(quantity) > self.stock:
            raise ValueError("Quantidade insuficiente em estoque.")
        self.stock += quantity
        self.save()
    

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'product'
        verbose_name = _("Produto")
        verbose_name_plural = _("Produtos")
        
class Order(models.Model):
    
    DISCOUNT_TYPE_CHOICES = (
        ('percent', _('Porcentagem')),
        ('amount', _('Valor fixo')),
    )
    
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, verbose_name=_("Cliente"))
    products = models.ManyToManyField(Product, through='OrderItem', verbose_name=_("Produtos"))
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[
        ('pending', _('Pendente')),
        ('confirmed', _('Confirmado')),
        ('cancelled', _('Cancelado')),
    ], default='pending', verbose_name=_("Status"))
    notes = models.TextField(blank=True, null=True, verbose_name=_("Notas"))
    
    delivery_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    discount_type = models.CharField(
        max_length=10,
        choices=DISCOUNT_TYPE_CHOICES,
        default='percent'
    )
    discount_value = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    confirmed_total = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True,
        verbose_name=_("Total Confirmado")
    )
    confirmed_date = models.DateTimeField(
        null=True, blank=True, verbose_name=_("Data de Confirmação")
    )
    
    free_delivery = models.BooleanField(default=False, verbose_name=_("Entrega Grátis"))
    
    @property
    def discount_amount(self):
        if self.discount_type == 'percent':
            return (self.subtotal * self.discount_value) / 100
        elif self.discount_type == 'amount':
            return self.discount_value
        return 0
    
    @property
    def total_amount(self):
        total = self.subtotal + self.delivery_fee - self.discount_amount
        return max(total, 0)
    
    @property
    def subtotal(self):
        return sum(item.total_price for item in self.orderitem_set.all())

    def save(self, *args, **kwargs):
    # Confere se o pedido está sendo confirmado agora
        if self.pk:
            old_status = Order.objects.get(pk=self.pk).status
            if old_status != 'confirmed' and self.status == 'confirmed':
                self.confirmed_total = self.total_amount
                self.confirmed_date = timezone.now()
        else:
            # Novo pedido ainda não confirmado
            if self.status == 'confirmed':
                self.confirmed_total = self.total_amount
                self.confirmed_date = timezone.now()

        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Pedido {self.id} de {self.customer}"

    class Meta:
        verbose_name = _("Pedido")
        verbose_name_plural = _("Pedidos")

class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = 'department'
        verbose_name = _("Departamento")
        verbose_name_plural = _("Departamentos")
    
    
    
class Employee(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='employee', verbose_name=_("Usuário"))
    birthdate = models.DateField(verbose_name=_("Data de Nascimento"))
    departament = models.ForeignKey(Department, on_delete=models.PROTECT, verbose_name=_("Departamento"))
    
    class Meta:
        db_table = 'employee'
        verbose_name = _("Funcionário")
        verbose_name_plural = _("Funcionários")
        ordering = ['user__first_name', 'user__last_name']

class Vehicle(models.Model):
    license_plate = models.CharField(max_length=50, unique=True, verbose_name=_("Placa do Veículo"))
    model = models.CharField(max_length=255, verbose_name=_("Modelo do Veículo"))
    year = models.PositiveIntegerField(verbose_name=_("Ano do Veículo"))
    value = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Valor do Veículo"))
    
    def __str__(self):
        return f"{self.model} ({self.year}) - {self.license_plate}"

    class Meta:
        db_table = 'vehicle'
        verbose_name = _("Veículo")
        verbose_name_plural = _("Veículos")
        ordering = ['-model']
    
class Delivery(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name=_("Pedido"))
    delivery_date = models.DateTimeField(verbose_name=_("Data de Entrega"))
    delivered = models.BooleanField(default=False, verbose_name=_("Entregue"))
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT, verbose_name=_("Funcionário Entregador"))
    vehicle = models.ForeignKey(Vehicle, on_delete=models.PROTECT, verbose_name=_("Veículo Utilizado")) 

    def __str__(self):
        return f"Entrega do Pedido {self.order.id} por {self.employee.first_name} {self.employee.last_name}"

    class Meta:
        db_table = 'delivery'
        verbose_name = _("Entrega")
        verbose_name_plural = _("Entregas")
        ordering = ['-delivery_date']
        
        
class OrderItem(models.Model):
  
    
    
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name=_("Pedido"))
    product = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name=_("Produto"))
    quantity = models.PositiveIntegerField(default=1, verbose_name=_("Quantidade"))
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Preço Unitário"))
    
    @property
    def total_price(self) -> float:
        return self.unit_price * self.quantity
    
    def __str__(self):
        return f"{self.quantity}x {self.product.name} para Pedido {self.order.id}"

    class Meta:
        db_table = 'prod_order'
        verbose_name = _("Item do Pedido")
        verbose_name_plural = _("Itens do Pedido")
        unique_together = ('order', 'product') 

