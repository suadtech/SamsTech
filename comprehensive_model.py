from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse
import json

class Category(models.Model):
    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['id']
    
    name = models.CharField(max_length=254, unique=True)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.friendly_name or self.name

class Product(models.Model):
    class Meta:
        ordering = ['name']  
        
    # Basic fields
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL, related_name='products')
    sku = models.CharField(max_length=254, unique=True)
    name = models.CharField(max_length=254)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
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
    
    # Fields we've already added
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
    time_required = models.CharField(max_length=254, null=True, blank=True)
    
    # Additional fields from JSON analysis - ADD THESE TO RESOLVE REMAINING ERRORS
    abrasion_resistance = models.CharField(max_length=254, null=True, blank=True)
    accessories_included = models.CharField(max_length=254, null=True, blank=True)
    adhesive_type = models.CharField(max_length=254, null=True, blank=True)
    advanced_tech = models.CharField(max_length=254, null=True, blank=True)
    alert_slider_cutout = models.CharField(max_length=254, null=True, blank=True)
    anti_glare = models.CharField(max_length=254, null=True, blank=True)
    apple_specific = models.CharField(max_length=254, null=True, blank=True)
    audio_features = models.CharField(max_length=254, null=True, blank=True)
    audio_quality = models.CharField(max_length=254, null=True, blank=True)
    automotive = models.CharField(max_length=254, null=True, blank=True)
    available = models.CharField(max_length=254, null=True, blank=True)
    awg = models.CharField(max_length=254, null=True, blank=True)
    bandwidth = models.CharField(max_length=254, null=True, blank=True)
    base_layer = models.CharField(max_length=254, null=True, blank=True)
    battery = models.CharField(max_length=254, null=True, blank=True)
    battery_protection = models.CharField(max_length=254, null=True, blank=True)
    bend_cycles = models.CharField(max_length=254, null=True, blank=True)
    bend_life = models.CharField(max_length=254, null=True, blank=True)
    bend_radius = models.CharField(max_length=254, null=True, blank=True)
    best_offer = models.CharField(max_length=254, null=True, blank=True)
    biometric_note = models.CharField(max_length=254, null=True, blank=True)
    bit_depth = models.CharField(max_length=254, null=True, blank=True)
    blue_light_filter = models.CharField(max_length=254, null=True, blank=True)
    bpa_free = models.CharField(max_length=254, null=True, blank=True)
    brightness = models.CharField(max_length=254, null=True, blank=True)
    bubble_free_adhesive = models.CharField(max_length=254, null=True, blank=True)
    bulk_discount = models.CharField(max_length=254, null=True, blank=True)
    bulk_discounts = models.CharField(max_length=254, null=True, blank=True)
    bundle = models.CharField(max_length=254, null=True, blank=True)
    cable = models.CharField(max_length=254, null=True, blank=True)
    cable_length = models.CharField(max_length=254, null=True, blank=True)
    cables = models.CharField(max_length=254, null=True, blank=True)
    cameras = models.CharField(max_length=254, null=True, blank=True)
    capacity = models.CharField(max_length=254, null=True, blank=True)
    case_charges = models.CharField(max_length=254, null=True, blank=True)
    certifications = models.CharField(max_length=254, null=True, blank=True)
    channels = models.CharField(max_length=254, null=True, blank=True)
    chargers = models.CharField(max_length=254, null=True, blank=True)
    charging = models.CharField(max_length=254, null=True, blank=True)
    charging_speed = models.CharField(max_length=254, null=True, blank=True)
    chemistry = models.CharField(max_length=254, null=True, blank=True)
    clarity = models.CharField(max_length=254, null=True, blank=True)
    coating = models.CharField(max_length=254, null=True, blank=True)
    color_accuracy = models.CharField(max_length=254, null=True, blank=True)
    color_depth = models.CharField(max_length=254, null=True, blank=True)
    color_options = models.CharField(max_length=254, null=True, blank=True)
    color_temp = models.CharField(max_length=254, null=True, blank=True)
    comfort_features = models.CharField(max_length=254, null=True, blank=True)
    commercial = models.CharField(max_length=254, null=True, blank=True)
    commercial_discount = models.CharField(max_length=254, null=True, blank=True)
    compatible_models = models.CharField(max_length=254, null=True, blank=True)
    conductors = models.CharField(max_length=254, null=True, blank=True)
    connectivity = models.CharField(max_length=254, null=True, blank=True)
    connector = models.CharField(max_length=254, null=True, blank=True)
    connectors = models.CharField(max_length=254, null=True, blank=True)
    connector_specs = models.CharField(max_length=254, null=True, blank=True)
    connector_type = models.CharField(max_length=254, null=True, blank=True)
    consoles = models.CharField(max_length=254, null=True, blank=True)
    construction = models.CharField(max_length=254, null=True, blank=True)
    content_creator_bundle = models.CharField(max_length=254, null=True, blank=True)
    control = models.CharField(max_length=254, null=True, blank=True)
    curing_process = models.CharField(max_length=254, null=True, blank=True)
    curing_time = models.CharField(max_length=254, null=True, blank=True)
    currency_options = models.CharField(max_length=254, null=True, blank=True)
    current = models.CharField(max_length=254, null=True, blank=True)
    curved_display_specs = models.CharField(max_length=254, null=True, blank=True)
    daisy_chaining = models.CharField(max_length=254, null=True, blank=True)
    data_speed = models.CharField(max_length=254, null=True, blank=True)
    data_transfer = models.CharField(max_length=254, null=True, blank=True)
    devices = models.CharField(max_length=254, null=True, blank=True)
    diameter = models.CharField(max_length=254, null=True, blank=True)
    discount = models.CharField(max_length=254, null=True, blank=True)
    discount_threshold = models.CharField(max_length=254, null=True, blank=True)
    discount_tiers = models.CharField(max_length=254, null=True, blank=True)
    display = models.CharField(max_length=254, null=True, blank=True)
    display_features = models.CharField(max_length=254, null=True, blank=True)
    display_optimization = models.CharField(max_length=254, null=True, blank=True)
    drivers = models.CharField(max_length=254, null=True, blank=True)
    drop_protection = models.CharField(max_length=254, null=True, blank=True)
    drop_test = models.CharField(max_length=254, null=True, blank=True)
    durability = models.CharField(max_length=254, null=True, blank=True)
    durability_features = models.CharField(max_length=254, null=True, blank=True)
    edge_coverage = models.CharField(max_length=254, null=True, blank=True)
    efficiency = models.CharField(max_length=254, null=True, blank=True)
    emc_shielding = models.CharField(max_length=254, null=True, blank=True)
    energy_efficiency = models.CharField(max_length=254, null=True, blank=True)
    energy_star = models.CharField(max_length=254, null=True, blank=True)
    environmental = models.CharField(max_length=254, null=True, blank=True)
    equivalents = models.CharField(max_length=254, null=True, blank=True)
    exclusions = models.CharField(max_length=254, null=True, blank=True)
    frequency = models.CharField(max_length=254, null=True, blank=True)
    frequency_response = models.CharField(max_length=254, null=True, blank=True)
    functions = models.CharField(max_length=254, null=True, blank=True)
    
    # JSON field for additional flexible data
    extra_data = models.JSONField(default=dict, blank=True, null=True)
    
    # System fields
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    stock_quantity = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.name




