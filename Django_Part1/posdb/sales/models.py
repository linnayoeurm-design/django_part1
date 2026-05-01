from django.db import models
from django.contrib.auth.models import User



# =========================
# PRODUCT MODEL
# =========================
class Product(models.Model):
    CATEGORY_CHOICES = [
        ('food', 'អាហារ និងភេសជ្ជៈ'),
        ('electronics', 'អេឡិចត្រូនិក'),
        ('clothing', 'សម្លៀកបំពាក់'),
        ('household', 'គ្រឿងសង្ហារឹម'),
        ('other', 'ផ្សេងៗ'),
    ]

    name = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    barcode = models.CharField(max_length=50, unique=True, blank=True)
    is_active = models.BooleanField(default=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True)


    def __str__(self):
        return self.name

    def __str__(self):
        return f"{self.name} - ${self.price} (Stock: {self.stock})"

    class Meta:
        ordering = ['name']


# =========================
# ORDER MODEL
# =========================
class Order(models.Model):
    STATUS_CHOICES = [
        ('open', 'បានបើក'),
        ('paid', 'បានបង់'),
        ('refunded', 'បានសង'),
        ('cancelled', 'បានលុបចោល'),
    ]

    cashier = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='orders'
    )

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    created_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    @property
    def total(self):
        """Calculate total price of all items in this order"""
        return sum(item.subtotal() for item in self.items.all())

    def __str__(self):
        return f"Order #{self.pk} - {self.status} - ${self.total:.2f}"

    class Meta:
        ordering = ['-created_at']


# =========================
# ORDER ITEM MODEL
# =========================
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=8, decimal_places=2)

    def subtotal(self):
        return self.unit_price * self.quantity

    def save(self, *args, **kwargs):
        # auto set price if not set
        if not self.unit_price:
            self.unit_price = self.product.price

        super().save(*args, **kwargs)