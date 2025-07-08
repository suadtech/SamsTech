from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from django.db.models.functions import Lower
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import ProductForm

from .models import Product, Category # Ensure Category is imported

def all_products(request):
    """Display all products with search, filtering, and sorting for SamTech."""
    products = Product.objects.all()
    current_category_obj = None 
    category_name_from_url = request.GET.get('category')

    
    
    # Define aggregate categories and their sub-categories
    # The keys here MUST match the 'name' field in your Category model for these aggregate categories
    aggregate_categories = {
        'All LCDs': ['Apple LCDs', 'Samsung LCDs', 'Other LCDs'],

        'All Parts': [
            'Batteries', 'Back Camera', 'Front Camera', 'Charging Ports & Flex',
            'LCDs Main Flex', 'Home Button', 'Power/Volume Flex', 'Back Camera Lens',
            'Sim Tray', 'Ear/Loud Speaker'
        ],
        'ACCESSORIES': [ # This is an aggregate category in your categories.json
            'Tempered Glass', 'Power Adapters', 'Audio', 'Car Accessories',
            'Power Banks', 'Other Accessories'
        ],
        'All Cases & Covers': [
            'iPhones Cases & Covers', 'Samsung Galaxy Cases & Covers', 'Original Anti Burst Case',
            'Clear TPU Gel Cases', 'Black GEL TPU Cases', 'Book Cases', 'MagSafe Clear Cases',
            'Ring Armor Cases', 'Kids Cases', 'Tap Leather Cases', 'Other Cases'
        ],
        # Add other aggregate categories if you have them, e.g., 'SPECIAL OFFERS'
        # 'SPECIAL OFFERS': ['New Arrivals', 'Deals', 'Clearance'],
    }

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
    
    # Category filtering logic
    if category_name_from_url:
        # Check if it's an aggregate category
        if category_name_from_url in aggregate_categories:
            sub_categories_to_filter = aggregate_categories[category_name_from_url]
            
            products = products.filter(category__in=sub_categories_to_filter)
            
            # Try to get the Category object for the aggregate category for display
            try:
                current_category_obj = Category.objects.get(name=category_name_from_url)
            except Category.DoesNotExist:
                current_category_obj = None 
                messages.warning(request, f"Aggregate Category '{category_name_from_url}' not recognized in Category model.")
        else: # It's a single, specific category
            
            products = products.filter(category=category_name_from_url)
            
            # Try to get the Category object for display purposes
            try:
                current_category_obj = Category.objects.get(name=category_name_from_url)
            except Category.DoesNotExist:
                current_category_obj = None 
                messages.warning(request, f"Category '{category_name_from_url}' not recognized.")
        
        # If no products found for the selected category (or aggregate), show a message
        if not products.exists():
            messages.info(request, f"No products found in category: {category_name_from_url}")

    # Enhanced Sorting functionality (Following tutorial approach)
    sort = None
    direction = None
    sortkey = None
    current_sorting = None

    # Get sort and direction parameters
    if 'sort' in request.GET:
        sortkey = request.GET['sort']
        sort = sortkey
        
        # Handle case-insensitive sorting for name field
        if sortkey == 'name':
            sortkey = 'lower_name'
            products = products.annotate(lower_name=Lower('name'))
        
        # Handle direction parameter
        if 'direction' in request.GET:
            direction = request.GET['direction']
            if direction == 'desc':
                sortkey = f'-{sortkey}'
        
        # Apply the sorting
        products = products.order_by(sortkey)
        
        # Create current_sorting string for template
        current_sorting = f'{sort}_{direction}' if direction else f'{sort}_asc'
    else:
        # Fallback to existing sort parameter for backward compatibility
        current_sort = request.GET.get('sort', 'id')
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
        
        if current_sort in sort_options:
            products = products.order_by(current_sort)
        
        current_sorting = 'none_none'

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
        'current_sort': current_sort if 'sort' not in request.GET else sort,
        'current_sort_display': current_sort_display if 'sort' not in request.GET else None,
        'current_sorting': current_sorting,  # New variable for enhanced sorting
        'total_products': products.count(),
    }
    
    return render(request, 'products/products.html', context)

def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    context = {'product': product}
    return render(request, 'products/product_detail.html', context)
@login_required
def add_product(request):
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, 'Successfully added product!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to add product. Please ensure the form is valid.')
    else:
        form = ProductForm()
        
    template = 'products/add_product.html'
    context = {'form': form}
    return render(request, template, context)

@login_required
def edit_product(request, product_id):
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated product!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to update product. Please ensure the form is valid.')
    else:
        form = ProductForm(instance=product)
        messages.info(request, f'You are editing {product.name}')

    template = 'products/edit_product.html'
    context = {'form': form, 'product': product}
    return render(request, template, context)

@login_required
def delete_product(request, product_id):
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    messages.success(request, 'Product deleted!')
    return redirect(reverse('products'))

