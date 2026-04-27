from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product, Order
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

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_name', 'phone', 'items_summary', 'address', 'total_amount', 'status', 'status_badge')
    list_filter = ('status', 'payment_method', 'created_at')
    list_editable = ('status',)
    search_fields = ('customer_name', 'phone', 'address')
    readonly_fields = ('created_at', 'formatted_items')
    
    def items_summary(self, obj):
        try:
            items = json.loads(obj.items_json)
            summary = []
            for item in items:
                p = Product.objects.filter(id=item['id']).first()
                name = p.name if p else f"ID:{item['id']}"
                summary.append(f"{name} ({item.get('qty', 1)}x {item.get('size', '').upper()})")
            return ", ".join(summary)
        except:
            return "Error loading items"
    items_summary.short_description = "Products Ordered"
    
    fieldsets = (
        ('Customer Info', {
            'fields': ('customer_name', 'email', 'phone', 'address')
        }),
        ('Order Details', {
            'fields': (('total_amount', 'status', 'payment_method'),)
        }),
        ('Purchased Items', {
            'fields': ('formatted_items',),
            'description': 'Customer ne jo suits kharide hain unki details yahan hain.'
        }),
        ('Timestamps', {
            'fields': ('created_at',),
        }),
    )

    def status_badge(self, obj):
        colors = {
            'Pending': '#f39c12',
            'Confirmed': '#27ae60',
            'Shipped': '#2980b9',
            'Delivered': '#2c3e50',
            'Cancelled': '#c0392b',
        }
        color = colors.get(obj.status, '#000')
        return format_html(
            '<span style="background: {}; color: #fff; padding: 4px 10px; border-radius: 20px; font-weight: bold; font-size: 11px;">{}</span>',
            color, obj.get_status_display()
        )
    status_badge.short_description = "Status"

    def formatted_items(self, obj):
        try:
            items = json.loads(obj.items_json)
            html = '<table style="width:100%; border-collapse: collapse; background: #f9f9f9; border-radius: 8px; overflow: hidden;">'
            html += '<tr style="background: #eee; text-align: left;"><th style="padding: 8px;">Product</th><th style="padding: 8px;">Size</th><th style="padding: 8px;">Qty</th></tr>'
            for item in items:
                # Get product name from ID if possible (optional but good)
                p = Product.objects.filter(id=item['id']).first()
                name = p.name if p else f"Product ID: {item['id']}"
                html += f'<tr><td style="padding: 8px; border-top: 1px solid #ddd;">{name}</td>'
                html += f'<td style="padding: 8px; border-top: 1px solid #ddd;">{item["size"].upper()}</td>'
                html += f'<td style="padding: 8px; border-top: 1px solid #ddd;">{item["qty"]}</td></tr>'
            html += '</table>'
            return format_html(html)
        except:
            return obj.items_json
    formatted_items.short_description = "Items Ordered"
