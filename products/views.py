from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.http import JsonResponse
from django.views.generic import ListView, DetailView
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from .models import Product, Category


class ProductListView(ListView):
    """
    Display a list of products with filtering and pagination.
    """
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        """Get filtered and ordered product queryset."""
        queryset = Product.objects.filter(is_active=True).select_related('category')
        
        # Category filtering
        category_name = self.request.GET.get('category')
        if category_name:
            try:
                category = Category.objects.get(name=category_name, is_active=True)
                queryset = Product.get_products_by_category(category)
            except Category.DoesNotExist:
                pass

        # Search filtering
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(sku__icontains=search_query)
            )

        # Price filtering
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')
        if min_price:
            try:
                queryset = queryset.filter(price__gte=float(min_price))
            except ValueError:
                pass
        if max_price:
            try:
                queryset = queryset.filter(price__lte=float(max_price))
            except ValueError:
                pass

        # Rating filtering
        min_rating = self.request.GET.get('min_rating')
        if min_rating:
            try:
                queryset = queryset.filter(rating__gte=int(min_rating))
            except ValueError:
                pass

        # Sorting
        sort_by = self.request.GET.get('sort', 'name')
        if sort_by in ['name', '-name', 'price', '-price', 'rating', '-rating', 'created_at', '-created_at']:
            queryset = queryset.order_by(sort_by)

        return queryset

    def get_context_data(self, **kwargs):
        """Add additional context data."""
        context = super().get_context_data(**kwargs)
        
        # Add categories for filtering
        context['categories'] = Category.objects.filter(
            is_active=True
        ).annotate(
            product_count=Count('products', filter=Q(products__is_active=True))
        ).order_by('name')
        
        # Add current filters to context
        context['current_category'] = self.request.GET.get('category', '')
        context['current_search'] = self.request.GET.get('search', '')
        context['current_sort'] = self.request.GET.get('sort', 'name')
        context['min_price'] = self.request.GET.get('min_price', '')
        context['max_price'] = self.request.GET.get('max_price', '')
        context['min_rating'] = self.request.GET.get('min_rating', '')
        
        # Add price range for filtering
        if Product.objects.filter(is_active=True).exists():
            price_range = Product.objects.filter(is_active=True).aggregate(
                min_price=models.Min('price'),
                max_price=models.Max('price')
            )
            context['price_range'] = price_range

        return context


class ProductDetailView(DetailView):
    """
    Display detailed information about a single product.
    """
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'

    def get_queryset(self):
        """Get product queryset with related data."""
        return Product.objects.filter(is_active=True).select_related('category')

    def get_context_data(self, **kwargs):
        """Add additional context data."""
        context = super().get_context_data(**kwargs)
        
        # Add related products from the same category
        if self.object.category:
            related_products = Product.objects.filter(
                category=self.object.category,
                is_active=True
            ).exclude(
                id=self.object.id
            ).select_related('category')[:4]
            context['related_products'] = related_products

        return context


class CategoryProductListView(ListView):
    """
    Display products for a specific category.
    """
    model = Product
    template_name = 'products/category_products.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        """Get products for the specified category."""
        self.category = get_object_or_404(
            Category, 
            name=self.kwargs['category_name'],
            is_active=True
        )
        
        include_subcategories = self.request.GET.get('include_subcategories', 'true') == 'true'
        queryset = Product.get_products_by_category(self.category, include_subcategories)
        
        # Apply sorting
        sort_by = self.request.GET.get('sort', 'name')
        if sort_by in ['name', '-name', 'price', '-price', 'rating', '-rating']:
            queryset = queryset.order_by(sort_by)

        return queryset

    def get_context_data(self, **kwargs):
        """Add category context data."""
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        context['subcategories'] = self.category.subcategories.filter(is_active=True)
        context['current_sort'] = self.request.GET.get('sort', 'name')
        context['include_subcategories'] = self.request.GET.get('include_subcategories', 'true') == 'true'
        
        # Add breadcrumb navigation
        breadcrumbs = []
        current_category = self.category
        while current_category:
            breadcrumbs.insert(0, current_category)
            current_category = current_category.parent
        context['breadcrumbs'] = breadcrumbs

        return context


@cache_page(60 * 15)  # Cache for 15 minutes
def home_view(request):
    """
    Home page view with featured products and categories.
    """
    context = {
        'featured_products': Product.get_featured_products(),
        'main_categories': Category.objects.filter(
            parent=None,
            is_active=True
        ).annotate(
            product_count=Count('products', filter=Q(products__is_active=True))
        ).order_by('name')[:6],
        'recent_products': Product.objects.filter(
            is_active=True
        ).select_related('category').order_by('-created_at')[:8]
    }
    return render(request, 'products/home.html', context)


def search_view(request):
    """
    Advanced search view with multiple filtering options.
    """
    query = request.GET.get('q', '')
    category_id = request.GET.get('category')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    min_rating = request.GET.get('min_rating')
    sort_by = request.GET.get('sort', 'name')

    products = Product.objects.filter(is_active=True).select_related('category')

    # Text search
    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(sku__icontains=query) |
            Q(category__name__icontains=query) |
            Q(category__friendly_name__icontains=query)
        )

    # Category filter
    if category_id:
        try:
            category = Category.objects.get(id=category_id, is_active=True)
            products = Product.get_products_by_category(category)
        except Category.DoesNotExist:
            pass

    # Price filters
    if min_price:
        try:
            products = products.filter(price__gte=float(min_price))
        except ValueError:
            pass
    if max_price:
        try:
            products = products.filter(price__lte=float(max_price))
        except ValueError:
            pass

    # Rating filter
    if min_rating:
        try:
            products = products.filter(rating__gte=int(min_rating))
        except ValueError:
            pass

    # Sorting
    if sort_by in ['name', '-name', 'price', '-price', 'rating', '-rating', 'created_at', '-created_at']:
        products = products.order_by(sort_by)

    # Pagination
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'products': page_obj,
        'query': query,
        'categories': Category.objects.filter(is_active=True).order_by('name'),
        'current_category': category_id,
        'min_price': min_price,
        'max_price': max_price,
        'min_rating': min_rating,
        'current_sort': sort_by,
        'total_results': products.count()
    }

    return render(request, 'products/search_results.html', context)


def category_tree_view(request):
    """
    Display hierarchical category tree.
    """
    categories = Category.objects.filter(
        parent=None,
        is_active=True
    ).prefetch_related(
        'subcategories__subcategories'
    ).annotate(
        product_count=Count('products', filter=Q(products__is_active=True))
    ).order_by('name')

    context = {
        'categories': categories
    }
    return render(request, 'products/category_tree.html', context)


def ajax_product_search(request):
    """
    AJAX endpoint for product search autocomplete.
    """
    query = request.GET.get('q', '')
    if len(query) < 2:
        return JsonResponse({'products': []})

    products = Product.objects.filter(
        Q(name__icontains=query) | Q(sku__icontains=query),
        is_active=True
    ).select_related('category')[:10]

    results = []
    for product in products:
        results.append({
            'id': product.id,
            'name': product.name,
            'sku': product.sku,
            'price': str(product.price),
            'category': product.category.get_friendly_name() if product.category else '',
            'url': product.get_absolute_url(),
            'image_url': product.get_image_url()
        })

    return JsonResponse({'products': results})


def ajax_category_products(request, category_id):
    """
    AJAX endpoint to get products for a category.
    """
    try:
        category = Category.objects.get(id=category_id, is_active=True)
        products = Product.get_products_by_category(category)[:20]
        
        results = []
        for product in products:
            results.append({
                'id': product.id,
                'name': product.name,
                'price': str(product.price),
                'image_url': product.get_image_url(),
                'url': product.get_absolute_url()
            })
        
        return JsonResponse({
            'products': results,
            'category_name': category.get_friendly_name()
        })
    except Category.DoesNotExist:
        return JsonResponse({'error': 'Category not found'}, status=404)



