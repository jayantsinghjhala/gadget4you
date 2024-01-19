from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
# Register your models here.
from app.models import Customer,Product,Cart,PlacedOrder

# admin.site.register(Customer)
# admin.site.register(Product)
# admin.site.register(Cart)
# admin.site.register(PlacedOrder)

@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
     list_display=['id','user','name','locality','city','zipcode','state']
     
@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
     list_display=['id','title','selling_price','discounted_price','description','brand','category','product_image']
     
@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
     list_display=['id','user','product','product_info','quantity']
     def product_info(self,obj):
          link=reverse("admin:app_product_change",args=[obj.product.pk])
          return format_html('<a href="{}">{}</a>',link,obj.product.title)
     
@admin.register(PlacedOrder)
class PlacedOrderModelAdmin(admin.ModelAdmin):
     list_display=['id','user','customer','customer_info','product','quantity','ordered_date','status']
     
     def customer_info(self,obj):
          link=reverse("admin:app_customer_change",args=[obj.customer.pk])
          return format_html('<a href="{}">{}</a>',link,obj.customer.name)