from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)

    door = models.CharField(max_length=200, null=True)
    landmark = models.CharField(max_length=200, null=True)

    pincode = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)

    profile_pic = models.ImageField(default="profile1.png", null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    booksdonated = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    CONDITION = (
        ('LIKE NEW', 'LIKE NEW'),
        ('VERY GOOD', 'VERY GOOD'),
        ('GOOD', 'GOOD'),
        ('FAIR', 'FAIR'),
        ('POOR', 'POOR'),
    )

    TAGS = (
        ('1', 'Engineering'),
        ('2', 'Medical'),
        ('3', 'Economics'),
        ('4', 'MPC Inter'),
        ('5', 'BiPC Inter'),
    )

    image = models.ImageField(null=True, blank=True)
    name = models.CharField(max_length=200, null=True)
    price = models.FloatField(null=True)
    author = models.CharField(max_length=200, null=True, blank=True)
    publisher = models.CharField(max_length=200, null=True, blank=True)
    isbn = models.CharField(max_length=200, null=True, blank=True)
    condition = models.CharField(max_length=200, null=True, choices=CONDITION)
    description = models.CharField(max_length=200, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    categories = models.ManyToManyField(Category,choices=TAGS)
    # tags = models.ForeignKey(Tag, null=True, on_delete=models.SET_NULL)
    digital = models.BooleanField(default=False, null=True, blank=True)
    product_count = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


class Order(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('Out for delivery', 'Out for delivery'),
        ('Delivered', 'Delivered'),
    )

    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    date_ordered = models.DateTimeField(auto_now_add=True, null=True)
    status = models.CharField(max_length=200, null=True, choices=STATUS)
    note = models.CharField(max_length=1000, null=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return "%s - %s - with transaction id - %s" % (self.id, self.customer.name, self.transaction_id)

    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital == False:
                shipping = True
        return shipping

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

    @property
    def get_name(self):
        orderitems = self.orderitem_set.all()
        return orderitems


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s) Name - %s, Book - %s, Quantity-%s" % (self.order.id, self.order.customer.name, self.product.name, self.quantity)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    state = models.CharField(max_length=200, null=False)
    zipcode = models.CharField(max_length=200, null=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s - %s - with transaction id - %s" % (self.order.id, self.city, self.order.transaction_id)


class Contact(models.Model):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=200, null=True)
    phone = models.CharField(max_length=13, null=True)
    message = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name


class Donate(models.Model):
    fstnm = models.CharField(max_length=200, null=True)
    lsnm = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=12, null=True)
    phone = models.IntegerField(null=True)
    books = models.IntegerField(null=True)
    doorno = models.CharField(max_length=200, null=True)
    landmark = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    pincode = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.fstnm
