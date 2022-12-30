from .models import Product,ProductAttribute,Category
from django.db.models import Min,Max
def get_filters(request):
    cats=Product.objects.distinct().values('category__title','category__id')
    brands=Product.objects.distinct().values('brand__title','brand__id')
    colors=ProductAttribute.objects.distinct().values('color__title','color__id','color__color_code')
    sizes=ProductAttribute.objects.distinct().values('size__title','size__id')
    minMaxPrice=ProductAttribute.objects.aggregate(Min('price'),Max('price'))
    cat2 = Category.objects.all().order_by('-id')
    data={
        'cat2':cat2,
        'cats':cats,
        'brands':brands,
        'colors':colors,
        'sizes':sizes,
        'minMaxPrice':minMaxPrice,
    }
    return data

