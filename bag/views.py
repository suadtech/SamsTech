from django.shortcuts import render, redirect, reverse, HttpResponse, get_object_or_404
from products.models import Product # Import the Product model
from django.contrib import messages # Import messages

# Create your views here.
def view_bag(request):
    """A view that renders the bag contents page"""
    return render(request, 'bag/bag.html')

def add_to_bag(request, item_id):
    """Add a specified quantity of the product to the shopping bag"""

    product = get_object_or_404(Product, pk=item_id) # Get the product object
    quantity = int(request.POST.get('quantity')) # Get quantity from form
    redirect_url = request.POST.get('redirect_url') # Get redirect URL from form (optional)

    bag = request.session.get('bag', {}) # Get the bag from session, or create an empty dict

    if item_id in list(bag.keys()):
        bag[item_id] += quantity # If item already in bag, increment quantity
        messages.success(request, f'Updated {product.name} quantity to {bag[item_id]}')
    else:
        bag[item_id] = quantity # Add new item to bag
        messages.success(request, f'Added {product.name} to your bag')

    request.session['bag'] = bag # Update the session bag

    return redirect(reverse('products:product_detail', args=[item_id])) # Redirect back to product detail
