import json

# Define the fields that your Product model actually has.
# These are the only fields we want to keep.
import json

# These are the only fields that actually exist in your Product model.
VALID_FIELDS = {
    'sku',
    'name',
    'description',
    'price',
    'category',
    'rating',
    'image_url',
    'image',
    'brand',
    'shipping',
    'estimated_delivery',
    'vat_status',
}

# Load the original, broken JSON file
with open('products/fixtures/products.json', 'r') as f:
# ... the rest of the script is the same

    data = json.load(f)

cleaned_data = []
for product in data:
    # Get all the fields for the current product
    original_fields = product.get('fields', {})
    
    # Create a new dictionary with only the valid fields
    cleaned_fields = {key: value for key, value in original_fields.items() if key in VALID_FIELDS}
    
    # Make sure the price is a simple string, not a complex object
    if isinstance(cleaned_fields.get('price'), dict):
        # Try to find a single price value, default to "0.00" if none found
        price_obj = cleaned_fields['price']
        if 'single' in price_obj:
            cleaned_fields['price'] = str(price_obj['single'])
        elif 'range' in price_obj and 'min' in price_obj['range']:
             cleaned_fields['price'] = str(price_obj['range']['min'])
        else:
            cleaned_fields['price'] = "0.00"

    # Update the product with the cleaned fields
    product['fields'] = cleaned_fields
    cleaned_data.append(product)

# Save the cleaned data to a new file
with open('products/fixtures/products_cleaned.json', 'w') as f:
    json.dump(cleaned_data, f, indent=4)

print("Successfully cleaned the product data!")
print("A new file 'products_cleaned.json' has been created in products/fixtures/")

