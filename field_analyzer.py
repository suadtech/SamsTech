#!/usr/bin/env python3
"""
Django Model Field Analyzer
Automatically detects missing fields from JSON fixture and generates Django model field definitions
"""

import json
from collections import defaultdict

def analyze_json_fields(json_file_path):
    """Extract all unique field names from the JSON fixture file"""
    print(f"🔍 Analyzing JSON file: {json_file_path}")
    
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"❌ Error: File {json_file_path} not found!")
        return set(), {}
    except json.JSONDecodeError as e:
        print(f"❌ Error: Invalid JSON format - {e}")
        return set(), {}
    
    all_fields = set()
    field_types = defaultdict(set)
    
    # Extract fields from each product record
    for item in data:
        if isinstance(item, dict) and 'fields' in item:
            fields = item['fields']
            for field_name, field_value in fields.items():
                all_fields.add(field_name)
                # Analyze field value types for better field type suggestions
                if isinstance(field_value, str):
                    if len(field_value) > 254:
                        field_types[field_name].add('TextField')
                    else:
                        field_types[field_name].add('CharField')
                elif isinstance(field_value, (int, float)):
                    field_types[field_name].add('CharField')  # Store as CharField for flexibility
                elif field_value is None:
                    field_types[field_name].add('CharField')  # Default to CharField
                else:
                    field_types[field_name].add('CharField')  # Default fallback
    
    print(f"✅ Found {len(all_fields)} unique fields in JSON data")
    return all_fields, field_types

def get_existing_model_fields():
    """Get list of fields that are already in the Django model"""
    # These are the fields we know have been successfully added based on our conversation
    existing_fields = {
        # Core Django fields
        'id', 'pk',
        
        # Original model fields
        'sku', 'name', 'description', 'price', 'category', 'rating', 
        'image_url', 'image', 'brand', 'shipping', 'warranty',
        'estimated_delivery', 'vat_status', 'model_number',
        
        # Fields we've successfully added in batches (151+ fields)
        'excludes', 'specifications', 'tags', 'category_path', 'repair_difficulty',
        'tool_requirements', 'install_notes', 'color_accuracy', 'special_features',
        'color_options', 'display_features', 'technical_specs', 'installation_notes',
        'durability_features', 'performance_specs', 'connectivity_options',
        'power_requirements', 'environmental_specs', 'safety_features',
        'quality_rating', 'user_manual', 'support_info', 'replacement_parts',
        'maintenance_guide', 'troubleshooting', 'functions', 'oem_equivalent',
        'popularity_rank', 'sales_rank', 'trending_score', 'launch_date',
        'discontinuation_date', 'lifecycle_stage', 'stock_status', 'availability',
        'lead_time', 'cost_price', 'msrp', 'discount_percentage', 'quality_score',
        'test_results', 'certification_status', 'customer_reviews', 'review_count',
        'market_segment', 'dimensions', 'weight', 'material', 'system_requirements',
        'compatibility_notes', 'prerequisites', 'documentation_url', 'video_guide',
        'faq_link', 'vendor_info', 'supplier_code', 'purchase_terms', 'keywords',
        'metadata', 'notes', 'featured', 'promoted', 'resolution', 'screen_size',
        'refresh_rate', 'pixel_density', 'aspect_ratio', 'brightness_level',
        'contrast_ratio', 'viewing_angle', 'response_time', 'color_gamut',
        'hdr_support', 'touch_sensitivity', 'glass_type', 'oleophobic_coating',
        'anti_fingerprint', 'part_type', 'component_category', 'device_model',
        'part_number', 'manufacturer_code', 'oem_part', 'aftermarket_part',
        'replacement_for', 'compatible_models', 'installation_level', 'tools_needed',
        'repair_type', 'connector_type', 'cable_length', 'port_type', 'charging_speed',
        'data_transfer_rate', 'voltage_rating', 'current_rating', 'power_output',
        'efficiency_rating', 'protection_features', 'build_quality', 'durability_rating',
        'market', 'target_audience', 'usage_instructions', 'storage_requirements',
        'shipping_info', 'return_policy', 'certification', 'compliance',
        'testing_standards', 'quality_assurance', 'optical_properties', 'audio_quality',
        'autofocus_type', 'battery_specs', 'biometric_features', 'bluetooth_version',
        'camera_specs', 'cellular_bands', 'charging_technology', 'display_technology',
        'encryption_support', 'flash_type', 'gps_accuracy', 'image_stabilization',
        'lens_quality', 'microphone_specs', 'nfc_support', 'screen_protection',
        'security_features', 'sensor_type', 'speaker_specs', 'touch_technology',
        'video_recording', 'wifi_standards', 'wireless_features', 'package_contents',
        'package_dimensions', 'package_weight', 'package_type', 'unboxing_experience',
        'warranty_period', 'warranty_terms', 'warranty_coverage', 'support_contact',
        'support_hours', 'environmental_rating', 'recycling_info', 'regulatory_compliance',
        'safety_warnings', 'age_restrictions', 'performance_metrics', 'benchmark_scores',
        'stress_test_results', 'reliability_rating', 'mtbf_rating', 'competitor_comparison',
        'market_position', 'target_market', 'sales_channel', 'distribution_method',
        'operating_temperature', 'storage_temperature', 'humidity_tolerance',
        'shock_resistance', 'vibration_resistance',
        
        # System fields
        'extra_data', 'difficulty'
    }
    
    print(f"📋 Known existing fields: {len(existing_fields)}")
    return existing_fields

def generate_missing_fields(all_fields, existing_fields, field_types):
    """Generate Django model field definitions for missing fields"""
    missing_fields = all_fields - existing_fields
    
    if not missing_fields:
        print("🎉 No missing fields found! All fields are already in the model.")
        return []
    
    print(f"🔍 Found {len(missing_fields)} missing fields:")
    
    field_definitions = []
    for field_name in sorted(missing_fields):
        # Determine the best field type based on analysis
        if field_name in field_types and 'TextField' in field_types[field_name]:
            field_def = f"    {field_name} = models.TextField(null=True, blank=True)"
        else:
            field_def = f"    {field_name} = models.CharField(max_length=254, null=True, blank=True)"
        
        field_definitions.append(field_def)
        print(f"  - {field_name}")
    
    return field_definitions

def main():
    """Main function to analyze JSON and generate missing field definitions"""
    print("🚀 Django Model Field Analyzer")
    print("=" * 50)
    
    # Use the local products.json file
    json_file_path = "./products/fixtures/products.json"
    
    # Analyze JSON file
    all_fields, field_types = analyze_json_fields(json_file_path)
    if not all_fields:
        return
    
    # Get existing model fields
    existing_fields = get_existing_model_fields()
    
    # Generate missing field definitions
    missing_field_definitions = generate_missing_fields(all_fields, existing_fields, field_types)
    
    if missing_field_definitions:
        print("\n" + "=" * 50)
        print("📝 DJANGO MODEL FIELD DEFINITIONS TO ADD:")
        print("=" * 50)
        print("\n# Add these fields to your Product model:")
        for field_def in missing_field_definitions:
            print(field_def)
        
        # Save to file
        output_file = "./missing_fields.py"
        with open(output_file, 'w') as f:
            f.write("# Missing Django Model Fields\n")
            f.write("# Add these fields to your Product model in products/models.py\n\n")
            for field_def in missing_field_definitions:
                f.write(field_def + "\n")
        
        print(f"\n💾 Field definitions saved to: {output_file}")
        print(f"\n🎯 Total missing fields: {len(missing_field_definitions)}")
        print("\n📋 NEXT STEPS:")
        print("1. Copy the field definitions above")
        print("2. Open: nano products/models.py")
        print("3. Add all fields to your Product model")
        print("4. Run: python manage.py makemigrations")
        print("5. Run: python manage.py migrate")
        print("6. Run: python manage.py loaddata products.json")
    
    print("\n✅ Analysis complete!")

if __name__ == "__main__":
    main()
