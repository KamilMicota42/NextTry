from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200, null=True)
    price = models.FloatField()
    sizes = (
        ('XXL', 'XXL'),
        ('XL', 'XL'),
        ('L', 'L'),
        ('M', 'M'),
        ('S', 'S'),
        ('XS', 'XS'),
    )
    size = models.CharField(max_length=3, choices=sizes, blank=True)
    shoe_size = models.FloatField(null=True, blank=True)
    brand = models.CharField(max_length=200, null=True)
    sexes = (
        ('Unisex', 'Unisex'),
        ('M', 'Male'),
        ('F', 'Female'),
    )
    sex = models.CharField(max_length=6, choices=sexes, default='Unisex')
    conditions = (
        ('New', 'New'),
        ('Very good', 'Very good'),
        ('Good', 'Good'),
        ('Satisfactory', 'Satisfactory'),
    )
    condition = models.CharField(max_length=12, choices=conditions, default='New')
    genres = (
        ('Sweatshirt', 'Sweatshirt'),
        ('T-shirt', 'T-shirt'),
        ('Jacket', 'Jacket'),
        ('Sweater', 'Sweater'),
        ('Pants', 'Pants'),
        ('Shirt', 'Shirt'),
        ('Shoes', 'Shoes'),
        ('Other', 'Other'),
    )
    genre = models.CharField(max_length=10, choices=genres, default='Other')
    image = models.ImageField(null=True, blank=True)
    image1 = models.ImageField(null=True, blank=True)
    image2 = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ""
        return url

    @property
    def image1URL(self):
        try:
            url = self.image1.url
        except:
            url = ""
        return url

    @property
    def image2URL(self):
        try:
            url = self.image2.url
        except:
            url = ""
        return url


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = len(orderitems)
        return total

    @property
    def get_cart_items_ids(self):
        orderitems = self.orderitem_set.all()
        id_list = []
        for item in orderitems:
            id_list.append(item.product.id)
        return id_list


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)

    @property
    def get_total(self):
        total = self.product.price
        return total


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    zipcode = models.CharField(max_length=200, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)


class Favorites(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.id)


class FavoritesItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)
    favorites = models.ForeignKey(Favorites, on_delete=models.SET_NULL, blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)
