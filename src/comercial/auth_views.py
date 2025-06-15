from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import CreateView,FormView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.views.generic import DetailView, UpdateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib.auth import get_user_model
from .models import Customer, Employee, Order

User = get_user_model()

class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'auth/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('comercial:dashboard')
    
    def form_valid(self, form):
        messages.success(self.request, f'Bem-vindo, {form.get_user().get_full_name() or form.get_user().username}!')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Credenciais inválidas. Tente novamente.')
        return super().form_invalid(form)

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('auth:login')
    
    def dispatch(self, request, *args, **kwargs):
        messages.info(request, 'Você foi desconectado com sucesso.')
        return super().dispatch(request, *args, **kwargs)

class RegisterView(CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = 'auth/register.html'
    success_url = reverse_lazy('auth:login')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Conta criada com sucesso! Faça login para continuar.')
        return response
    
    def form_invalid(self, form):
        messages.error(self.request, 'Erro ao criar conta. Verifique os dados informados.')
        return super().form_invalid(form)



# Profile Views

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'auth/profile_edit.html'
    success_url = reverse_lazy('profile')
    
    def get_form_class(self):
        from .forms import ProfileUpdateForm
        return ProfileUpdateForm
    
    def get_object(self):
        return self.request.user
    
    def form_valid(self, form):
        messages.success(self.request, 'Perfil atualizado com sucesso!')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Erro ao atualizar perfil. Verifique os dados informados.')
        return super().form_invalid(form)


class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'auth/profile_detail.html'
    context_object_name = 'profile_user'
    
    def get_object(self):
        return self.request.user
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Verificar se o usuário é um cliente
        try:
            customer = Customer.objects.get(user=self.request.user)
            context['customer'] = customer
            
            # Estatísticas do cliente
            from datetime import datetime, timedelta
            from django.db.models import Sum, Count
            
            orders = Order.objects.filter(customer=customer)
            context['total_orders'] = orders.count()
            context['total_spent'] = orders.aggregate(
                total=Sum('total_amount')
            )['total'] or 0
            
            # Pedidos dos últimos 30 dias
            thirty_days_ago = datetime.now() - timedelta(days=30)
            context['recent_orders'] = orders.filter(
                order_date__gte=thirty_days_ago
            ).order_by('-order_date')[:5]
            
            # Status dos pedidos
            context['pending_orders'] = orders.filter(
                status__in=['pending', 'processing']
            ).count()
            
            context['completed_orders'] = orders.filter(
                status='delivered'
            ).count()
            
        except Customer.DoesNotExist:
            context['customer'] = None
        
        # Verificar se o usuário é um funcionário
        try:
            employee = Employee.objects.get(user=self.request.user)
            context['employee'] = employee
        except Employee.DoesNotExist:
            context['employee'] = None
        
        return context
    
    
class CustomPasswordChangeView(PasswordChangeView):
    success_url = reverse_lazy('auth:profile')
    template_name = 'auth/profile_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile_user'] = self.request.user  # Adiciona o profile_user ao contexto
        return context  

    def form_valid(self, form):
        messages.success(self.request, "Senha alterada com sucesso.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Erro ao alterar a senha.")
        return super().form_invalid(form)