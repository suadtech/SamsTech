from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.db.models import Q
from django.db.models.functions import Lower
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Product, Category
from .forms import ProductForm

def all_products(request):
    """ A view to show all products, including sorting and search queries """
    products = Product.objects.all()
    query = request.GET.get('q')
    category = request.GET.get('category')
    sort = request.GET.get('sort')
    direction = request.GET.get('direction')

    # This is the CORRECT filtering logic for a CharField
    if category:
        products = products.filter(category=category)

    if query:
        # This prevents the "None" text from being searched
        if query == 'None':
            query = None
        else:
            queries = Q(name__icontains=query) | Q(description__icontains=query)
            products = products.filter(queries)

    if sort:
        if sort == 'name':
            sortkey = 'lower_name'
            products = products.annotate(lower_name=Lower('name'))
        else:
            sortkey = sort

        if direction == 'desc':
            sortkey = f'-{sortkey}'
        products = products.order_by(sortkey)

    # This is the CORRECT way to get the category list for your dropdown
    all_category_names = Product.objects.order_by('category').values_list('category', flat=True).distinct()

    context = {
        'products': products,
        'search_term': query,
        'current_category': category,
        'all_categories': all_category_names, # This is a simple list of strings
        'current_sort': sort,
    }

    return render(request, 'products/products.html', context)

def product_detail(request, product_id):
    """ Show individual product details """
    product = get_object_or_404(Product, pk=product_id)
    context = {
        'product': product,
    }
    return render(request, 'products/product_detail.html', context)

@login_required
def add_product(request):
    """ Add a product to the store """
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
    context = {
        'form': form,
    }
    return render(request, template, context)

@login_required
def edit_product(request, product_id):
    """ Edit a product in the store """
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
    context = {
        'form': form,
        'product': product,
    }
    return render(request, template, context)

@login_required
def delete_product(request, product_id):
    """ Delete a product from the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))
    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    messages.success(request, 'Product deleted!')
    return redirect(reverse('products'))
