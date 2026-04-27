import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'noorani_backend.settings')
django.setup()

from core.models import Product, Category

def update_products():
    # 1. Create Casual Wear category if not exists
    casual_cat, created = Category.objects.get_or_create(
        slug='casual',
        defaults={'name': 'Casual Wear', 'image': 'https://images.unsplash.com/photo-1585386959984-a4155224a1ad?w=500'}
    )
    if not created:
        casual_cat.name = 'Casual Wear'
        casual_cat.save()

    # 2. Update specific products as 'new' (New Arrivals)
    new_ids = [14, 15, 30, 22, 23]
    Product.objects.filter(id__in=new_ids).update(badge='new')
    print(f"Updated {len(new_ids)} products to 'New Arrivals'")

    # 3. Update specific products to 'Casual Wear' category
    casual_ids = [16, 17, 18, 20]
    Product.objects.filter(id__in=casual_ids).update(category=casual_cat)
    print(f"Moved {len(casual_ids)} products to 'Casual Wear' category")

if __name__ == "__main__":
    update_products()
