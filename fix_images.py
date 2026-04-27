import os
import django
import json

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'noorani_backend.settings')
django.setup()

from core.models import Product

# High-quality e-commerce placeholders from Unsplash
PLACEHOLDERS = [
    "https://images.unsplash.com/photo-1583391733956-3750e0ff4e8b?w=800&q=80",
    "https://images.unsplash.com/photo-1610030469983-98e550d6193c?w=800&q=80",
    "https://images.unsplash.com/photo-1618932260643-eee4a2f652a6?w=800&q=80",
    "https://images.unsplash.com/photo-1602810316498-ab67cf68c8e1?w=800&q=80",
    "https://images.unsplash.com/photo-1614252235316-8c857d38b5f4?w=800&q=80",
    "https://images.unsplash.com/photo-1585386959984-a4155224a1ad?w=800&q=80",
]

def fix_broken_images():
    products = Product.objects.all()
    count = 0
    base_dir = os.path.dirname(os.path.abspath(__file__))
    media_dir = os.path.join(base_dir, 'media')
    
    for i, p in enumerate(products):
        needs_fix = False
        if not p.img:
            needs_fix = True
        else:
            img_path = str(p.img)
            if not img_path.startswith('http'):
                full_path = os.path.join(media_dir, img_path)
                exists = os.path.exists(full_path)
                print(f"Checking: {p.name} | Path: {full_path} | Exists: {exists}")
                if not exists:
                    needs_fix = True
        
        if needs_fix:
            print(f"Applying fix for: {p.name}")
            p.img = PLACEHOLDERS[i % len(PLACEHOLDERS)]
            p.save()
            count += 1

    print(f"Total fixed: {count}")

if __name__ == "__main__":
    fix_broken_images()
