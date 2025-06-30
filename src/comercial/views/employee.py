from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, DetailView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from ..models import Employee, Department
from ..forms import EmployeeCreateForm
from django.db.models import Q, Count

class EmployeeListView(LoginRequiredMixin, ListView):
    model = Employee
    template_name = 'employees/employee_list.html'
    context_object_name = 'employees'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = super().get_queryset()
        department = self.request.GET.get('department')
        search = self.request.GET.get('search')

        if department:
            queryset = queryset.filter(departament_id=department)

        if search:
            queryset = queryset.filter(
                Q(user__first_name__icontains=search) |
                Q(user__last_name__icontains=search) |
                Q(user__username__icontains=search)
            )

        return queryset

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Lista de Funcionários'
        context['subtitle'] = 'Gerencie os funcionários da empresa'
        context['total_departments_count'] = Department.objects.count()
        # Pegar departamentos mais a quantidade de funcionários em cada um
        context['departments'] = Department.objects.all().annotate(employee_count=Count('employee'))
        context['total_delivery_employees'] = Employee.objects.filter(departament__name='Entrega').count()
        return context

class EmployeeCreateView(LoginRequiredMixin, CreateView):
    model = Employee
    form_class = EmployeeCreateForm
    template_name = 'employees/employee_form.html'
    success_url = reverse_lazy('comercial:employee_list')
    context_object_name = 'employee'

    def form_valid(self, form):
        messages.success(self.request, 'Funcionario criado com sucesso!')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Erro ao criar funcionario. Verifique os dados informados.')
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Novo Funcionário'
        context['subtitle'] = 'Preencha os dados para cadastrar um novo funcionario'
        return context

class EmployeeUpdateView(LoginRequiredMixin, CreateView):
    model = Employee
    form_class = EmployeeCreateForm
    template_name = 'employees/employee_form.html'
    success_url = reverse_lazy('comercial:employee_list')
    context_object_name = 'employee'

    def form_valid(self, form):
        messages.success(self.request, 'Funcionario atualizado com sucesso!')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Erro ao atualizar funcionario. Verifique os dados informados.')
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Funcionário'
        context['subtitle'] = 'Atualize os dados do funcionario'
        return context

class EmployeeDetailView(LoginRequiredMixin, DetailView):
    model = Employee
    template_name = 'employees/employee_detail.html'
    context_object_name = 'employee'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Detalhes do Funcionário: {self.object.user.get_full_name()}'
        context['subtitle'] = 'Visualize os detalhes do funcionário'
        return context
    
class EmployeeDeleteView(LoginRequiredMixin, DeleteView):
    model = Employee
    template_name = 'employees/employee_delete_confirm.html'
    success_url = reverse_lazy('comercial:employee_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Funcionário deletado com sucesso.')
        return super().delete(request, *args, **kwargs)