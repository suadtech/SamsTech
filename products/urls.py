from django.urls import path
from . import views



urlpatterns = [
    # Updated to use function-based views instead of class-based views
    path('', views.all_products, name='products'),
    path('', views.all_products, name='product_list'),
    path('<int:product_id>/', views.product_detail, name='product_detail'),
    path('add/', views.add_product, name='add_product'),
    path('edit/<int:product_id>/', views.edit_product, name='edit_product'),
    path('delete/<int:product_id>/', views.delete_product, name='delete_product'),


    # Keep these if you have them implemented, otherwise comment out
    # path('category/<str:category_name>/', views.category_products, name='category'),
    # path('search/', views.search_view, name='search'),
    # path('categories/', views.category_tree_view, name='category_tree'),
    # path('ajax/search/', views.ajax_product_search, name='ajax_search'),
    # path('ajax/category/<int:category_id>/', views.ajax_category_products, name='ajax_category_products'),
]

