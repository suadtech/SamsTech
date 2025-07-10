# Add these two lines
from django.views.generic.base import RedirectView
from django.contrib.staticfiles.storage import staticfiles_storage

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
   
   
path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('images/favicon.ico'))),

    
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', include('home.urls')),
    path('products/', include('products.urls')),
    path('bag/', include('bag.urls')),
    path('checkout/', include('checkout.urls')),
    path('profile/', include('profiles.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


