from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, View
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin

from ..models import Product
from ..forms import ProductForm


class StockUpdateView(View):
    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        operation = request.POST.get('operation')
        reason = request.POST.get('reason', '').strip()

        try:
            quantity = int(request.POST.get('quantity'))
        except (ValueError, TypeError):
            messages.error(request, "Quantidade inválida.")
            return redirect('comercial:product_detail', pk=product.pk)

        if operation == 'add':
            product.stock += quantity
            messages.success(request, f"{quantity} unidade(s) adicionada(s) ao estoque.")
        elif operation == 'remove':
            if quantity > product.stock:
                messages.error(request, "A quantidade a remover excede o estoque atual.")
                return redirect('comercial:product_detail', pk=product.pk)
            product.stock -= quantity
            messages.success(request, f"{quantity} unidade(s) removida(s) do estoque.")
        elif operation == 'set':
            product.stock = quantity
            messages.success(request, f"Estoque definido como {quantity} unidade(s).")
        else:
            messages.error(request, "Operação inválida.")
            return redirect('comercial:product_detail', pk=product.pk)

        product.save()


        return redirect('comercial:product_detail', pk=product.pk)
class ProductListView(ListView):
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Product.objects.all()
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) | Q(description__icontains=search)
            )
        return queryset

class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'

class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/product_form.html'
    success_url = reverse_lazy('comercial:product_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Produto criado com sucesso!')
        return super().form_valid(form)

class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/product_form.html'
    success_url = reverse_lazy('comercial:product_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Produto atualizado com sucesso!')
        return super().form_valid(form)