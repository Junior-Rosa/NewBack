
from ..models import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from ..forms import *
from django.urls import reverse_lazy
from django.contrib import messages
from ..utils.math_customer import get_percentage_of_active_customers, confirmed_orders_per_month, top_products_sales
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q, Avg

class CustomerListView(LoginRequiredMixin, ListView):
    model = Customer
    template_name = 'customers/customer_list.html'
    context_object_name = 'customers'
    paginate_by = 20
    
    
    def get_queryset(self):
        queryset = Customer.objects.all()

        # Busca genérica (ex: nome ou email do usuário)
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(user__first_name__icontains=search) |
                Q(user__last_name__icontains=search) |
                Q(user__email__icontains=search)
            )

        # Filtro por cidade
        city = self.request.GET.get('city')
        if city:
            queryset = queryset.filter(address__city__iexact=city)

        # Filtro por status (ativo ou não)
        status = self.request.GET.get('status')
        if status == 'active':
            queryset = queryset.filter(active=True)
        elif status == 'inactive':
            queryset = queryset.filter(active=False)

        return queryset
    
    
    def get_context_data(self, **kwargs):
        
        
        context = super().get_context_data(**kwargs)
        
        thirty_days_ago = timezone.now() - timedelta(days=30)
        
        
        total_customers = Customer.objects.count()
        active_customers = Customer.objects.filter(active=True).count()
        recent_active_customers = Customer.objects.filter(
            active=True,
            user__date_joined__gte=thirty_days_ago
        ).count()
        
        context['cities'] = Customer.objects \
            .exclude(address__city__isnull=True) \
            .exclude(address__city__exact='') \
            .values_list('address__city', flat=True) \
            .distinct()
        
        
        context['search'] = self.request.GET.get('search', '')
        context['city'] = self.request.GET.get('city', '')
        context['status'] = self.request.GET.get('status', '')
        
        context['active_customers_percent'] = get_percentage_of_active_customers(total_customers, active_customers)
        context['active_customers'] = active_customers
        context['recent_customers'] = recent_active_customers
        context['avg_ticket'] = Order.objects.aggregate(Avg('confirmed_total'))['confirmed_total__avg'] or 0
        print(context)
        
        return context
    
    

class CustomerDetailView(LoginRequiredMixin, DetailView):
    model = Customer
    template_name = 'customers/customer_detail.html'
    context_object_name = 'customer'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orders'] = Order.objects.filter(customer=self.object).order_by('-order_date')
        context['pending_orders'] = Order.objects.filter(status='pending').count()
        context['total_spent'] = sum(order.subtotal for order in context['orders'])
        context['monthly_total'] = sum(order.subtotal for order in context['orders'] if order.order_date >= timezone.now() - timedelta(days=30))
        context.update(confirmed_orders_per_month(Order, self.object))
        context['top_products'] = top_products_sales(OrderItem, self.object)
        return context

class CustomerCreateView(LoginRequiredMixin, CreateView):
    model = Customer
    form_class = CustomerCreateForm
    template_name = 'customers/customer_form.html'
    success_url = reverse_lazy('comercial:customer_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Cliente criado com sucesso!')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Erro ao criar cliente. Verifique os dados informados.')
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Novo Cliente'
        context['subtitle'] = 'Preencha os dados para cadastrar um novo cliente'
        return context

class CustomerUpdateView(LoginRequiredMixin, UpdateView):
    model = Customer
    template_name = 'customers/customer_form.html'
    success_url = reverse_lazy('comercial:customer_list')
    
    def get_form_class(self):
        return CustomerUpdateForm
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Cliente'
        context['subtitle'] = f'Editando dados de {self.object.user.get_full_name()}'
        context['is_edit'] = True
        return context
    
    def form_valid(self, form):
        messages.success(self.request, 'Cliente atualizado com sucesso!')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Erro ao atualizar cliente. Verifique os dados informados.')
        return super().form_invalid(form)