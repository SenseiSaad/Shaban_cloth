import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'noorani_backend.settings')
django.setup()

from core.models import Category, Product

def populate():
    # 1. Create Categories
    cats = [
        {"name": "3Pc Collection", "slug": "3piece"},
        {"name": "2Pc Collection", "slug": "2piece"},
        {"name": "Embroidery", "slug": "embroidery"},
        {"name": "Casual Wear", "slug": "casual"},
    ]
    
    cat_objs = {}
    for c in cats:
        obj, created = Category.objects.get_or_create(name=c['name'], slug=c['slug'])
        cat_objs[c['slug']] = obj
        print(f"Category {c['name']} created.")

    # 2. Sample Products
    products = [
        {
            "name": "ANARKALI 3PC",
            "cat": "3piece",
            "price": 5990,
            "oldPrice": 15000,
            "img": "https://images.unsplash.com/photo-1583391733956-3750e0ff4e8b?w=600&q=80",
            "img2": "https://images.unsplash.com/photo-1610030469983-98e550d6193c?w=600&q=80",
            "desc": "Elegant Anarkali 3-piece suit with farshi shalwar. Premium fabric with beautiful embroidery work.",
            "badge": "sale"
        },
        {
            "name": "NAYAB 2PC LAWN",
            "cat": "2piece",
            "price": 3250,
            "oldPrice": 5500,
            "img": "https://images.unsplash.com/photo-1596178065887-1198b6148b2b?w=600&q=80",
            "img2": "https://images.unsplash.com/photo-1609188076864-c35269136b09?w=600&q=80",
            "desc": "Elegant 2-piece lawn set with printed shirt and matching trousers.",
            "badge": "new"
        },
        {
            "name": "FAHMI HEAVY EMB SET",
            "cat": "embroidery",
            "price": 4690,
            "oldPrice": 9000,
            "img": "https://images.unsplash.com/photo-1618932260643-eee4a2f652a6?w=600&q=80",
            "img2": "https://images.unsplash.com/photo-1602810316498-ab67cf68c8e1?w=600&q=80",
            "desc": "Heavy embroidery set with intricate hand work. Premium chiffon fabric.",
            "badge": "sale"
        },
    ]

    for p in products:
        Product.objects.get_or_create(
            name=p['name'],
            category=cat_objs[p['cat']],
            price=p['price'],
            old_price=p['oldPrice'],
            img=p['img'],
            img2=p['img2'],
            desc=p['desc'],
            badge=p['badge']
        )
        print(f"Product {p['name']} created.")

if __name__ == "__main__":
    populate()
