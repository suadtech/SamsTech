import json
import sys

def analyze_json_and_generate_fields(json_file_path):
    """
    Analyze JSON fixture file and generate Django model field definitions
    """
    try:
        with open(json_file_path, 'r') as f:
            data = json.load(f)
        
        # Collect all fields and their sample values
        field_info = {}
        
        for item in data:
            if 'fields' in item:
                for field_name, field_value in item['fields'].items():
                    if field_name not in field_info:
                        field_info[field_name] = {
                            'values': [],
                            'types': set()
                        }
                    
                    field_info[field_name]['values'].append(field_value)
                    field_info[field_name]['types'].add(type(field_value).__name__)
        
        # Known existing fields in the model (based on previous conversations)
        existing_fields = {
            'sku', 'name', 'description', 'price', 'category', 'rating', 
            'image_url', 'image', 'brand', 'shipping', 'estimated_delivery', 
            'vat_status', 'stock_status', 'warranty', 'compatibility', 
            'includes', 'condition', 'availability', 'features', 
            'display_type', 'release_year', 'device_tier', 'extra_data',
            'color', 'size', 'weight', 'dimensions', 'material', 
            'model_number', 'is_active', 'is_featured', 'stock_quantity',
            'created_at', 'updated_at', 'excludes', 'specifications', 
            'tags', 'category_path', 'tool_requirements'
        }
        
        # Generate field definitions for missing fields
        missing_fields = []
        
        for field_name, info in field_info.items():
            if field_name not in existing_fields:
                # Determine field type based on sample values
                field_type = determine_field_type(info['values'], info['types'])
                missing_fields.append((field_name, field_type))
        
        # Sort fields alphabetically
        missing_fields.sort()
        
        print("=== MISSING DJANGO MODEL FIELDS ===")
        print(f"Found {len(missing_fields)} missing fields:")
        print()
        
        for field_name, field_type in missing_fields:
            print(f"    {field_name} = {field_type}")
        
        print()
        print("=== COPY THE ABOVE FIELDS TO YOUR PRODUCT MODEL ===")
        print("Add these lines to your products/models.py Product class")
        
        return missing_fields
        
    except Exception as e:
        print(f"Error analyzing file: {e}")
        return []

def determine_field_type(values, types):
    """
    Determine appropriate Django field type based on sample values
    """
    # Remove None values for analysis
    non_none_values = [v for v in values if v is not None]
    
    if not non_none_values:
        return "models.CharField(max_length=254, null=True, blank=True)"
    
    # Check if all values are strings
    if all(isinstance(v, str) for v in non_none_values):
        max_length = max(len(str(v)) for v in non_none_values)
        
        # If very long text, use TextField
        if max_length > 500:
            return "models.TextField(null=True, blank=True)"
        else:
            # Use CharField with appropriate max_length
            suggested_length = min(max(max_length + 50, 100), 500)
            return f"models.CharField(max_length={suggested_length}, null=True, blank=True)"
    
    # Check if all values are numbers
    elif all(isinstance(v, (int, float)) for v in non_none_values):
        if all(isinstance(v, int) for v in non_none_values):
            return "models.IntegerField(null=True, blank=True)"
        else:
            return "models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)"
    
    # Check if all values are booleans
    elif all(isinstance(v, bool) for v in non_none_values):
        return "models.BooleanField(default=False)"
    
    # Mixed types or complex data - use CharField as fallback
    else:
        return "models.CharField(max_length=254, null=True, blank=True)"

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python generate_model_fields.py <json_file_path>")
        sys.exit(1)
    
    json_file = sys.argv[1]
    generate_model_fields = analyze_json_and_generate_fields(json_file)
