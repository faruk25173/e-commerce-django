from decimal import Decimal
from typing import Dict, Union, Any

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView
from sslcommerz_python.payment import SSLCSession

from .models import Banner,Category,Brand,Product,ProductAttribute,CartOrder,CartOrderItems,ProductReview,Wishlist,UserAddressBook,ShippingCharge, Color, Cart
from django.db.models import Max,Min,Count,Avg
from django.db.models.functions import ExtractMonth
from django.template.loader import render_to_string
from .forms import SignupForm,ReviewAdd,AddressBookForm,ProfileForm
from django.contrib.auth import login,authenticate
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ProductSerializer,BrandSerializer,CategorySerializer,RegisterSerializer,ProductAttributeSerializer
from django.core import paginator
from django.core.paginator import Paginator

from django.utils import timezone

#from notification.notific import SendNotification
#paypal
from django.urls import reverse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from paypal.standard.forms import PayPalPaymentsForm
# Home Page
def home(request):
    banners=Banner.objects.all().order_by('-id')
    index_product = Product.objects.all()
    data=Product.objects.filter(is_featured=True).order_by('-id')
   # paginator=Paginator(index_product,3)
    #page_number=request.GET.get('page')
    #index_product_final=paginator.get_page(page_number)

    return render(request,'index.html',{'data':data,'banners':banners,'index_product':index_product,})
# Category
def category_list(request):
    data=Category.objects.all().order_by('-id')
    return render(request,'category_list.html',{'data':data})

# Brand
def brand_list(request):
    data=Brand.objects.all().order_by('-id')
    return render(request,'brand_list.html',{'data':data})

# Product List
def product_list(request):
    total_data=Product.objects.count()
    data=Product.objects.all().order_by('-id')[:8]
    min_price=ProductAttribute.objects.aggregate(Min('price'))
    max_price=ProductAttribute.objects.aggregate(Max('price'))
    return render(request,'product_list.html',
        {
            'data':data,
            'total_data':total_data,
            'min_price':min_price,
            'max_price':max_price,
        }
        )

# Product List According to Category
def category_product_list(request,cat_id):
    category=Category.objects.get(id=cat_id)
    data=Product.objects.filter(category=category).order_by('-id')
    return render(request,'category_product_list.html',{
            'data':data,          })



# Product List According to Brand
def brand_product_list(request,brand_id):
    brand=Brand.objects.get(id=brand_id)

    data=Product.objects.filter(brand=brand).order_by('-id')
    return render(request,'brand_product_list.html',{
            'data':data,
            })

# Product Detail
def product_detail(request,slug,id):
    product=Product.objects.get(id=id)
    related_products=Product.objects.filter(category=product.category).exclude(id=id)[:3]
    colors=ProductAttribute.objects.filter(product=product).values('color__id','color__title','color__color_code').distinct()
    sizes=ProductAttribute.objects.filter(product=product).values('size__id', 'size__title', 'color', 'size', 'id','image', 'price', 'quantity', 'color__id','color__title').distinct()
    charges = ShippingCharge.objects.all().order_by('id')
    images=ProductAttribute.objects.filter(product=product)

    reviewForm=ReviewAdd()

    # Check
    canAdd=True
    reviewCheck=ProductReview.objects.filter(user=request.user,product=product).count()
    if request.user.is_authenticated:
        if reviewCheck > 0:
            canAdd=False
    # End

    # Fetch reviews
    reviews=ProductReview.objects.filter(product=product)
    # End

    # Fetch avg rating for reviews
    avg_reviews=ProductReview.objects.filter(product=product).aggregate(avg_rating=Avg('review_rating'))

    # End

    return render(request, 'product_detail.html',{'data':product,'related_products':related_products,'colors':colors,'sizes':sizes,'reviewForm':reviewForm,'canAdd':canAdd,'reviews':reviews,'avg_reviews':avg_reviews,'charges':charges, 'images':images})

# Search
def search(request):
    q=request.GET['q']
    data=Product.objects.filter(title__icontains=q).order_by('-id')
    return render(request,'search.html',{'data':data})

# Filter Data
@login_required()
def filter_data(request):
    colors=request.GET.getlist('color[]')
    categories=request.GET.getlist('category[]')
    brands=request.GET.getlist('brand[]')
    sizes=request.GET.getlist('size[]')
    minPrice=request.GET['minPrice']
    maxPrice=request.GET['maxPrice']
    allProducts=Product.objects.all().order_by('-id').distinct()
    allProducts=allProducts.filter(productattribute__price__gte=minPrice)
    allProducts=allProducts.filter(productattribute__price__lte=maxPrice)
    if len(colors)>0:
        allProducts=allProducts.filter(productattribute__color__id__in=colors).distinct()
    if len(categories)>0:
        allProducts=allProducts.filter(category__id__in=categories).distinct()
    if len(brands)>0:
        allProducts=allProducts.filter(brand__id__in=brands).distinct()
    if len(sizes)>0:
        allProducts=allProducts.filter(productattribute__size__id__in=sizes).distinct()
    t=render_to_string('ajax/product-list.html',{'data':allProducts})
    return JsonResponse({'data':t})

# Load More
def load_more_data(request):
    offset=int(request.GET['offset'])
    limit=int(request.GET['limit'])
    data=Product.objects.all().order_by('-id')[offset:offset+limit]
    t=render_to_string('ajax/product-list.html',{'data':data})
    return JsonResponse({'data':t}
)

# Add to cart
def add_to_cart(request):
   # del request.session['cartdata']
   cart_p = {}
   cart_p[str(request.GET['id'])] = {
       'image': request.GET['image'],
       'title': request.GET['title'],
       'qty': request.GET['qty'],
       'color': request.GET['color'],
       'size': request.GET['size'],
       'price': request.GET['price']

   }
   if 'cartdata' in request.session:
       if str(request.GET['id']) in request.session['cartdata']:
           cart_data = request.session['cartdata']
           cart_data[str(request.GET['id'])]['qty'] = int(cart_p[str(request.GET['id'])]['qty'])
           cart_data.update(cart_data)
           request.session['cartdata'] = cart_data
       else:
           cart_data = request.session['cartdata']
           cart_data.update(cart_p)
           request.session['cartdata'] = cart_data
   else:
       request.session['cartdata'] = cart_p
   return JsonResponse({'data': request.session['cartdata'], 'totalitems': len(request.session['cartdata'])})



# Cart List Page
def cart_list(request):
    sub_total = 0
    shipping_charge: int = 0
    total_amt=0

    if 'cartdata' in request.session:
        for p_id,item in request.session['cartdata'].items():
            sub_total += int(item['qty']) * float(item['price'])
            shipping_charge += int(item['qty']) * 50
            total_amt = sub_total + shipping_charge

        return render(request, 'cart.html',{'cart_data':request.session['cartdata'],'totalitems':len(request.session['cartdata']),'total_amt':total_amt,'shipping_charge':shipping_charge,' sub_total': sub_total})
    else:
        return render(request, 'cart.html',{'cart_data':'','totalitems':0,'total_amt':total_amt,' sub_total': sub_total,'shipping_charge':shipping_charge})




# Delete Cart Item
def delete_cart_item(request):
    sub_total = 0
    shipping_charge = 0
    total_amount = 0
    p_id=str(request.GET['id'])
    if 'cartdata' in request.session:
        if p_id in request.session['cartdata']:
            cart_data=request.session['cartdata']
            del request.session['cartdata'][p_id]
            request.session['cartdata']=cart_data
    total_amt=0
    for p_id,item in request.session['cartdata'].items():
        sub_total += int(item['qty']) * float(item['price'])
        shipping_charge += int(item['qty']) * 50
        total_amount += (sub_total + shipping_charge)
    t=render_to_string('ajax/cart-list.html',{'cart_data':request.session['cartdata'],'totalitems':len(request.session['cartdata']),'total_amt':total_amount,'shipping_charge':shipping_charge,'sub_total':sub_total})
    return JsonResponse({'data':t,'totalitems':len(request.session['cartdata'])})

# update Cart Item
def update_cart_item(request):
    sub_total = 0
    shipping_charge = 0
    total_amount = 0
    p_id=str(request.GET['id'])
    p_qty=request.GET['qty']
    if 'cartdata' in request.session:
        if p_id in request.session['cartdata']:
            cart_data=request.session['cartdata']
            cart_data[str(request.GET['id'])]['qty']=p_qty
            request.session['cartdata']=cart_data
    total_amt=0
    for p_id,item in request.session['cartdata'].items():
        sub_total += int(item['qty']) * float(item['price'])
        shipping_charge += int(item['qty']) * 50
        total_amount = (sub_total + shipping_charge)
    t=render_to_string('ajax/cart-list.html',{'cart_data':request.session['cartdata'],'totalitems':len(request.session['cartdata']),'total_amt':total_amount,'shipping_charge':shipping_charge,'sub_total':sub_total})
    return JsonResponse({'data':t,'totalitems':len(request.session['cartdata'])})

# Signup Form
def signup(request):
    if request.method=='POST':
        form=SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username=form.cleaned_data.get('username')
            pwd=form.cleaned_data.get('password1')
            user=authenticate(username=username,password=pwd)
            login(request, user)
            return redirect('home')
    form=SignupForm
    return render(request, 'registration/signup.html',{'form':form})


# Checkout
class CheckoutTemplateView(TemplateView):
    def get( self, request, *args, **kwargs):
        sub_total = 0
        shipping_charge = 0
        total_amt=0
        totalAmt=0
        if 'cartdata' in request.session:
            for p_id,item in request.session['cartdata'].items():
                sub_total += int(item['qty']) * float(item['price'])
                shipping_charge += int(item['qty']) * 50
                totalAmt = (sub_total + shipping_charge)


        # Order
        order=CartOrder.objects.create(
                user=request.user,
                total_amt=totalAmt
            )
        # End
        for p_id,item in request.session['cartdata'].items():
            total_amt=(sub_total + shipping_charge)
            # OrderItems
            items=CartOrderItems.objects.create(
                order=order,
                att_id=p_id,
                invoice_no='INV-'+str(order.id),
                item=item['title'],
                image=item['image'],
                color=item['color'],
                size=item['size'],
                qty=item['qty'],
                price=item['price'],
                delivery_charge=str(50),
                total=float(item['qty'])*float(item['price'])+ int(item['qty']) * 50
                )

            qtys = int(item['qty'])
            qt = ProductAttribute.objects.get(id=p_id)

            qt.quantity = int(qt.quantity) - qtys
            qt.save()

            # End

        address=UserAddressBook.objects.filter(user=request.user,status=True).first()
        return render(request, 'checkout.html',{'cart_data':request.session['cartdata'],'totalitems':len(request.session['cartdata']),'total_amt':total_amt,'address':address,'shipping_charge':shipping_charge})

def post(self, request, *args, **kwargs):
        store_id = settings.STORE_ID
        store_pass = settings.STORE_PASS
        mypayment = SSLCSession(sslc_is_sandbox=True, sslc_store_id=store_id, sslc_store_pass=store_pass)

        status_url = request.build_absolute_uri(reverse('status'))
        mypayment.set_urls(success_url=status_url, fail_url=status_url, cancel_url=status_url,
                           ipn_url=status_url)

        order_qs = CartOrderItems.objects.filter(user=request.user)
        order_item = order_qs.item.all()
        order_item_count = order_qs.item.count()
        order_total = order_qs.total

        mypayment.set_product_integration(total_amount=Decimal(order_total), currency='BDT',
                                          product_category='clothing', product_name=order_item,
                                          num_of_item=order_item_count, shipping_method='Courier',
                                          product_profile='None')

        current_user = request.user
        mypayment.set_customer_info(name=current_user.profile.full_name, email=current_user.email,
                                    address1=current_user.profile.address,
                                    address2=current_user.profile.address, city=current_user.profile.city,
                                    postcode=current_user.profile.zipcode, country=current_user.profile.country,
                                    phone=current_user.profile.phone)

        mypayment.set_shipping_info(shipping_to=current_user.profile.address,
                                    address=current_user.profile.address, city=current_user.profile.city,
                                    postcode=current_user.profile.zipcode, country=current_user.profile.country)

        response_data = mypayment.init_payment()

        return redirect(response_data['GatewayPageURL'])


@csrf_exempt
def sslc_status(request):
    if request.method == 'post' or request.method == 'POST':
        payment_data = request.POST
        status = payment_data['status']
        if status == 'VALID':
            val_id = payment_data['val_id']
            tran_id = payment_data['tran_id']

            return HttpResponseRedirect(reverse('sslc_complete', kwargs={'val_id': val_id, 'tran_id': tran_id}))

    return render(request, 'status.html')


def sslc_complete(request, val_id, tran_id):
    order_qs = CartOrderItems.objects.filter(user=request.user)
    order = order_qs
    order.orderId = val_id
    order.paymentId = tran_id
    order.save()

    order_qs = CartOrderItems.objects.filter(user=request.user)

    for qt in order_qs:
        item_id = qt.att_id


        qt_source = ProductAttribute.object.get(id=item_id,)

        qt_source.quantity = qt_source.quantity - qt.qty
        qt_source.save()

    return redirect('store:index')


# Save Review
def save_review(request,pid):
    product=Product.objects.get(pk=pid)
    user=request.user
    review=ProductReview.objects.create(
        user=user,
        product=product,
        review_text=request.POST['review_text'],
        review_rating=request.POST['review_rating'],
        )
    data={
        'user':user.username,
        'review_text':request.POST['review_text'],
        'review_rating':request.POST['review_rating']
    }

    # Fetch avg rating for reviews
    avg_reviews=ProductReview.objects.filter(product=product).aggregate(avg_rating=Avg('review_rating'))
    # End

    return JsonResponse({'bool':True,'data':data,'avg_reviews':avg_reviews})

# User Dashboard
import calendar
def my_dashboard(request):
    orders=CartOrder.objects.annotate(month=ExtractMonth('order_dt')).values('month').annotate(count=Count('id')).values('month','count')
    monthNumber=[]
    totalOrders=[]
    for d in orders:
        monthNumber.append(calendar.month_name[d['month']])
        totalOrders.append(d['count'])
    return render(request, 'user/dashboard.html',{'monthNumber':monthNumber,'totalOrders':totalOrders})

# My Orders
def my_orders(request):
    orders=CartOrder.objects.filter(user=request.user).order_by('-id')
    return render(request, 'user/orders.html',{'orders':orders})

# Order Detail
def my_order_items(request,id):
    order=CartOrder.objects.get(pk=id)
    orderitems=CartOrderItems.objects.filter(order=order).order_by('-id')
    return render(request, 'user/order-items.html',{'orderitems':orderitems})

# Wishlist
def add_wishlist(request):
    pid=request.GET['product']
    product=Product.objects.get(id=pid)
    data={}
    checkw=Wishlist.objects.filter(product=product,user=request.user).count()
    if checkw > 0:
        data={
            'bool':False
        }
    else:
        wishlist=Wishlist.objects.create(
            product=product,
            user=request.user
        )
        data={
            'bool':True
        }
    return JsonResponse(data)

# My Wishlist
def my_wishlist(request):
    wlist=Wishlist.objects.filter(user=request.user).order_by('-id')
    return render(request, 'user/wishlist.html',{'wlist':wlist})

def remove_item_from_wishlist(request):
    pid = request.GET['id']
    item = get_object_or_404(Product, id=pid)
    orders = Wishlist.objects.filter(user=request.user, product=item)
    if orders.exists():
            orders.delete()
            t = render_to_string('user/wishlist.html', {'wlist': len(orders.product)})
            return JsonResponse({'data':t,'wlist': len(orders.product)})

# My Reviews
def my_reviews(request):
    reviews=ProductReview.objects.filter(user=request.user).order_by('-id')
    return render(request, 'user/reviews.html',{'reviews':reviews})

# My AddressBook
def my_addressbook(request):
    addbook=UserAddressBook.objects.filter(user=request.user).order_by('-id')
    return render(request, 'user/addressbook.html',{'addbook':addbook})

# Save addressbook
def save_address(request):
    msg=None
    if request.method=='POST':
        form=AddressBookForm(request.POST)
        if form.is_valid():
            saveForm=form.save(commit=False)
            saveForm.user=request.user
            if 'status' in request.POST:
                UserAddressBook.objects.update(status=False)
            saveForm.save()
            msg='Data has been saved'
    form=AddressBookForm
    return render(request, 'user/add-address.html',{'form':form,'msg':msg})

# Activate address
def activate_address(request):
    a_id=str(request.GET['id'])
    UserAddressBook.objects.update(status=False)
    UserAddressBook.objects.filter(id=a_id).update(status=True)
    return JsonResponse({'bool':True})

# Edit Profile
def edit_profile(request):
    msg=None
    if request.method=='POST':
        form=ProfileForm(request.POST,instance=request.user)
        if form.is_valid():
            form.save()
            msg='Data has been saved'
    form=ProfileForm(instance=request.user)
    return render(request, 'user/edit-profile.html',{'form':form,'msg':msg})

# Update addressbook
def update_address(request,id):
    address=UserAddressBook.objects.get(pk=id)
    msg=None
    if request.method=='POST':
        form=AddressBookForm(request.POST,instance=address)
        if form.is_valid():
            saveForm=form.save(commit=False)
            saveForm.user=request.user
            if 'status' in request.POST:
                UserAddressBook.objects.update(status=False)
            saveForm.save()
            msg='Data has been saved'
    form=AddressBookForm(instance=address)
    return render(request, 'user/update-address.html',{'form':form,'msg':msg})

@api_view(['GET'])
def apiOverview(request):
    api_urls = {
        'List':'/task-list/',
        'Detail View':'/task-detail/<str:pk>/',
        'Create':'/task-create/',
        }

    return Response(api_urls)

@api_view(['GET'])
def categoryList(request):
    categoryList = Category.objects.all().order_by('-id')
    serializer = CategorySerializer(categoryList, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def brandList(request):
    brandList = Brand.objects.all().order_by('-id')
    serializer = BrandSerializer(brandList, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def brandproductList(request,brand_id):
    brandlist=Brand.objects.get(id=brand_id)
    brandproducts=Product.objects.filter(brand=brandlist).order_by('-id')
    serializer = ProductSerializer(brandproducts, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def categoryproductList(request,cat_id):
    categorylist = Category.objects.get(id=cat_id)
    categoryproduct = Product.objects.filter(category=categorylist).order_by('-id')
    serializer = ProductSerializer(categoryproduct, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def productDetail(request, pro_id):
    tasks = Product.objects.get(id=pro_id)
    serializer = ProductSerializer(tasks, many=False)
    return Response(serializer.data)


@api_view(['POST'])
def userRegistration(request):
    user = RegisterSerializer(data=request.data)

    if user.is_valid():
        user.save()

    return Response(user.data)

@api_view(['GET'])
def productcolor(request,pro_id):
    prolist=Product.objects.get(id=pro_id)
    colors=ProductAttribute.objects.filter(product=prolist).distinct()
    serializer = ProductAttributeSerializer(colors, many=True)
    return Response(serializer.data)