from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages

from .models import Product, Category

def all_products(request):
    """Display all products with search and filtering for SamTech."""
    products = Product.objects.all()
    
    # Search functionality - customers can search for iPhone, Samsung, etc.
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
    
    # Category filtering - separate Apple LCDs from Samsung parts
    category = request.GET.get('category')
    if category:
        products = products.filter(category=category) # Keep this as per our last fix
    
    # Sorting functionality
    current_sort = request.GET.get('sort', 'id') # Default sort by 'id'
    sort_options = {
        'id': 'Default (ID)',
        'name': 'Name (A-Z)',
        '-name': 'Name (Z-A)',
        'price': 'Price (Low to High)',
        '-price': 'Price (High to Low)',
        'rating': 'Rating (Low to High)', # Added for completeness
        '-rating': 'Rating (High to Low)',
        '-created_at': 'Newest First',
    }
    current_sort_display = sort_options.get(current_sort, 'Default (ID)') # Get display name

    if current_sort in sort_options: # Only apply valid sorts
        products = products.order_by(current_sort)

    # Pagination - show 12 products per page instead of all 74
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Context for template
    context = {
        'products': page_obj,
        'categories': Category.objects.all(),
        'current_search': search_query or '',
        'current_category': category or '',
        'current_sort': current_sort, # Pass the raw sort value
        'current_sort_display': current_sort_display, # Pass the user-friendly display value
        'total_products': products.count(),
    }
    
    return render(request, 'products/products.html', context)

def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    context = {'product': product}
    return render(request, 'products/product_detail.html', context)
