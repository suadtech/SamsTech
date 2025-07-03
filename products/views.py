from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages

from .models import Product, Category # Ensure Category is imported

def all_products(request):
    """Display all products with search, filtering, and sorting for SamTech."""
    products = Product.objects.all()
    current_category_obj = None 
    category_name_from_url = request.GET.get('category')
   
   

    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        if not search_query.strip():
            messages.error(request, "You didn't enter any search criteria!")
            return redirect('products:products')

        products = products.filter(
            Q(name__icontains=search_query) |
            Q(sku__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    # Category filtering (SIMPLIFIED for single category match)
   
    if category_name_from_url:
        # Filter products where their 'category' CharField EXACTLY matches the URL parameter
        products = products.filter(category=category_name_from_url)
        
        # Try to get the Category object for display purposes
        try:
            current_category_obj = Category.objects.get(name=category_name_from_url)
        except Category.DoesNotExist:
            current_category_obj = None # Category not found in Category model
            messages.warning(request, f"Category '{category_name_from_url}' not recognized.")
        
        # If no products found for the selected category, show a message
        if not products.exists():
            messages.info(request, f"No products found in category: {category_name_from_url}")
    
    # Sorting functionality
    current_sort = request.GET.get('sort', 'id') # Default sort by 'id'
    sort_options = {
        'id': 'Default (ID)',
        'name': 'Name (A-Z)',
        '-name': 'Name (Z-A)',
        'price': 'Price (Low to High)',
        '-price': 'Price (High to Low)',
        'rating': 'Rating (Low to High)',
        '-rating': 'Rating (High to Low)',
        'created_at': 'Oldest First',
        '-created_at': 'Newest First',
    }
    current_sort_display = sort_options.get(current_sort, 'Default (ID)')

    if current_sort in sort_options: # Only apply valid sorts
        products = products.order_by(current_sort)

    # Pagination
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Context for template
    context = {
        'products': page_obj,
        'categories': Category.objects.all(), # All categories for the filter dropdown
        'current_search': search_query or '',
        'current_category': category_name_from_url or '', # The raw category string from URL
        'current_category_obj': current_category_obj, # The single Category object for display
        'current_sort': current_sort,
        'current_sort_display': current_sort_display,
        'total_products': products.count(),
    }
    
    return render(request, 'products/products.html', context)

def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    context = {'product': product}
    return render(request, 'products/product_detail.html', context)

