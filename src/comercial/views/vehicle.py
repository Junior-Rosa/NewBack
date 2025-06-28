from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
# from ..models import Vehicle



# class VehicleListView(LoginRequiredMixin, ListView):
#     model = Vehicle
#     template_name = 'vehicles/vehicle_list.html'
#     context_object_name = 'vehicles'
#     paginate_by = 20
