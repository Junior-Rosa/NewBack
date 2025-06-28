from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, DetailView
# from ..models import Delivery
from django.contrib.auth.decorators import login_required


# class DeliveryListView(LoginRequiredMixin, ListView):
#     model = Delivery
#     template_name = 'deliveries/delivery_list.html'
#     context_object_name = 'deliveries'
#     paginate_by = 20

# class DeliveryDetailView(LoginRequiredMixin, DetailView):
#     model = Delivery
#     template_name = 'deliveries/delivery_detail.html'
#     context_object_name = 'delivery'

# @login_required
# def mark_delivery_complete(request, pk):
#     delivery = get_object_or_404(Delivery, pk=pk)
#     delivery.delivered = True
#     delivery.save()
#     messages.success(request, 'Entrega marcada como concluída!')
#     return redirect('comercial:delivery_detail', pk=pk)