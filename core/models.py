from django.db import models

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

class Order(models.Model):
    customer_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    STATUS_CHOICES = [
        ('Pending', 'Pending ⏳'),
        ('Confirmed', 'Confirmed ✅'),
        ('Shipped', 'Shipped 🚚'),
        ('Delivered', 'Delivered 🎉'),
        ('Cancelled', 'Cancelled ❌'),
    ]
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50, default='Cash on Delivery')
    items_json = models.TextField()  # Store cart items as JSON string
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"Order #{self.id} by {self.customer_name}"
