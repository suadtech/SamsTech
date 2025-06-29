from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.ProductListView.as_view(), name='product_list'),
    path('product/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('category/<str:category_name>/', views.CategoryProductListView.as_view(), name='category'),
    path('search/', views.search_view, name='search'),
    path('categories/', views.category_tree_view, name='category_tree'),
    path('ajax/search/', views.ajax_product_search, name='ajax_search'),
    path('ajax/category/<int:category_id>/', views.ajax_category_products, name='ajax_category_products'),
]
