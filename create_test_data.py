import os
import django
from django.core.files.base import ContentFile
import urllib.request
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'noorani_backend.settings')
django.setup()

from core.models import Category, Product, Order

# 1. Create a Category
category, created = Category.objects.get_or_create(
    name="Test Category",
    defaults={'slug': "test-category"}
)

if created:
    print("Test Category created.")

# 2. Create a Product
try:
    product = Product.objects.get(name="Render Test Product")
except Product.DoesNotExist:
    product = Product(
        name="Render Test Product",
        category=category,
        price=1999.00,
        desc="A beautiful piece of test fabric validating that your Cloudinary storage and Netlify connection are operational! Buy this right now.",
        badge="new",
        stock=50,
        is_trending=True,
        is_featured=True,
    )
    
    # Download a placeholder image from an online service
    try:
        print("Downloading test image from Unsplash to test Cloudinary upload...")
        url = "https://images.unsplash.com/photo-1596464716127-f2a82984de30?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80"
        request = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        response = urllib.request.urlopen(request)
        image_content = response.read()
        
        # Save placeholder to Cloudinary via Django storage mechanism
        product.img.save("test_fabric_image.jpg", ContentFile(image_content))
        print("Image uploaded and saved successfully.")
    except Exception as e:
        print(f"Image upload skipped or failed: {e}")
        product.save()

# 3. Create a Test Order
if not Order.objects.filter(customer_name="Test Customer Name").exists():
    Order.objects.create(
        customer_name="Test Customer Name",
        email="test@example.com",
        phone="03001234567",
        address="123 Render Avenue, Test City",
        total_amount=1999.00,
        status='Pending',
        items_json=json.dumps([{"id": product.id, "name": product.name, "price": 1999.00, "quantity": 1}])
    )
    print("Test Order created successfully.")

print("All Test Data Successfully Injected!")
