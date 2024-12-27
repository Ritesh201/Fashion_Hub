from django.shortcuts import render,redirect,HttpResponseRedirect
from django.contrib.auth.hashers import  check_password,make_password

from django.views import  View
from .models import  Product,Customer,Order,Category,Hisab,Payment

from django import template

register = template.Library()

class Cart(View):
    
    def get(self , request):
        ids = list(request.session.get('cart').keys())
        products = Product.get_products_by_id(ids)
        print(products)
        customer = request.session.get('customer')
        customer=Customer(id=customer)
        return render(request , 'cart.html' , {'products' : products,'customer':customer})
   
class CheckOut(View):
    
    def post(self, request):
        serialNo=0
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        customer = request.session.get('customer')
        cart = request.session.get('cart')
        products = Product.get_products_by_id(list(cart.keys()))
        print(address, phone, customer, cart, products)
        finalAmount=0
        for product in products:
            serialNo=serialNo+1
            finalAmount=finalAmount+product.price*cart.get(str(product.id))
            print(cart.get(str(product.id)))
            order = Order(customer=Customer(id=customer),
                          
                          serial_no=serialNo,
                          product=product,
                          price=product.price,
                          address=address,
                          phone=phone,
                          quantity=cart.get(str(product.id)))

            order.save()
            
        newHisab=Hisab(customer=Customer(id=customer),
                amount=finalAmount,
                order=order)  
        newHisab.save()         
        request.session['cart'] = {}

        return redirect('cart')

class Index(View):

    def post(self , request):
        product = request.POST.get('product')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(product)
            if quantity:
                if remove:
                    if quantity<=1:
                        cart.pop(product)
                    else:
                        cart[product]  = quantity-1
                else:
                    cart[product]  = quantity+1

            else:
                cart[product] = 1
        else:
            cart = {}
            cart[product] = 1

        request.session['cart'] = cart
        print('cart' , request.session['cart'])
        return redirect('homepage')



    def get(self , request):
        return HttpResponseRedirect(f'/store{request.get_full_path()[1:]}')

def store(request):
    cart = request.session.get('cart')
    if not cart:
        request.session['cart'] = {}
    products = None
    categories = Category.get_all_categories()
    categoryID = request.GET.get('category')
    
    
    if categoryID:
        products = Product.get_all_products_by_categoryid(categoryID)
    else:
        products = Product.get_all_products()


    data = {}
    data['products'] = products
    data['categories'] = categories

    print('you are : ', request.session.get('email'))
    return render(request, 'index.html', data)


class Login(View):
    return_url = None
    def get(self , request):
        Login.return_url = request.GET.get('return_url')
        return render(request , 'login.html')

    def post(self , request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        customer = Customer.get_customer_by_email(email)
        print("Customer is",customer)
        error_message = None
        breakpoint()
        if customer:
            flag = check_password(password, customer.password)
            if flag:
                request.session['customer'] = customer.id
                breakpoint()
                if Login.return_url:
                    return HttpResponseRedirect(Login.return_url)
                else:
                    Login.return_url = None
                    return redirect('homepage')
            else:
                breakpoint()
                error_message = 'Email or Password invalid !!'
        else:
            breakpoint()
            error_message = 'Email or Password invalid !!'

        print(email, password)
        return render(request, 'login.html', {'error': error_message})

def logout(request):
    request.session.clear()
    return redirect('login')




class OrderView(View):


    def get(self , request ):
        customer = request.session.get('customer')
        orders = Order.get_orders_by_customer(customer)
        print(orders)
        return render(request , 'orders.html'  , {'orders' : orders})  



class Signup(View):
    def get(self, request):
        return render(request, 'signup.html')

    def post(self, request):
        postData = request.POST
        user_name = postData.get('user_name')
        email = postData.get('email')
        password = postData.get('password')
        re_enter_password = postData.get('re_enter_password')
        phone=postData.get('phone')
        address=postData.get('address')
        pincode=postData.get('pincode')
        # validation
        value = {
            'user_name': user_name,
            'email': email
        }
        error_message = None

        customer = Customer(user_name=user_name,
                            pincode=pincode,
                            address=address,
                            email=email,
                            password=password,
                            phone=phone,
                            
                            re_enter_password=re_enter_password)
        error_message = self.validateCustomer(customer)

        if not error_message:
            customer.register()
            return redirect('homepage')
        else:
            data = {
                'error': error_message,
                'values': value
            }
            return render(request, 'signup.html', data)

    def validateCustomer(self, customer):
        if customer.re_enter_password==customer.password:
            if len(customer.password)>0:
                if len(customer.user_name)>0:

                    error_message = None
                else:
                    error_message="Fill the username"
            else:
                error_message="Fill the password"            
        else:
            error_message="Password does not matches with Re-enter password"    
            
        return error_message 
class hisab(View):
    def get(self, request):
        customer = request.session.get('customer')
        orders = Order.get_orders_by_customer(customer)
        orderAmount=0
        for ord in orders:
            orderAmount=orderAmount+(ord.price*ord.quantity)
        print(orders)
        hisabs=Hisab.get_all_hisab()
        payments=Payment.get_all_payment()
        debitAmount=0
        for hisab in hisabs:
            debitAmount=debitAmount+hisab.amount
        creditAmount=0    
        for payment in payments:
            creditAmount=creditAmount+payment.amount
        balance=debitAmount-creditAmount        
        return render(request , 'hisab.html'  , {'balance':balance,'total_1':debitAmount,'total_2':creditAmount,'hisabs':hisabs,'payments':payments})  
        
      

    