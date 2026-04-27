from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .models import Product, Category, Order
import json

def product_list(request):
    products = Product.objects.all().order_by('-created_at')
    data = []
    for p in products:
        def get_img_url(img_field):
            if not img_field: return None
            s = str(img_field)
            if s.startswith('http'): return s
            if hasattr(img_field, 'url'):
                try: return request.build_absolute_uri(img_field.url)
                except: return s
            return request.build_absolute_uri(settings.MEDIA_URL + s)

        data.append({
            "id": p.id,
            "name": p.name,
            "cat": p.category.slug,
            "price": float(p.price),
            "oldPrice": float(p.old_price) if p.old_price else None,
            "img": get_img_url(p.img),
            "img2": get_img_url(p.img2),
            "img3": get_img_url(p.img3),
            "img4": get_img_url(p.img4),
            "img5": get_img_url(p.img5),
            "sizes": p.sizes.split(','),
            "sold": p.sold,
            "stock": p.stock,
            "desc": p.desc,
            "badge": p.badge if p.badge != 'none' else None,
            "is_trending": p.is_trending,
            "is_featured": p.is_featured,
        })
    return JsonResponse(data, safe=False)

def category_list(request):
    cats = Category.objects.all()
    data = [{"name": c.name, "slug": c.slug, "image": c.image} for c in cats]
    return JsonResponse(data, safe=False)

@csrf_exempt
def create_order(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            order = Order.objects.create(
                customer_name=body.get('name'),
                email=body.get('email'),
                phone=body.get('phone'),
                address=body.get('address'),
                total_amount=body.get('total'),
                payment_method=body.get('payment_method', 'Cash on Delivery'),
                items_json=json.dumps(body.get('items'))
            )
            return JsonResponse({"status": "success", "order_id": order.id})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)
    return JsonResponse({"status": "error", "message": "Method not allowed"}, status=405)
