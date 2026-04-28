from django.db import models
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    image = models.URLField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"

class Product(models.Model):
    BADGE_CHOICES = [
        ('new', 'New'),
        ('sale', 'Sale'),
        ('none', 'None'),
    ]
    
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    old_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    img = models.ImageField(upload_to='products/')
    img2 = models.ImageField(upload_to='products/', blank=True, null=True)
    img3 = models.ImageField(upload_to='products/', blank=True, null=True)
    img4 = models.ImageField(upload_to='products/', blank=True, null=True)
    img5 = models.ImageField(upload_to='products/', blank=True, null=True)
    sizes = models.CharField(max_length=100, default='s,m,l,xl')
    sold = models.IntegerField(default=0)
    stock = models.IntegerField(default=100)
    desc = models.TextField()
    badge = models.CharField(max_length=10, choices=BADGE_CHOICES, default='none')
    is_trending = models.BooleanField(default=False, verbose_name="Show in Trending?")
    is_featured = models.BooleanField(default=False, verbose_name="Show in Hero/Featured?")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Cart(models.Model):
    session_key = models.CharField(max_length=40, null=True, blank=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart {self.id}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    size = models.CharField(max_length=50, blank=True, null=True)
    color = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Cart {self.cart.id}"

class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending ⏳'),
        ('Confirmed', 'Confirmed ✅'),
        ('Packed', 'Packed 📦'),
        ('Shipped', 'Shipped 🚚'),
        ('Delivered', 'Delivered 🎉'),
        ('Cancelled', 'Cancelled ❌'),
    ]

    order_id = models.CharField(max_length=20, unique=True, editable=False, null=True, blank=True)
    first_name = models.CharField(max_length=100, default="Unknown")
    last_name = models.CharField(max_length=100, default="", blank=True)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    full_address = models.TextField()
    
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    payment_method = models.CharField(max_length=50, default='Cash on Delivery')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.order_id:
            year = timezone.now().year
            last_order = Order.objects.filter(order_id__startswith=f'ORD-{year}').order_by('-id').first()
            if last_order:
                # order_id format: ORD-YYYY-000000X
                try:
                    last_number = int(last_order.order_id.split('-')[-1])
                    new_number = last_number + 1
                except ValueError:
                    new_number = 1
            else:
                new_number = 1
            
            self.order_id = f"ORD-{year}-{new_number:06d}"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.order_id} - {self.first_name} {self.last_name}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    
    # Snapshots
    product_name_snapshot = models.CharField(max_length=200)
    price_snapshot = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    size = models.CharField(max_length=50, blank=True, null=True)
    color = models.CharField(max_length=50, blank=True, null=True)

    def get_cost(self):
        return self.price_snapshot * self.quantity

    def __str__(self):
        return f"{self.quantity}x {self.product_name_snapshot} for {self.order.order_id}"

