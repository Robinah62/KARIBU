from django.db import models

# Create your models here.
# borrowing the functionality of inbuilt user from django
from django.contrib.auth.models import AbstractUser
# Create your models here.
# list of tables
# user table( name, email, address, gender, phone number, roles(3))
# sales table(product_name, price, quantity, category, date,salesagent)
# stock table(product_name, product_quantity, cost, type_of stock, supplier_name, date)

# creating user table called user profile .using abstract user above on line 3

class Userprofile(AbstractUser):
    is_salesagent = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)
    is_owner = models.BooleanField(default=False)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=25, unique=True)
    address = models.TextField(max_length=25, blank=True)
    phonenumber = models.CharField(max_length=25, blank=True)
    gender = models.CharField(max_length=10, blank=True, choices=[("Male", "Male"), ("Female", "Female")])

    def __str__(self):
        return self.username # Display username in admin
# category for stock
class Category(models.Model):
    category_name = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.category_name
    

# stock table
class Stock(models.Model):
    category_name = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    item_name = models.CharField(max_length=10, null=True, blank=True)
    total_quantity = models.IntegerField(default=0, null=True, blank=True)
    issued_quantity = models.IntegerField(default=0, null=True, blank=True)
    received_quantity = models.IntegerField(default=0, null=True, blank=True)
    type_of_stock = models.CharField(max_length=20)
    cost = models.FloatField(blank=True)
    supplier_type = models.CharField(
        max_length=20,
        choices=[
            ("individual", "Individual Dealer"),
            ("company", "Company"),
            ("farm", "KGL Farm")
        ]
    )

    date = models.DateField(auto_now_add=True)
    branch = models.CharField(max_length=20, choices=[("Maganjo", "Maganjo"), ("Matugga", "Matugga")])
    unit_price = models.FloatField(blank=True, default=0, null=True)
    unit_cost = models.FloatField(blank=True, default=0, null=True)

    def __str__(self):
        return self.item_name
    

class Sale(models.Model):
    product_name = models.ForeignKey(Stock, on_delete=models.CASCADE)
    unit_price = models.FloatField(blank=True, null=True, default=0)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    customer_name = models.CharField(max_length=100, blank=True, null=True)
    payment_method = models.CharField(
        max_length=10,
        choices=[("Cash", "Cash"), ("Credit", "Credit")],
        default="Cash"
    )
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(blank=True, null=True)
    salesagent = models.ForeignKey(Userprofile, on_delete=models.SET_NULL, null=True, blank=True)
    amount_received = models.FloatField(blank=True, default=0, null=True)
    branch = models.CharField(max_length=20, choices=[("Maganjo", "Maganjo"), ("Matugga", "Matugga")])

    def get_total(self):
        return int(self.unit_price * self.quantity)

    def get_change(self):
        return abs(int(self.get_total() - self.amount_received))

    def __str__(self):
        return f"Sale of {self.quantity} units of {self.product_name}"

class CreditSale(models.Model):
    buyer_name = models.CharField(max_length=100, blank=True)
    national_id = models.CharField(max_length=14)
    location = models.CharField(max_length=100)
    contact = models.CharField(max_length=15)
    amount_due = models.PositiveIntegerField()
    sales_agent = models.ForeignKey(Userprofile, on_delete=models.SET_NULL, null=True)
    due_date = models.DateField(auto_now_add=True)
    product_name = models.ForeignKey(Stock, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0) 
    date_of_dispatch = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.buyer_name} - {self.product_name} ({self.amount_due} UGX)"
    