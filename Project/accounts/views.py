from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

# Create your views here.
from .models import *
from .forms import OrderForm, CreateUserForm, CustomerForm, DonationForm
from .filters import OrderFilter, ShopFilter
from .decorators import unauthenticated_user, allowed_users, admin_only

from django.http import JsonResponse
import json
import datetime
from .utils import cookieCart, cartData, guestOrder
from accounts.filters import OrderItemFilter


# @unauthenticated_user
# def registerPage(request):
#     form = CreateUserForm()
#     if request.method == 'POST':
#         form = CreateUserForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             username = form.cleaned_data.get('username')

#             messages.success(request, 'Account was created for ' + username)

#             return redirect('login')

#     context = {'form': form}

#     return render(request, 'accounts/Login/index.html', context)
    # return render(request, 'accounts/register.html', context)


@unauthenticated_user
def registerPage2(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            messages.success(request, 'Account was created for ' + username)

            return redirect('login')

    context = {'values': form}

    # return render(request, 'accounts/Login/signup.html', context)
    return render(request, 'accounts/login2/register.html', context)


# @unauthenticated_user
# def loginPage(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')

#         user = authenticate(request, username=username, password=password)

#         if user is not None:
#             login(request, user)
#             return redirect('home')
#         else:
#             messages.info(request, 'Username OR password is incorrect')

#     context = {}
#     return render(request, 'accounts/Login/index.html', context)
    # return render(request, 'accounts/login.html', context)


@unauthenticated_user
def loginPage2(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username OR password is incorrect')

    context = {}
    return render(request, 'accounts/login2/login.html', context)
    # return render(request, 'accounts/Login/signin.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


def home(request):

    return render(request, 'accounts/home2/index.html')


def comingsoon(request):

    return render(request, 'accounts/ComingSoon/comingsoon.html')

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
    orders = request.user.customer.order_set.all()

    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    print('ORDERS:', orders)

    context = {'orders': orders, 'total_orders': total_orders,
               'delivered': delivered, 'pending': pending}
    return render(request, 'accounts/user.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def accountSettings(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)

    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()

    context = {'form': form}
    return render(request, 'accounts/account_settings.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def products(request):
    products = Product.objects.all()
    # images = Product_image.objects.all()
    # context = {'products':products, 'images':images}
    return render(request, 'accounts/products.html', {'products': products})


def shop(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'accounts/Shop/shop.html', context)


def addtocart(request):
    return render(request, 'accounts/AddToCart/addtocart.html')


# @login_required(login_url='login')
def aboutus(request):
    return render(request, 'accounts/AboutUs/aboutus.html')


# @login_required(login_url='login')
def faq(request):
    return render(request, 'accounts/Faq/faq.html')

def privacy(request):
    return render(request, 'accounts/LP/privacy.html')

def license(request):
    return render(request, 'accounts/LP/license.html')

# @login_required(login_url='login')
def halloffame(request):
    return render(request, 'accounts/Hall Of Fame/halloffame.html')


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def accountdetails(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)

    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()

    context = {'form': form}
    return render(request, 'accounts/AccountDetails/dashb.html', context)


@login_required(login_url='login')
# @allowed_users(allowed_roles=['__all__'])
def orderdetails(request):
    customer = request.user.customer

    orders = customer.order_set.all()
    order_count = orders.count()

    myFilter = OrderFilter(request.GET, queryset=orders)
    myFilter2 = OrderItemFilter(request.GET, queryset=orders)

    orders = myFilter.qs
    orderitem = myFilter2.qs

    context = {'customer': customer, 'orders': orders, 'order_count': order_count,
               'myFilter': myFilter, 'myFilter2': myFilter2, 'orderitem': orderitem}
    return render(request, 'accounts/AccountDetails/order.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customer(request, pk_test):
    customer = Customer.objects.get(id=pk_test)

    orders = customer.order_set.all()
    order_count = orders.count()

    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs

    context = {'customer': customer, 'orders': orders, 'order_count': order_count, 'myFilter': myFilter}
    return render(request, 'accounts/customer.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createOrder(request, pk):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=10)
    customer = Customer.objects.get(id=pk)
    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)
    # form = OrderForm(initial={'customer':customer})
    if request.method == 'POST':
        # print('Printing POST:', request.POST)
        form = OrderForm(request.POST)
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')

    context = {'form': formset}
    return render(request, 'accounts/order_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    print('ORDER:', order)
    if request.method == 'POST':

        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form': form}
    return render(request, 'accounts/order_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == "POST":
        order.delete()
        return redirect('/')

    context = {'item': order}
    return render(request, 'accounts/delete.html', context)


def index(request):
    if request.method == "POST":
        contact = Contact()
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        contact.name = name
        contact.email = email
        contact.phone = phone
        contact.message = message
        contact.save()
        return render(request, 'accounts/ContactUs/thankyou.html')
    return render(request, 'accounts/ContactUs/index.html')


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def donate(request):
    if request.method == "POST":
        donate = Donate()
        fstnm = request.POST.get('fstnm')
        lsnm = request.POST.get('lsnm')

        email = request.POST.get('email')
        phone = request.POST.get('phone')
        books = request.POST.get('books')
        doorno = request.POST.get('doorno')
        landmark = request.POST.get('landmark')
        city = request.POST.get('city')
        state = request.POST.get('state')
        pincode = request.POST.get('pincode')

        donate.fstnm = fstnm
        donate.lsnm = lsnm

        donate.email = email
        donate.phone = phone
        donate.books = books
        donate.doorno = doorno
        donate.landmark = landmark
        donate.city = city
        donate.state = state
        donate.pincode = pincode

        donate.save()
        return render(request, 'accounts/ContactUs/thankyou.html')
    return render(request, 'accounts/Donate/donate.html')


# @login_required(login_url='login')
# @allowed_users(allowed_roles=['customer'])
def store(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    products = Product.objects.all()
    myFilter = ShopFilter(request.GET, queryset=products)
    products = myFilter.qs
    context = {'products': products, 'cartItems': cartItems, 'myFilter': myFilter}
    return render(request, 'accounts/Shop/store.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def productdetail(request, pk_test):
    product = Product.objects.get(id=pk_test)

    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    products12 = Product.objects.all()
    myFilter = ShopFilter(request.GET, queryset=products12)
    products = myFilter.qs
    
    context = {'product': product, 'products12': products12, 'cartItems': cartItems, 'myFilter': myFilter}
    return render(request, 'accounts/Shop/productdetails.html', context)


def cart(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'accounts/Shop/cart.html', context)


def checkout(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'accounts/Shop/checkout.html', context)


def buynow(request, pk_test):
    product = Product.objects.get(id=pk_test)
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'product': product, 'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'accounts/Shop/buynow.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
    else:
        customer, order = guestOrder(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True
        order.status= "Pending"
        
    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
        )
        # FinalOrder.objects.create(
        #     customer=customer,
        #     order=order,
        #     date_ordered=order.date_added,
        #     address=data['shipping']['address'],
        #     city=data['shipping']['city'],
        #     state=data['shipping']['state'],
        #     zipcode=data['shipping']['zipcode'],
        # )

    return JsonResponse('Payment submitted..', safe=False)
