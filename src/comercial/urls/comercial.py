from django.contrib import admin
from django.urls import path, include
from .. import views

app_name = 'comercial'


urlpatterns = [
    # Dashboard
    
    
    # Products
    path('products/', views.ProductListView.as_view(), name='product_list'),
    path('products/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('products/create/', views.ProductCreateView.as_view(), name='product_create'),
    path('products/<int:pk>/edit/', views.ProductUpdateView.as_view(), name='product_edit'),
    path('produtos/<int:pk>/update-stock/', views.StockUpdateView.as_view(), name='update_stock'),
    
    # Customers
    path('customers/', views.CustomerListView.as_view(), name='customer_list'),
    path('customers/<int:pk>/', views.CustomerDetailView.as_view(), name='customer_detail'),
    path('customers/create/', views.CustomerCreateView.as_view(), name='customer_create'),
    path('customers/<int:pk>/edit/', views.CustomerUpdateView.as_view(), name='customer_edit'),
    
    # Orders
    path('orders/', views.OrderListView.as_view(), name='order_list'),
    path('orders/<int:pk>/', views.OrderDetailView.as_view(), name='order_detail'),
    path('orders/create/', views.OrderCreateView.as_view(), name='order_create'),
    path('orders/<int:pk>/edit/', views.OrderUpdateView.as_view(), name='order_edit'),
    path('orders/<int:pk>/update-status/', views.UpdateOrderStatus.as_view(), name='order_update_status'),
    
    # Deliveries
    # path('deliveries/', views.DeliveryListView.as_view(), name='delivery_list'),
    # path('deliveries/<int:pk>/', views.DeliveryDetailView.as_view(), name='delivery_detail'),
    # path('deliveries/<int:pk>/complete/', views.mark_delivery_complete, name='delivery_complete'),
    
    # Employees
    path('employees/', views.EmployeeListView.as_view(), name='employee_list'),
    path('employees/create/', views.EmployeeCreateView.as_view(), name='employee_create'),
    path('employees/<int:pk>/edit/', views.EmployeeUpdateView.as_view(), name='employee_edit'),
    path('employees/<int:pk>/', views.EmployeeDetailView.as_view(), name='employee_detail'),
    
    # Vehicles
    # path('vehicles/', views.VehicleListView.as_view(), name='vehicle_list'),
]
