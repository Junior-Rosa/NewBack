from django.shortcuts import redirect
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, View
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from decimal import Decimal
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import connection

import json


from ..models import Order, OrderItem, Customer, Product
from ..forms import OrderForm, OrderUpdateForm



class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'orders/order_list.html'
    context_object_name = 'orders'
    paginate_by = 20
    
    def get_queryset(self):
        return Order.objects.select_related('customer').order_by('-order_date')

class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'orders/order_detail.html'
    context_object_name = 'order'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order_items'] = OrderItem.objects.filter(order=self.object).select_related('product')
        # context['delivery'] = Delivery.objects.filter(order=self.object).first()
        for query in connection.queries:
            print(query['sql'])
        return context


class OrderCreateView(LoginRequiredMixin, CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'orders/order_form.html'
    success_url = reverse_lazy('comercial:order_list')
    
    
    
    
    def form_valid(self, form):
        # Criar o pedido
        order = form.save(commit=False)
        
        # Capturar valores calculados do formulário
        # order.subtotal = Decimal(self.request.POST.get('subtotal', '0'))
        order.discount_percent = Decimal(self.request.POST.get('discount_percent', '0'))
        # order.discount_amount = Decimal(self.request.POST.get('discount_amount', '0'))
        order.delivery_fee = Decimal(self.request.POST.get('delivery_fee', '10'))
        # order.total_amount = Decimal(self.request.POST.get('total_amount', '0'))
        order.free_delivery = self.request.POST.get('free_delivery', 'false') == 'true'
        order.notes = self.request.POST.get('notes', '')
        
        order.save()
        
        # Processar itens do pedido
        products = self.request.POST.getlist('products[]')
        quantities = self.request.POST.getlist('quantities[]')
        
        for product_id, quantity in zip(products, quantities):
            if product_id and quantity:
                try:
                    product = Product.objects.get(id=product_id)
                    quantity = int(quantity)
                    
                    # Verificar estoque
                    if product.stock >= quantity:
                        OrderItem.objects.create(
                            order=order,
                            product=product,
                            quantity=quantity,
                            unit_price=product.price
                        )
                        
                        # Atualizar estoque
                        product.stock -= quantity
                        product.save()
                    else:
                        messages.warning(
                            self.request, 
                            f'Estoque insuficiente para {product.name}. Disponível: {product.stock}'
                        )
                except Product.DoesNotExist:
                    messages.error(self.request, f'Produto com ID {product_id} não encontrado.')
                except ValueError:
                    messages.error(self.request, f'Quantidade inválida: {quantity}')
    
        messages.success(
            self.request, 
            f'Pedido #{order.id} criado com sucesso! Total: R$ {order.total_amount}'
        )
        return redirect('comercial:order_detail', pk=order.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Dados dos clientes para o JavaScript
        customers_data = []
        for customer in Customer.objects.select_related('user', 'address').all():
            customers_data.append({
                'id': customer.id,
                'name': customer.user.get_full_name(),
                'email': customer.user.email,
                'address': f"{customer.address.street}, {customer.address.number} - {customer.address.city}"
            })
        
        # Dados dos produtos para o JavaScript
        products_data = []
        for product in Product.objects.filter(stock__gt=0):
            products_data.append({
                'id': product.id,
                'name': product.name,
                'price': float(product.price),
                'stock': product.stock
            })
        
        context['customers_json'] = json.dumps(customers_data)
        context['products_json'] = json.dumps(products_data)
        context['customers'] = Customer.objects.select_related('user', 'address').all()
        context['products'] = Product.objects.filter(stock__gt=0)
        
        for query in connection.queries:
            print(query['sql'])
        return context


class OrderUpdateView(LoginRequiredMixin, UpdateView):
    model = Order
    template_name = 'orders/order_form.html'
    
    def get_form_class(self):
        return OrderUpdateForm
    
    def get_success_url(self):
        return reverse_lazy('comercial:order_detail', kwargs={'pk': self.object.pk})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Dados dos clientes para o JavaScript
        customers_data = []
        for customer in Customer.objects.select_related('user', 'address').all():
            customers_data.append({
                'id': customer.id,
                'name': customer.user.get_full_name(),
                'email': customer.user.email,
                'address': f"{customer.address.street}, {customer.address.number} - {customer.address.city}"
            })
        
        # Dados dos produtos para o JavaScript (incluir todos os produtos, não só com estoque)
        products_data = []
        for product in Product.objects.all():
            products_data.append({
                'id': product.id,
                'name': product.name,
                'price': float(product.price),
                'stock': product.stock
            })
        
        context['customers_json'] = json.dumps(customers_data)
        context['products_json'] = json.dumps(products_data)
        context['customers'] = Customer.objects.select_related('user', 'address').all()
        context['products'] = Product.objects.all()
        
        # Dados dos itens existentes do pedido
        existing_items = []
        for item in OrderItem.objects.filter(order=self.object).select_related('product'):
            existing_items.append({
                'product_id': item.product.id,
                'quantity': item.quantity,
                'unit_price': float(item.unit_price)
            })
        
        context['existing_items'] = json.dumps(existing_items)
        context['is_edit'] = True
        
        for query in connection.queries:
            print(query['sql'])
        return context
    
    def form_valid(self, form):
        order = form.save(commit=False)
        
        # Capturar valores calculados do formulário
        order.subtotal = Decimal(self.request.POST.get('subtotal', '0'))
        order.discount_percent = Decimal(self.request.POST.get('discount_percent', '0'))
        order.discount_amount = Decimal(self.request.POST.get('discount_amount', '0'))
        order.delivery_fee = Decimal(self.request.POST.get('delivery_fee', '10'))
        order.total_amount = Decimal(self.request.POST.get('total_amount', '0'))
        order.free_delivery = self.request.POST.get('free_delivery', 'false') == 'true'
        order.notes = self.request.POST.get('notes', '')
        
        order.save()
        
        # Restaurar estoque dos itens antigos
        old_items = OrderItem.objects.filter(order=order)
        for old_item in old_items:
            product = old_item.product
            product.stock += old_item.quantity
            product.save()
        
        # Remover itens antigos
        old_items.delete()
        
        # Processar novos itens do pedido
        products = self.request.POST.getlist('products[]')
        quantities = self.request.POST.getlist('quantities[]')
        
        for product_id, quantity in zip(products, quantities):
            if product_id and quantity:
                try:
                    product = Product.objects.get(id=product_id)
                    quantity = int(quantity)
                    
                    # Verificar estoque
                    if product.stock >= quantity:
                        OrderItem.objects.create(
                            order=order,
                            product=product,
                            quantity=quantity,
                            unit_price=product.price
                        )
                        
                        # Atualizar estoque
                        product.stock -= quantity
                        product.save()
                    else:
                        messages.warning(
                            self.request, 
                            f'Estoque insuficiente para {product.name}. Disponível: {product.stock}'
                        )
                except Product.DoesNotExist:
                    messages.error(self.request, f'Produto com ID {product_id} não encontrado.')
                except ValueError:
                    messages.error(self.request, f'Quantidade inválida: {quantity}')
        
        messages.success(
            self.request, 
            f'Pedido #{order.id} atualizado com sucesso! Total: R$ {order.total_amount}'
        )
        return super().form_valid(form)
    
    


class UpdateOrderStatus(LoginRequiredMixin, View):
    def post(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        new_status = request.POST.get('status')
        
        valid_status_choices = [choice[0] for choice in Order._meta.get_field('status').choices]

        if not new_status or new_status not in valid_status_choices:
            messages.error(request, 'Status inválido.')
            return redirect('comercial:order_detail', pk=order.pk)
        
        order.status = new_status
        order.save()
        
        
        messages.success(request, f'Status do pedido atualizado para: {new_status}')
        return redirect('comercial:order_detail', pk=order.pk)

    