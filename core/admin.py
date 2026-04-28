from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product, Order, OrderItem, Cart, CartItem
import json

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'product_count')
    prepopulated_fields = {'slug': ('name',)}
    
    def product_count(self, obj):
        return obj.products.count()
    product_count.short_description = "Products"

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('display_image', 'name', 'category', 'price', 'stock', 'badge', 'is_trending', 'is_featured')
    list_filter = ('category', 'badge', 'is_trending', 'is_featured', 'created_at')
    list_editable = ('price', 'stock', 'badge', 'is_trending', 'is_featured')
    search_fields = ('name', 'desc')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Suit Details', {
            'fields': ('name', 'category', 'desc', ('badge', 'is_trending', 'is_featured')),
            'classes': ('wide',),
        }),
        ('Pricing & Stock', {
            'fields': (('price', 'old_price'), ('stock', 'sold'), 'sizes'),
        }),
        ('Suit Photography', {
            'fields': (('img', 'img2'), ('img3', 'img4'), 'img5'),
            'description': 'Upload up to 5 photos showing different views of the suit (Front, Back, Details, etc).',
        }),
    )

    def display_image(self, obj):
        if obj.img:
            # Handle both URLs and uploaded files
            url = obj.img.url if hasattr(obj.img, 'url') else str(obj.img)
            return format_html('<img src="{}" style="width: 45px; height: 55px; object-fit: cover; border-radius: 4px; border: 1px solid #ddd;" />', url)
        return "No Image"
    display_image.short_description = 'Preview'

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product_name_snapshot', 'price_snapshot', 'quantity', 'size', 'color')
    can_delete = False

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'get_full_name', 'phone_number', 'status', 'total_price', 'status_badge', 'created_at')
    list_filter = ('status', 'payment_method', 'created_at')
    list_editable = ('status',)
    search_fields = ('order_id', 'customer_name', 'phone_number', 'first_name', 'last_name', 'email')
    readonly_fields = ('order_id', 'created_at', 'updated_at', 'total_price')
    inlines = [OrderItemInline]

    fieldsets = (
        ('Customer Info', {
            'fields': (('first_name', 'last_name'), 'email', 'phone_number', 'full_address')
        }),
        ('Order Details', {
            'fields': (('order_id', 'total_price'), ('status', 'payment_method'))
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
        }),
    )

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    get_full_name.short_description = 'Customer Name'

    def status_badge(self, obj):
        colors = {
            'Pending': '#f39c12',
            'Confirmed': '#27ae60',
            'Packed': '#8e44ad',
            'Shipped': '#2980b9',
            'Delivered': '#2c3e50',
            'Cancelled': '#c0392b',
        }
        color = colors.get(obj.status.split(' ')[0], '#000')  # splitting to handle emojis safely if they exist
        return format_html(
            '<span style="background: {}; color: #fff; padding: 4px 10px; border-radius: 20px; font-weight: bold; font-size: 11px;">{}</span>',
            color, obj.get_status_display()
        )
    status_badge.short_description = "Status"

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ('product', 'quantity', 'size', 'color')

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'session_key', 'created_at', 'updated_at')
    inlines = [CartItemInline]
