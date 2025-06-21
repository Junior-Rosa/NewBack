from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from ..models import Employee


class EmployeeListView(LoginRequiredMixin, ListView):
    model = Employee
    template_name = 'employees/employee_list.html'
    context_object_name = 'employees'
    paginate_by = 20

class EmployeeCreateView(LoginRequiredMixin, CreateView):
    model = Employee
    template_name = 'employees/employee_form.html'
    success_url = reverse_lazy('comercial:employee_list')
    context_object_name = 'employee'
