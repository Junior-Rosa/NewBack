from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from ..models import Order, Customer, Product
from django.db import connection

class DashboardView(LoginRequiredMixin, ListView):
    template_name = 'core/dashboard.html'
    context_object_name = 'orders'
    model = Order
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_customers'] = Customer.objects.count()
        context['total_products'] = Product.objects.count()
        context['total_orders'] = Order.objects.count()
        # context['pending_deliveries'] = Delivery.objects.filter(delivered=False).count()
        context['recent_orders'] = Order.objects.order_by('-order_date')[:5]
        
        for query in connection.queries:
            print(query['sql'])
        
        return context
