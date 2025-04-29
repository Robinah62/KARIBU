from django.contrib import admin

# Register your models here.
# accessing our own models
from .models import *
# Register your models here.
admin.site.register(Stock)
admin.site.register(Sale)
admin.site.register(Category)
admin.site.register(Userprofile)
admin.site.register(CreditSale)