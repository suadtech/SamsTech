from django.urls import path
from . import views
from .webhooks import webhook
from .views import checkout, checkout_success

urlpatterns = [
    path('', views.checkout, name='checkout'),
    # THIS IS THE FIX: Ensure the name is 'checkout_success'
    path('checkout_success/<order_number>', views.checkout_success, name='checkout_success'),
    path('cache_checkout_data/', views.cache_checkout_data, name='cache_checkout_data'),
    path('wh/', webhook, name='webhook'),
]
