from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from ..models import Employee


class EmployeeListView(LoginRequiredMixin, ListView):
    model = Employee
    template_name = 'employees/employee_list.html'
    context_object_name = 'employees'
    paginate_by = 20
