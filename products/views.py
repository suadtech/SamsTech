from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Product, Category

def all_products(request):
    """Display all products with search and filtering for SamTech."""
    products = Product.objects.all()
    
    # Search functionality - customers can search for iPhone, Samsung, etc.
    search_query = request.GET.get('search')
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(sku__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    # Category filtering - separate Apple LCDs from Samsung parts
    category = request.GET.get('category')
    if category:
        products = products.filter(category=category)
    
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
        'total_products': products.count(),
    }
    
    return render(request, 'products/products.html', context)

def product_detail(request, product_id):
    """Display individual product details."""
    from django.shortcuts import get_object_or_404
    product = get_object_or_404(Product, id=product_id)
    
    context = {
        'product': product,
    }
    
    return render(request, 'products/product_detail.html', context)
