from django.contrib.admin import AdminSite
from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import timedelta


@staff_member_required
def dashboard_analytics(request):
    from orders.models import Order
    from products.models import Product
    from users.models import CustomUser

    today = timezone.now().date()
    last_30 = today - timedelta(days=30)
    last_7 = today - timedelta(days=7)

    total_revenue = Order.objects.filter(payment_status='paid').aggregate(total=Sum('total'))['total'] or 0
    monthly_revenue = Order.objects.filter(payment_status='paid', created_at__date__gte=last_30).aggregate(total=Sum('total'))['total'] or 0
    weekly_revenue = Order.objects.filter(payment_status='paid', created_at__date__gte=last_7).aggregate(total=Sum('total'))['total'] or 0

    total_orders = Order.objects.count()
    pending_orders = Order.objects.filter(status='pending').count()
    total_users = CustomUser.objects.count()
    total_products = Product.objects.filter(is_active=True).count()
    low_stock = Product.objects.filter(stock__lt=10, is_active=True).count()

    recent_orders = Order.objects.select_related('user').order_by('-created_at')[:10]

    # Daily revenue for chart (last 7 days)
    daily_data = []
    for i in range(6, -1, -1):
        day = today - timedelta(days=i)
        rev = Order.objects.filter(payment_status='paid', created_at__date=day).aggregate(total=Sum('total'))['total'] or 0
        daily_data.append({'day': day.strftime('%a'), 'revenue': float(rev)})

    context = {
        'total_revenue': total_revenue,
        'monthly_revenue': monthly_revenue,
        'weekly_revenue': weekly_revenue,
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'total_users': total_users,
        'total_products': total_products,
        'low_stock': low_stock,
        'recent_orders': recent_orders,
        'daily_data': daily_data,
        'title': 'Analytics Dashboard',
    }
    return render(request, 'admin/analytics_dashboard.html', context)
