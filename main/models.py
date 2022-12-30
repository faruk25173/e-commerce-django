from django.db import models
from django.db.models import Avg
from django.utils.html import mark_safe
from django.contrib.auth.models import User
# Banner
class Banner(models.Model):
    img=models.ImageField(upload_to="banner_imgs/")
    alt_text=models.CharField(max_length=300)

    class Meta:
        verbose_name_plural='Banners'

    def image_tag(self):
        return mark_safe('<img src="%s" width="100" />' % (self.img.url))

    def __str__(self):
        return self.alt_text

# Category
class Category(models.Model):
    title=models.CharField(max_length=100)
    image=models.ImageField(upload_to="cat_imgs/")

    class Meta:
        verbose_name_plural='Categories'

    def image_tag(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))

    def __str__(self):
        return self.title

    def get_category_name(self, obj):
        if obj.cat_id:
            return obj.category.title
        return ""

# Brand
class Brand(models.Model):
    title=models.CharField(max_length=100)
    image=models.ImageField(upload_to="brand_imgs/")

    class Meta:
        verbose_name_plural='Brands'

    def __str__(self):
        return self.title

    def image_tag(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))

    def get_brand_name(self, obj):
        if obj.brand_id:
            return obj.brand.title
        return ""
# Color
class Color(models.Model):
    title=models.CharField(max_length=100)
    color_code=models.CharField(max_length=100)

    class Meta:
        verbose_name_plural='Colors'

    def color_bg(self):
        return mark_safe('<div style="width:30px; height:30px; background-color:%s"></div>' % (self.color_code))

    def __str__(self):
        return self.title

# Size
class Size(models.Model):
    title=models.CharField(max_length=100)

    class Meta:
        verbose_name_plural='Sizes'

    def __str__(self):
        return self.title


# Product Model
class Product(models.Model):
    title=models.CharField(max_length=200)
    slug=models.CharField(max_length=400)
    detail=models.TextField()
    specs=models.TextField()
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    brand=models.ForeignKey(Brand,on_delete=models.CASCADE)
    status=models.BooleanField(default=True)
    is_featured=models.BooleanField(default=False)

    class Meta:
        verbose_name_plural='Products'

    def __str__(self):
        return self.title

    def get_avg_rating(self):
        reviews = ProductReview.objects.filter(product=self).aggregate(rating_avg=Avg('review_rating'))
        return (reviews['rating_avg'])

# Product Attribute

availability = (
    ('available', 'Available'),
    ('notavailable', 'Not-available'),
)
class ProductAttribute(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    color=models.ForeignKey(Color,on_delete=models.CASCADE)
    size=models.ForeignKey(Size,on_delete=models.CASCADE)
    price=models.PositiveIntegerField(default=0)
    image=models.ImageField(upload_to="product_imgs/",null=True)
    quantity=models.PositiveIntegerField(default=1)
    status =models.CharField(choices=availability,default='available',max_length=150)

    class Meta:
        verbose_name_plural='ProductAttributes'

    def __str__(self):
        return self.product.title

    def image_tag(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))



# Order
status_choice=(
        ('process','In Process'),
        ('shipped','Shipped'),
        ('delivered','Delivered'),
    )
class CartOrder(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    total_amt=models.FloatField()
    paid_status=models.BooleanField(default=False)
    order_dt=models.DateTimeField(auto_now_add=True)
    order_status=models.CharField(choices=status_choice,default='process',max_length=150)

    class Meta:
        verbose_name_plural='Orders'

# OrderItems
class CartOrderItems(models.Model):
    order=models.ForeignKey(CartOrder,on_delete=models.CASCADE)
    att_id = models.CharField(max_length=150,null=True)
    invoice_no=models.CharField(max_length=150)
    item=models.CharField(max_length=150)
    color=models.CharField(max_length=150,null=True)
    size=models.CharField(max_length=150,null=True)
    image=models.CharField(max_length=200)
    qty=models.IntegerField()
    price=models.FloatField()
    delivery_charge=models.CharField(max_length=150,null=True)
    total=models.FloatField()

    class Meta:
        verbose_name_plural='Order Items'

    def image_tag(self):
        return mark_safe('<img src="/media/%s" width="50" height="50" />' % (self.image))

# Product Review
RATING=(
    (1,'1'),
    (2,'2'),
    (3,'3'),
    (4,'4'),
    (5,'5'),
)
class ProductReview(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    review_text=models.TextField()
    review_rating=models.CharField(choices=RATING,max_length=150)

    class Meta:
        verbose_name_plural='Reviews'

    def get_review_rating(self):
        return self.review_rating

    def myrating(self):
        myvalue = self. review_rating.aggregate(Avg('review_rating'))
        return myvalue




# WishList
class Wishlist(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural='Wishlist'

# AddressBook
class UserAddressBook(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    mobile=models.CharField(max_length=50,null=True)
    address=models.TextField()
    status=models.BooleanField(default=False)

    class Meta:
        verbose_name_plural='AddressBook'

class ShippingCharge(models.Model):
    title = models.CharField(max_length=100)
    shipping_type = models.CharField(max_length=100)
    shipping_charge = models.PositiveIntegerField(default=0)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

class Meta:
    verbose_name_plural = 'charge'

def __str__(self):
    return self.title


class Cart(models.Model):
    title=models.CharField(max_length=100)
    image = models.CharField(max_length=200)
    color= models.CharField(max_length=100)
    size= models.CharField(max_length=100)
    price= models.PositiveIntegerField(default=0)
    quantity=models.PositiveIntegerField(default=1)
    created = models.DateTimeField(auto_now_add=True)

class Meta:
    verbose_name_plural = 'carts'

