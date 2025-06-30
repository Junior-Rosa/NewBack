from django.contrib import admin
from django.utils.html import format_html
from .models import *

@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'display_is_customer','display_is_employee', 'date_joined']
    list_filter = ['is_staff', 'is_superuser', 'date_joined']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    
    @admin.display(boolean=True, description='Cliente')
    def display_is_customer(self, obj):
        return obj.is_customer
    
    @admin.display(boolean=True, description='Funcionário')
    def display_is_employee(self, obj):
        return obj.is_employee

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['street', 'number', 'city', 'state', 'zip_code']
    list_filter = ['city', 'state', 'country']
    search_fields = ['street', 'city', 'zip_code']

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['get_full_name', 'get_email', 'get_address']
    search_fields = ['user__first_name', 'user__last_name', 'user__email']
    
    def get_full_name(self, obj):
        return obj.user.get_full_name()
    get_full_name.short_description = 'Nome Completo'
    
    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email'
    
    def get_address(self, obj):
        return f"{obj.address.street}, {obj.address.number} - {obj.address.city}"
    get_address.short_description = 'Endereço'

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'stock', 'is_in_stock', 'image_preview']
    list_filter = ['stock']
    search_fields = ['name', 'description']
    list_editable = ['price', 'stock']
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover;" />', obj.image.url)
        return "Sem imagem"
    image_preview.short_description = 'Imagem'

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'order_date', 'get_total_items']
    list_filter = ['order_date']
    search_fields = ['customer__user__first_name', 'customer__user__last_name']
    inlines = [OrderItemInline]
    
    def get_total_items(self, obj):
        return obj.orderitem_set.count()
    get_total_items.short_description = 'Total de Itens'

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['get_full_name', 'get_email', 'birthdate', 'department']
    list_filter = ['department', 'birthdate']
    search_fields = ['user__first_name', 'user__last_name', 'user__email']
    
    def get_full_name(self, obj):
        return obj.user.get_full_name()
    get_full_name.short_description = 'Nome Completo'
    
    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email'

# @admin.register(Vehicle)
# class VehicleAdmin(admin.ModelAdmin):
#     list_display = ['license_plate', 'model', 'year', 'value']
#     list_filter = ['year']
#     search_fields = ['license_plate', 'model']

# @admin.register(Delivery)
# class DeliveryAdmin(admin.ModelAdmin):
#     list_display = ['order', 'delivery_date', 'delivered', 'employee', 'vehicle']
#     list_filter = ['delivered', 'delivery_date', 'employee']
#     search_fields = ['order__id', 'employee__user__first_name']
#     list_editable = ['delivered']

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity']
    list_filter = ['order__order_date']
    search_fields = ['product__name', 'order__id']
