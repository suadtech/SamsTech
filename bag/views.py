from django.shortcuts import render, redirect, reverse, HttpResponse, get_object_or_404
from products.models import Product
from django.contrib import messages # Import messages

# Create your views here.

def view_bag(request):
    """ A view that renders the bag contents page """
    return render(request, 'bag/bag.html')


def add_to_bag(request, item_id):
    """ Add a specified quantity of the product to the bag """

    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url') # This line is not used in your provided code, but kept for consistency if you use it later

    bag = request.session.get('bag', {})

    if item_id in list(bag.keys()):
        bag[item_id] += quantity
        messages.success(request, f'Updated {product.name} quantity to {bag[item_id]}')
    else:
        bag[item_id] = quantity
        messages.success(request, f'Added {product.name} to your bag')
    
    request.session['bag'] = bag
    # print(request.session['bag']) # For debugging, you can uncomment this
    return redirect(redirect_url) # Redirect to the URL provided in the form


def adjust_bag(request, item_id):
    """Adjust the quantity of the specified product to the specified amount"""

    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    bag = request.session.get('bag', {})

    if quantity > 0:
        bag[item_id] = quantity
        messages.success(request, f'Updated {product.name} quantity to {bag[item_id]}')
    else:
        bag.pop(item_id)
        messages.info(request, f'Removed {product.name} from your bag')

    request.session['bag'] = bag
    return redirect(reverse('bag:view_bag'))


def remove_from_bag(request, item_id):
    """Remove the item from the shopping bag"""
    print(f"Attempting to remove item_id: {item_id}") # Debug print
    try:
        product = get_object_or_404(Product, pk=item_id)
        bag = request.session.get('bag', {})
        
        print(f"Bag before removal: {bag}") # Debug print
        
        if str(item_id) in bag: # Ensure key type matches (session stores keys as strings)
            bag.pop(str(item_id))
            messages.info(request, f'Removed {product.name} from your bag')
            print(f"Successfully removed {item_id}. Bag after removal: {bag}") # Debug print
        else:
            messages.error(request, f'Error removing item: {product.name} not found in bag.')
            print(f"Error: {item_id} not found in bag.") # Debug print
            return HttpResponse(status=404) # Return 404 if item not found in bag

        request.session['bag'] = bag
        return HttpResponse(status=200)

    except Exception as e:
        messages.error(request, f'Error removing item: {e}')
        print(f"Exception during removal: {e}") # Debug print
        return HttpResponse(status=500)
