from django.urls import path
from . import views
<<<<<<< HEAD
from . import webhooks 
=======

>>>>>>> eb922ec0d8a8b03645b914fd5877800b77e1adad
app_name = 'checkout'

urlpatterns = [
    path('', views.checkout, name='checkout'),
<<<<<<< HEAD
    path('checkout_success/<order_number>', views.checkout_success, name='checkout_success'),
    path('wh/', webhooks.webhook, name='webhook'),
    path('cache_checkout_data/', views.cache_checkout_data, name='cache_checkout_data'),

=======
>>>>>>> eb922ec0d8a8b03645b914fd5877800b77e1adad
]
