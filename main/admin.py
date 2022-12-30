from django.contrib import admin
from .models import Banner,Category,Brand,Color,Size,Product,ProductAttribute,CartOrder,CartOrderItems,ProductReview,Wishlist,UserAddressBook,ShippingCharge, Cart

# admin.site.register(Banner)
class BrandAdmin(admin.ModelAdmin):
    list_display=('title','image_tag')
admin.site.register(Brand,BrandAdmin)


admin.site.register(Size)

class BannerAdmin(admin.ModelAdmin):
    list_display=('alt_text','image_tag')
admin.site.register(Banner,BannerAdmin)

class CategoryAdmin(admin.ModelAdmin):
    list_display=('title','image_tag')
admin.site.register(Category,CategoryAdmin)

class ColorAdmin(admin.ModelAdmin):
    list_display=('title','color_bg')
admin.site.register(Color,ColorAdmin)

class ProductAdmin(admin.ModelAdmin):
    list_display=('id','title','category','brand','status','is_featured')
    list_editable=('status','is_featured')
admin.site.register(Product,ProductAdmin)

# Product Attribute
class ProductAttributeAdmin(admin.ModelAdmin):
    list_display=('id','image_tag','product','price','color','size','quantity','status')
admin.site.register(ProductAttribute,ProductAttributeAdmin)

# Order
class CartOrderAdmin(admin.ModelAdmin):
    list_editable=('paid_status','order_status')
    list_display=('user','total_amt','paid_status','order_dt','order_status')
admin.site.register(CartOrder,CartOrderAdmin)

class CartOrderItemsAdmin(admin.ModelAdmin):
    list_display=('invoice_no','item','image_tag','qty','price','delivery_charge','total')
admin.site.register(CartOrderItems,CartOrderItemsAdmin)


class ProductReviewAdmin(admin.ModelAdmin):
    list_display=('user','product','review_text','get_review_rating')
admin.site.register(ProductReview,ProductReviewAdmin)


class WishlistAdmin(admin.ModelAdmin):
    list_display=('user','product')
admin.site.register(Wishlist,WishlistAdmin)

class UserAddressBookAdmin(admin.ModelAdmin):
    list_display=('user','address','status')
admin.site.register(UserAddressBook,UserAddressBookAdmin)

class ShippingChargeAdmin(admin.ModelAdmin):
    list_display=('title','shipping_type','shipping_charge','product')
admin.site.register(ShippingCharge,ShippingChargeAdmin)

class CartAdmin(admin.ModelAdmin):
    list_display=('title','color','size','image','quantity','price')
admin.site.register(Cart,CartAdmin)
