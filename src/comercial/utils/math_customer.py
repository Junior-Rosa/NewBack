from django.db.models.functions import TruncMonth
from django.db.models import Count, Sum, F, DecimalField
import json
from django.utils import timezone

def get_percentage_of_active_customers(total:int, active: int) -> float:
    """
    Calculate the percentage of active customers.
    
    Returns:
        float: Percentage of active customers.
    """

    if total == 0:
        return 0.0

    return round((active / total) * 100, 2)


def orders_count_by_status(orders, status: str) -> int:
    """
    Count the number of orders with a specific status.
    
    Args:
        orders (QuerySet): A queryset of orders.
        status (str): The status to filter by.
        
    Returns:
        int: The count of orders with the specified status.
    """
    return orders.filter(status=status).count() if orders else 0

def confirmed_orders_per_month(order, customer) -> dict:
    
    queryset = order.objects.filter(status='confirmed', confirmed_total__isnull=False)
    
    if customer:
        queryset = queryset.filter(customer=customer)
    
    orders_by_month = (
        queryset
        .annotate(month=TruncMonth('order_date'))
        .values('month')
        .annotate(
            total_orders=Count('id'),
            total_confirmed=Sum('confirmed_total')
        )
        .order_by('month')
    )
    
    monthly_labels = []
    monthly_orders = []
    monthly_totals = []

    for entry in orders_by_month:
        month = entry['month']
        monthly_labels.append(month.strftime('%b/%Y'))
        monthly_orders.append(entry['total_orders'])
        monthly_totals.append(float(entry['total_confirmed'] or 0))

    if not monthly_labels:
        monthly_labels = [(timezone.now()).strftime('%b/%Y')]
        monthly_orders = [0]
        monthly_totals = [0]

    return {
        'monthly_labels': json.dumps(monthly_labels),
        'monthly_orders': json.dumps(monthly_orders),
        'monthly_values': json.dumps(monthly_totals),
    }


def top_products_sales(orders, customer, limit=5):
    
    top_products = (
        orders.objects
        .filter(order__customer=customer, order__status='confirmed')
        .values('product__name')
        .annotate(
            total_quantity=Sum('quantity'),
            total_value=Sum(F('quantity') * F('unit_price'), output_field=DecimalField())
        )
        .order_by('-total_quantity')[:limit]
    )
    return top_products