from django.shortcuts import render,redirect
from django.views import View
from .models import Customer, Product, Cart, PlacedOrder
from .forms import CustomerRegistrationForm,CustomerProfileForm
from django.contrib import messages
from django.db.models import F
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
import pdb
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
#pdb.set_trace(test)
# def home(request):
#      return render(request, 'app/home.html')

class ProductView(View):
     def get(self,request):
          mobiles=Product.objects.filter(category='M')
          mobile_accessories=Product.objects.filter(category='MA')
          laptops=Product.objects.filter(category='L')
          smart_wearables=Product.objects.filter(category='SW')
          
          return render(
            request,
            'app/home.html',
            {
                'mobiles': mobiles,
                'mobile_accessories': mobile_accessories,
                'laptops': laptops,
                'smart_wear': smart_wearables
            }
          )
# def product_detail(request):
#  return render(request, 'app/productdetail.html')

class ProductDetailView(View):
  def get(self,request,id):
    product=Product.objects.get(pk=id)
    in_cart=0
    if request.user.is_authenticated:
      cart_item=Cart.objects.filter(user=request.user,product=product)
      if cart_item: 
        in_cart=1
    return render(
      request,
      'app/productdetail.html',
      {
        'in_cart':in_cart,
        'product':product
      })
    
@method_decorator(login_required, name='dispatch')
class AddToCartView(View):
  def get(self,request):
    return redirect('showcart')

  def post(self, request):
        user = request.user
        product_id = request.POST.get('product_id')
        product = Product.objects.get(id=product_id)
        cart_item = Cart.objects.filter(user=user, product=product).first()
        if cart_item:
            cart_item.quantity=F('quantity') + 1
            cart_item.save()
        else:
            Cart(user=user, product=product, quantity=1).save()
        return redirect('showcart')
  
@login_required  
def show_cart(request):
  if request.user.is_authenticated:
    user=request.user
    products=Cart.objects.filter(user=user)
    amount=0.0
    shipping_amount=70.0
    total_amount=0.0
    total_shipping=0.0
    cart_product=[p for p in Cart.objects.all() if p.user==user]
    # print(cart_product)
    if cart_product:
      for p in cart_product:
        temp_amount=(p.quantity * p.product.discounted_price)
        amount+=temp_amount
        total_amount=amount + shipping_amount
        total_shipping+=shipping_amount
    return render(request, 'app/addtocart.html', {'products': products,'total_amount':total_amount,'amount':amount,'total_shipping':total_shipping})

@login_required
def change_cart(request):
  if request.method=="GET":
    action=request.GET['action']
    cart_id=request.GET['cart_id']
    cart_item = Cart.objects.get(id=cart_id)
    
    if cart_item:
      # cart_item.update(quantity=F('quantity')+1)#does not work, only work on direct objects
      if action in ["plus","plus_b"]:
        Cart.objects.filter(id=cart_id).update(quantity=F('quantity') + 1)
      elif action in ["minus","minus_b"]:
        Cart.objects.filter(id=cart_id).update(quantity=F('quantity') - 1)
      elif action=="remove":
        try:
            product = Cart.objects.get(id=cart_id, user=request.user)
            product.delete()
        except Cart.DoesNotExist:
            return HttpResponseBadRequest("Invalid cart item")
    if action in ["minus","plus","remove"]:      
      amount=0.0
      shipping_amount=70.0
      total_amount=0.0
      total_shipping=0.0
      cart_product=[p for p in Cart.objects.all() if p.user==request.user]
      # print(cart_product)
      if cart_product:
        for p in cart_product:
          temp_amount=(p.quantity * p.product.discounted_price)
          amount+=temp_amount
          total_amount=amount + shipping_amount
          total_shipping+=shipping_amount
          
    if action in ["minus_b","plus_b"]: 
      cart_product = Cart.objects.get(id=cart_id)
      amount=cart_item.product.discounted_price * cart_product.quantity
      total_shipping = 70.0
      total_amount= amount + total_shipping
    
    if action=="remove":
      data={
        'amount':amount,
        'total_amount':total_amount,
        'total_shipping':total_shipping,
      }
    else:
      cart_item = Cart.objects.get(id=cart_id)
      data={
        'quantity':cart_item.quantity,
        'amount':amount,
        'total_amount':total_amount,
        'total_shipping':total_shipping,
      }
    return JsonResponse(data)
    

@login_required
def address(request):
  add=Customer.objects.filter(user=request.user)
  return render(request, 'app/address.html',{'addresses':add,'active':'btn-primary'})

# def change_password(request):
#  return render(request, 'app/changepassword.html')

# In your views.py
def products_page(request,category,data=None):
    if data is None:
        brands = Product.objects.filter(category=category).values('brand').distinct()
        products = Product.objects.filter(category=category)
    else:
        products = Product.objects.filter(category=category, brand=data)
        brands = Product.objects.filter(category=category).values('brand').distinct()  # No need to pass brands if data is not None

    return render(request, 'app/products_page.html', {'products': products, 'brands': brands, 'category': category})

# def login(request):
#  return render(request, 'app/login.html')

# def customerregistration(request):
#  return render(request, 'app/customerregistration.html')

class CustomerRegistrationView(View):
  def get(self,request):
    form=CustomerRegistrationForm()
    return render(request,
                  'app/customerregistration.html',
                  {
                    'form':form
                  })
  
  def post(self,request):
    form=CustomerRegistrationForm(request.POST)
    if form.is_valid():
      messages.success(request, 'User Registered Successfully')
      form.save()
    else:
      messages.error(request,'Unable to Register User')
      
    return render(request,
                  'app/customerregistration.html',
                  {
                    'form':form
                  })
    
@method_decorator(login_required, name='dispatch')
class ProfileView(View):
  def get(self,request):
    form=CustomerProfileForm()
    return render(request,'app/profile.html',{'form':form,'active':'btn-primary'})

  def post(self,request):
    form=CustomerProfileForm(request.POST)
    if form.is_valid():
      usr=request.user
      name=form.cleaned_data['name']
      locality=form.cleaned_data['locality']
      city=form.cleaned_data['city']
      state=form.cleaned_data['state']
      zipcode=form.cleaned_data['zipcode']
      reg=Customer(user=usr,name=name,locality=locality,city=city,state=state,zipcode=zipcode)
      reg.save()
      messages.success(request,"Profile Updated. Check Your Address Book for the Newly Added Address")
    else:
      messages.error(request,"Unable to Update Profile")
    return render(request,'app/profile.html',{'form':form,'active':'btn-primary'})
    
def delete_address(request, address_id):
        try:
            address = Customer.objects.get(id=address_id, user=request.user)
            address.delete()
            messages.success(request, 'Address deleted successfully')
        except Address.DoesNotExist:
            messages.error(request, 'Address not found')

        return redirect('address')

# def delete_cart(request, cart_id):
#         try:
#             product = Cart.objects.get(id=cart_id, user=request.user)
#             product.delete()
#             messages.success(request, 'Product Removed from Cart')
#         except Address.DoesNotExist:
#             messages.error(request, 'Unable to Remove the Product')

#         return redirect('showcart')

@login_required
def checkout(request,type):
  if type=="cart":
    addresses=Customer.objects.filter(user=request.user)
    products=Cart.objects.filter(user=request.user)
    amount=0.0
    shipping_amount=70.0
    total_amount=0.0
    total_shipping=0.0
    cart_product=[p for p in Cart.objects.all() if p.user==request.user]
    # print(cart_product)
    if cart_product:
      for p in cart_product:
        temp_amount=(p.quantity * p.product.discounted_price)
        amount+=temp_amount
        total_amount=amount + shipping_amount
        total_shipping+=shipping_amount
    return render(request,
            'app/checkout.html',
            {
              'addresses':addresses,
              'products': products,
              'total_amount':total_amount,
              'amount':amount,
              'total_shipping':total_shipping
            })
  else:
    addresses=Customer.objects.filter(user=request.user)
    cart_id=type
    product=Cart.objects.get(id=cart_id)
    amount=product.product.discounted_price * product.quantity
    total_shipping=70.0
    total_amount=amount + total_shipping
    return render(request,
          'app/checkout.html',
          {
            'addresses':addresses,
            'cart_item': product,
            'total_amount':total_amount,
            'amount':amount,
            'total_shipping':total_shipping
          })
    
  
  
@login_required
def payment_done(request):
  customer_id=request.POST.get('customer_id')
  customer=Customer.objects.get(id=customer_id)
  cart=Cart.objects.filter(user=request.user)
  for c in cart:
    PlacedOrder(user=request.user,customer=customer,product=c.product,quantity=c.quantity).save()
    c.delete()
  return redirect('orders')
    
@login_required
def buy_now(request):
  if request.user.is_authenticated:
    user=request.user
    product_id=request.POST.get('product_id')
    product=Product.objects.get(id=product_id)
    

    cart_item = Cart.objects.filter(user=user, product=product).first()
    if cart_item:
      pass
        # cart_item.quantity=F('quantity') + 1
        # cart_item.save()
    else:
        Cart(user=user, product=product, quantity=1).save()
        
    cart_product=Cart.objects.get(user=user,product=product)
    amount=cart_product.product.discounted_price
    shipping_amount = 70.0
    total_amount= amount * cart_product.quantity + shipping_amount 
    return render(request, 'app/buynow.html',
                  {'cart_product': cart_product,
                   'total_amount':total_amount,
                   'amount':amount,
                   'total_shipping':shipping_amount
                   })


@login_required
def orders(request):
  placed_orders=PlacedOrder.objects.filter(user=request.user).order_by('-ordered_date')
  return render(request, 'app/orders.html',
                {
                  'placed_orders':placed_orders
                })