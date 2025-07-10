import json
from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Product

def get_product_price(product):
    """
    Safely gets the price of a product, handling complex price strings.
    """
    try:
        price_value = product.price
        if isinstance(price_value, str) and price_value.startswith('{') and price_value.endswith('}'):
            price_dict = json.loads(price_value.replace("'", "\""))
            return float(price_dict.get('single', price_dict.get('unit_price', 0.0)))
        else:
            return float(price_value)
    except (ValueError, TypeError, json.JSONDecodeError):
        return 0.0

def bag_contents(request):
    bag_items = []
    total = 0
    product_count = 0
    bag = request.session.get('bag', {})

    for item_id, item_data in bag.items():
        product = get_object_or_404(Product, pk=item_id)
        product_price_for_calc = get_product_price(product)

        if isinstance(item_data, int):
            total += item_data * product_price_for_calc
            product_count += item_data
            bag_items.append({
                'item_id': item_id,
                'quantity': item_data,
                'product': product,
            })
        else:
            for size, quantity in item_data['items_by_size'].items():
                total += quantity * product_price_for_calc
                product_count += quantity
                bag_items.append({
                    'item_id': item_id,
                    'quantity': quantity,
                    'product': product,
                    'size': size,
                })

    # Convert total to Decimal for calculations
    total_decimal = Decimal(str(total))
    
    if total_decimal < settings.FREE_DELIVERY_THRESHOLD:
        delivery = total_decimal * Decimal(settings.STANDARD_DELIVERY_PERCENTAGE / 100)
        free_delivery_delta = settings.FREE_DELIVERY_THRESHOLD - total_decimal
    else:
        delivery = 0
        free_delivery_delta = 0
    
    grand_total = delivery + total_decimal

    context = {
        'bag_items': bag_items,
        'total': total_decimal,
        'product_count': product_count,
        'delivery': delivery,
        'free_delivery_delta': free_delivery_delta,
        'free_delivery_threshold': settings.FREE_DELIVERY_THRESHOLD,
        'grand_total': grand_total,
    }

    return context
