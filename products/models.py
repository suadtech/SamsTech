from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse
import json
class Category(models.Model):
    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']
    
    name = models.CharField(max_length=254, null=True, blank=True)
   
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.friendly_name or self.name

class Product(models.Model):
    class Meta:
        ordering = ['id']  
        
    # Basic fields

    name = models.CharField(max_length=254, null=True, blank=True)
    sku = models.CharField(max_length=254, null=True, blank=True)
    category = models.CharField(max_length=254, null=True, blank=True)

   

    description = models.TextField()
    price = models.CharField(max_length=254, null=True, blank=True)

    rating = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True, upload_to='products/')
    
    # Product details fields
    brand = models.CharField(max_length=254, null=True, blank=True)
    shipping = models.CharField(max_length=254, null=True, blank=True)
    estimated_delivery = models.CharField(max_length=254, null=True, blank=True)
    vat_status = models.CharField(max_length=254, null=True, blank=True)
    stock_status = models.CharField(max_length=254, null=True, blank=True)
    warranty = models.CharField(max_length=254, null=True, blank=True)
    compatibility = models.CharField(max_length=254, null=True, blank=True)
    includes = models.CharField(max_length=254, null=True, blank=True)
    condition = models.CharField(max_length=254, null=True, blank=True)
    availability = models.CharField(max_length=254, null=True, blank=True)
    features = models.TextField(null=True, blank=True)
    display_type = models.CharField(max_length=254, null=True, blank=True)
    release_year = models.CharField(max_length=254, null=True, blank=True)
    device_tier = models.CharField(max_length=254, null=True, blank=True)
    color = models.CharField(max_length=254, null=True, blank=True)
    size = models.CharField(max_length=254, null=True, blank=True)


    weight = models.CharField(max_length=254, null=True, blank=True)
    dimensions = models.CharField(max_length=254, null=True, blank=True)
    material = models.CharField(max_length=254, null=True, blank=True)
    model_number = models.CharField(max_length=254, null=True, blank=True)
    
    # Additional fields for JSON compatibility
    excludes = models.CharField(max_length=254, null=True, blank=True)
    specifications = models.TextField(null=True, blank=True)
    tags = models.CharField(max_length=254, null=True, blank=True)

    category_path = models.CharField(max_length=254, null=True, blank=True)
    repair_difficulty = models.CharField(max_length=254, null=True, blank=True)
    tool_requirements = models.CharField(max_length=254, null=True, blank=True)
    install_notes = models.TextField(null=True, blank=True)
    difficulty = models.CharField(max_length=254, null=True, blank=True)
    installation = models.CharField(max_length=254, null=True, blank=True)
    installation_time = models.CharField(max_length=254, null=True, blank=True)
    color_accuracy = models.CharField(max_length=254, null=True,blank=True)
 
    special_features = models.CharField(max_length=254, null=True, blank=True)
    color_options = models.CharField(max_length=254, null=True, blank=True)
    display_features = models.CharField(max_length=254, null=True, blank=True)
    technical_specs = models.CharField(max_length=254, null=True, blank=True)
    installation_notes = models.TextField(null=True, blank=True)
    durability_features = models.CharField(max_length=254, null=True, blank=True)
    performance_specs = models.CharField(max_length=254, null=True, blank=True)
    connectivity_options = models.CharField(max_length=254, null=True, blank=True)
    power_requirements = models.CharField(max_length=254, null=True, blank=True)
    environmental_specs = models.CharField(max_length=254, null=True, blank=True)
    safety_features = models.CharField(max_length=254, null=True, blank=True)
    quality_rating = models.CharField(max_length=254, null=True, blank=True)
    user_manual = models.CharField(max_length=254, null=True, blank=True)
    support_info = models.CharField(max_length=254, null=True, blank=True)
    replacement_parts = models.CharField(max_length=254, null=True, blank=True)
    maintenance_guide = models.TextField(null=True, blank=True)
    troubleshooting = models.TextField(null=True, blank=True)
    market = models.CharField(max_length=254, null=True, blank=True)
    target_audience = models.CharField(max_length=254, null=True, blank=True)
    usage_instructions = models.TextField(null=True, blank=True)
    storage_requirements = models.CharField(max_length=254, null=True, blank=True)
    shipping_info = models.CharField(max_length=254, null=True, blank=True)
    return_policy = models.CharField(max_length=254, null=True, blank=True)
    certification = models.CharField(max_length=254, null=True, blank=True)
    compliance = models.CharField(max_length=254, null=True, blank=True)
    testing_standards = models.CharField(max_length=254, null=True, blank=True)
    quality_assurance = models.CharField(max_length=254, null=True, blank=True)
    resolution = models.CharField(max_length=254, null=True, blank=True)
    screen_size = models.CharField(max_length=254, null=True, blank=True)
    refresh_rate = models.CharField(max_length=254, null=True, blank=True)
    pixel_density = models.CharField(max_length=254, null=True, blank=True)
    aspect_ratio = models.CharField(max_length=254, null=True, blank=True)
    brightness_level = models.CharField(max_length=254, null=True, blank=True)
    contrast_ratio = models.CharField(max_length=254, null=True, blank=True)
    viewing_angle = models.CharField(max_length=254, null=True, blank=True)
    response_time = models.CharField(max_length=254, null=True, blank=True)
    color_gamut = models.CharField(max_length=254, null=True, blank=True)
    hdr_support = models.CharField(max_length=254, null=True, blank=True)
    touch_sensitivity = models.CharField(max_length=254, null=True, blank=True)
    glass_type = models.CharField(max_length=254, null=True, blank=True)
    oleophobic_coating = models.CharField(max_length=254, null=True, blank=True)
    anti_fingerprint = models.CharField(max_length=254, null=True, blank=True)
    part_type = models.CharField(max_length=254, null=True, blank=True)
    component_category = models.CharField(max_length=254, null=True, blank=True)
    device_model = models.CharField(max_length=254, null=True, blank=True)
    part_number = models.CharField(max_length=254, null=True, blank=True)
    manufacturer_code = models.CharField(max_length=254, null=True, blank=True)
    oem_part = models.CharField(max_length=254, null=True, blank=True)
    aftermarket_part = models.CharField(max_length=254, null=True, blank=True)
    replacement_for = models.CharField(max_length=254, null=True, blank=True)
    compatible_models = models.TextField(null=True, blank=True)
    installation_level = models.CharField(max_length=254, null=True, blank=True)
    tools_needed = models.CharField(max_length=254, null=True, blank=True)
    connector_type = models.CharField(max_length=254, null=True, blank=True)
    cable_length = models.CharField(max_length=254, null=True, blank=True)
    port_type = models.CharField(max_length=254, null=True, blank=True)
    charging_speed = models.CharField(max_length=254, null=True, blank=True)
    data_transfer_rate = models.CharField(max_length=254, null=True, blank=True)
    voltage_rating = models.CharField(max_length=254, null=True, blank=True)
    current_rating = models.CharField(max_length=254, null=True, blank=True)
    power_output = models.CharField(max_length=254, null=True, blank=True)
    efficiency_rating = models.CharField(max_length=254, null=True, blank=True)
    protection_features = models.CharField(max_length=254, null=True, blank=True)
    build_quality = models.CharField(max_length=254, null=True, blank=True)
    durability_rating = models.CharField(max_length=254, null=True, blank=True)
    functions = models.CharField(max_length=254, null=True, blank=True)
    oem_equivalent = models.CharField(max_length=254, null=True, blank=True)


    popularity_rank = models.CharField(max_length=254, null=True, blank=True)
    sales_rank = models.CharField(max_length=254, null=True, blank=True)
    trending_score = models.CharField(max_length=254, null=True, blank=True)
    launch_date = models.CharField(max_length=254, null=True, blank=True)
    discontinuation_date = models.CharField(max_length=254, null=True, blank=True)
    lifecycle_stage = models.CharField(max_length=254, null=True, blank=True)
    stock_status = models.CharField(max_length=254, null=True, blank=True)
    availability = models.CharField(max_length=254, null=True, blank=True)
    lead_time = models.CharField(max_length=254, null=True, blank=True)
    cost_price = models.CharField(max_length=254, null=True, blank=True)
    msrp = models.CharField(max_length=254, null=True, blank=True)
    discount_percentage = models.CharField(max_length=254, null=True, blank=True)
    quality_score = models.CharField(max_length=254, null=True, blank=True)
    test_results = models.TextField(null=True, blank=True)
    certification_status = models.CharField(max_length=254, null=True, blank=True)
    customer_reviews = models.TextField(null=True, blank=True)
    review_count = models.CharField(max_length=254, null=True, blank=True)
    market_segment = models.CharField(max_length=254, null=True, blank=True)
    dimensions = models.CharField(max_length=254, null=True, blank=True)
    weight = models.CharField(max_length=254, null=True, blank=True)
    material = models.CharField(max_length=254, null=True, blank=True)
    system_requirements = models.TextField(null=True, blank=True)
    compatibility_notes = models.TextField(null=True, blank=True)
    prerequisites = models.CharField(max_length=254, null=True, blank=True)
    documentation_url = models.CharField(max_length=254, null=True, blank=True)
    video_guide = models.CharField(max_length=254, null=True, blank=True)
    faq_link = models.CharField(max_length=254, null=True, blank=True)
    vendor_info = models.CharField(max_length=254, null=True, blank=True)
    supplier_code = models.CharField(max_length=254, null=True, blank=True)
    purchase_terms = models.CharField(max_length=254, null=True, blank=True)
    keywords = models.CharField(max_length=254, null=True, blank=True)
    metadata = models.TextField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    featured = models.CharField(max_length=254, null=True, blank=True)
    promoted = models.CharField(max_length=254, null=True, blank=True)
    optical_properties = models.CharField(max_length=254, null=True, blank=True)
    display_technology = models.CharField(max_length=254, null=True, blank=True)
    screen_protection = models.CharField(max_length=254, null=True, blank=True)
    touch_technology = models.CharField(max_length=254, null=True, blank=True)
    sensor_type = models.CharField(max_length=254, null=True, blank=True)
    camera_specs = models.CharField(max_length=254, null=True, blank=True)
    lens_quality = models.CharField(max_length=254, null=True, blank=True)
    image_stabilization = models.CharField(max_length=254, null=True, blank=True)
    autofocus_type = models.CharField(max_length=254, null=True, blank=True)
    flash_type = models.CharField(max_length=254, null=True, blank=True)
    video_recording = models.CharField(max_length=254, null=True, blank=True)
    audio_quality = models.CharField(max_length=254, null=True, blank=True)
    microphone_specs = models.CharField(max_length=254, null=True, blank=True)
    speaker_specs = models.CharField(max_length=254, null=True, blank=True)
    battery_specs = models.CharField(max_length=254, null=True, blank=True)
    charging_technology = models.CharField(max_length=254, null=True, blank=True)
    wireless_features = models.CharField(max_length=254, null=True, blank=True)
    bluetooth_version = models.CharField(max_length=254, null=True, blank=True)
    wifi_standards = models.CharField(max_length=254, null=True, blank=True)
    cellular_bands = models.CharField(max_length=254, null=True, blank=True)
    gps_accuracy = models.CharField(max_length=254, null=True, blank=True)
    nfc_support = models.CharField(max_length=254, null=True, blank=True)
    biometric_features = models.CharField(max_length=254, null=True, blank=True)
    security_features = models.CharField(max_length=254, null=True, blank=True)
    encryption_support = models.CharField(max_length=254, null=True, blank=True)
    package_contents = models.TextField(null=True, blank=True)
    package_dimensions = models.CharField(max_length=254, null=True, blank=True)
    package_weight = models.CharField(max_length=254, null=True, blank=True)
    package_type = models.CharField(max_length=254, null=True, blank=True)
    unboxing_experience = models.CharField(max_length=254, null=True, blank=True)
    warranty_period = models.CharField(max_length=254, null=True, blank=True)
    warranty_terms = models.TextField(null=True, blank=True)
    warranty_coverage = models.CharField(max_length=254, null=True, blank=True)
    support_contact = models.CharField(max_length=254, null=True, blank=True)
    support_hours = models.CharField(max_length=254, null=True, blank=True)
    environmental_rating = models.CharField(max_length=254, null=True, blank=True)
    recycling_info = models.CharField(max_length=254, null=True, blank=True)
    regulatory_compliance = models.CharField(max_length=254, null=True, blank=True)
    safety_warnings = models.TextField(null=True, blank=True)
    age_restrictions = models.CharField(max_length=254, null=True, blank=True)
    performance_metrics = models.TextField(null=True, blank=True)
    benchmark_scores = models.CharField(max_length=254, null=True, blank=True)
    stress_test_results = models.CharField(max_length=254, null=True, blank=True)
    reliability_rating = models.CharField(max_length=254, null=True, blank=True)
    mtbf_rating = models.CharField(max_length=254, null=True, blank=True)
    competitor_comparison = models.TextField(null=True, blank=True)
    market_position = models.CharField(max_length=254, null=True, blank=True)
    target_market = models.CharField(max_length=254, null=True, blank=True)
    sales_channel = models.CharField(max_length=254, null=True, blank=True)
    distribution_method = models.CharField(max_length=254, null=True, blank=True)
    operating_temperature = models.CharField(max_length=254, null=True, blank=True)
    storage_temperature = models.CharField(max_length=254, null=True, blank=True)
    humidity_tolerance = models.CharField(max_length=254, null=True, blank=True)
    shock_resistance = models.CharField(max_length=254, null=True, blank=True)
    vibration_resistance = models.CharField(max_length=254, null=True, blank=True)
    accessories_included = models.CharField(max_length=254, null=True, blank=True)
    advanced_tech = models.CharField(max_length=254, null=True, blank=True)
    apple_specific = models.CharField(max_length=254, null=True, blank=True)
    audio_features = models.CharField(max_length=254, null=True, blank=True)
    battery = models.CharField(max_length=254, null=True, blank=True)
    biometric_note = models.CharField(max_length=254, null=True, blank=True)
    brightness = models.CharField(max_length=254, null=True, blank=True)
    certifications = models.CharField(max_length=254, null=True, blank=True)
    color_temp = models.CharField(max_length=254, null=True, blank=True)
    comfort_features = models.CharField(max_length=254, null=True, blank=True)
    compatibility = models.CharField(max_length=254, null=True, blank=True)
    connector_specs = models.CharField(max_length=254, null=True, blank=True)
    connectors = models.CharField(max_length=254, null=True, blank=True)
    construction = models.CharField(max_length=254, null=True, blank=True)
    curved_display_specs = models.CharField(max_length=254, null=True, blank=True)
    device_tier = models.CharField(max_length=254, null=True, blank=True)
    display_optimization = models.CharField(max_length=254, null=True, blank=True)
    display_type = models.CharField(max_length=254, null=True, blank=True)
    durability = models.CharField(max_length=254, null=True, blank=True)
    environmental = models.CharField(max_length=254, null=True, blank=True)
    features = models.CharField(max_length=254, null=True, blank=True)
    galaxy_optimization = models.CharField(max_length=254, null=True, blank=True)
    gaming_features = models.CharField(max_length=254, null=True, blank=True)
    gaming_optimized = models.CharField(max_length=254, null=True, blank=True)
    haptic_support = models.CharField(max_length=254, null=True, blank=True)
    included_accessories = models.CharField(max_length=254, null=True, blank=True)
    includes = models.CharField(max_length=254, null=True, blank=True)
    installation = models.CharField(max_length=254, null=True, blank=True)
    installation_time = models.CharField(max_length=254, null=True, blank=True)
    key_applications = models.CharField(max_length=254, null=True, blank=True)
    key_features = models.CharField(max_length=254, null=True, blank=True)
    material_composition = models.CharField(max_length=254, null=True, blank=True)
    material_tech = models.CharField(max_length=254, null=True, blank=True)
    oneplus_specific = models.CharField(max_length=254, null=True, blank=True)
    package_details = models.CharField(max_length=254, null=True, blank=True)
    package_includes = models.CharField(max_length=254, null=True, blank=True)
    performance = models.CharField(max_length=254, null=True, blank=True)
    performance_features = models.CharField(max_length=254, null=True, blank=True)
    platform_compatibility = models.CharField(max_length=254, null=True, blank=True)
    promotions = models.CharField(max_length=254, null=True, blank=True)
    protection = models.CharField(max_length=254, null=True, blank=True)
    protection_levels = models.CharField(max_length=254, null=True, blank=True)
    protection_rating = models.CharField(max_length=254, null=True, blank=True)
    protection_specs = models.CharField(max_length=254, null=True, blank=True)
    quality_marks = models.CharField(max_length=254, null=True, blank=True)
    release_year = models.CharField(max_length=254, null=True, blank=True)
    release_years = models.CharField(max_length=254, null=True, blank=True)
    safety_certifications = models.CharField(max_length=254, null=True, blank=True)
    seller_info = models.CharField(max_length=254, null=True, blank=True)
    seller_note = models.CharField(max_length=254, null=True, blank=True)
    smart_features = models.CharField(max_length=254, null=True, blank=True)
    special_editions = models.CharField(max_length=254, null=True, blank=True)
    stand_angles = models.CharField(max_length=254, null=True, blank=True)
    stand_functionality = models.CharField(max_length=254, null=True, blank=True)
    stock = models.CharField(max_length=254, null=True, blank=True)
    technology = models.CharField(max_length=254, null=True, blank=True)
    thickness = models.CharField(max_length=254, null=True, blank=True)
    universal_compatibility = models.CharField(max_length=254, null=True, blank=True)
    use_cases = models.CharField(max_length=254, null=True, blank=True)
    water_resistance = models.CharField(max_length=254, null=True, blank=True)

    # Ranking and popularity fields
    popularity_rank = models.CharField(max_length=254, null=True, blank=True)
    sales_rank = models.CharField(max_length=254, null=True, blank=True)
    trending_score = models.CharField(max_length=254, null=True, blank=True)
    
    # Product lifecycle fields
    launch_date = models.CharField(max_length=254, null=True, blank=True)
    discontinuation_date = models.CharField(max_length=254, null=True, blank=True)
    lifecycle_stage = models.CharField(max_length=254, null=True, blank=True)
    
    # Inventory and availability
    stock_status = models.CharField(max_length=254, null=True, blank=True)
    availability = models.CharField(max_length=254, null=True, blank=True)
    lead_time = models.CharField(max_length=254, null=True, blank=True)


    repair_type = models.CharField(max_length=254, null=True, blank=True)
   
    # JSON field for additional flexible data
    difficulty = models.CharField(max_length=254, null=True, blank=True)


    extra_data = models.JSONField(default=dict, blank=True, null=True)
    
    # System fields
  
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    stock_quantity = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.name
