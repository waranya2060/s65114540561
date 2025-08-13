from api.forms import *
from .models import *
from .serializers import *
from django.http import request
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, get_object_or_404
from . import cart 
from django.contrib import messages 
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.utils import timezone
# หน้าแรก
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import  View 
from django.views.generic import DetailView 



class ProfileDetailView(DetailView): 
    # pass 
    model = Users
# class bankTransferlView(DetailView): 
#     # pass
#     model = Payment

def index(request):
    products_list = Product.objects.all().order_by('name')
    product_type=Product_Type.objects.all()
    paginator = Paginator(products_list,8) #จำนวนรายการ/หน้า
    page = request.GET.get('page')
    print(page)
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    print(products)
    return render(request, 'api/index.html',{
         'product_type' :product_type,
         'products':products })


#แสดงสินค้าทั้งหมด
def showProductAll(request):
    product_type=Product_Type.objects.all() # แสดงประเภทช่างบน tap
    product=Product.objects.all()
 
    return render(request,'api/showProductAll.html',{
        'product_type':product_type,
		'product':product,
})

#ประวัติการซื้อ
def order(request):
  
    order = Order.objects.filter(user =request.user, ordered=True).order_by('-id')
    product_type=Product_Type.objects.all()
   
    paginator = Paginator(order,6) #จำนวนรายการ/หน้า
    page = request.GET.get('page')
    try:
        orders = paginator.page(page)
    except PageNotAnInteger:
        orders = paginator.page(1)
    except EmptyPage:
        orders = paginator.page(paginator.num_pages)

    return render(request, 'api/order.html',{
        'orders':orders,
        'product_type':product_type
    })

# หน้ารายการสินค้า
def orderproduct(request,id=0):
    order = Order.objects.filter(user =request.user, ordered=True,id=id)
    product_type=Product_Type.objects.all()
    return render(request, 'api/orderproduct.html',{
        'order':order,
        'product_type':product_type 
    })

# หน้าสินค้าแต่ละหมวดหมู่
def productTypeUser(request,id=0): 
    type=Product_Type.objects.get(pk=id)
    product_type=Product_Type.objects.all()
    product=Product.objects.filter(product_type=id).order_by('id')
    print(type)
    return render(request,'api/productTypeUser.html',{
        'product':product,
        'type' :type,
        'product_type':product_type,
        })

    # รายละเอียดสินค้า 
def productDetail(request,id):
    # if request.user.is_anonymous:
    #     return redirect('/login')
    # else: 
    #     users= Users.objects.get(username=request.user.username)
   
    # except: pass
   
    product = Product.objects.get(pk=id)
    # item_count = cart.item_count(request) #ตัวเลขบนตะกร้าสินค้า
    product_type=Product_Type.objects.all()
    return render(request, 'api/productDetail.html', {
                                            'product': product,
                                            # 'form': form,
                                            # 'cart_item_count': item_count,
                                            'product_type':product_type,
                                            # 'users':users
                                         
                                            })


def home(request):
    all_products = Product.objects.all()
    return render(request, "api/home.html", {
                                    'all_products': all_products,
                                 })
# @login_required(login_url='/login')                        
class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            product_type=Product_Type.objects.all()
            order = Order.objects.get(user=self.request.user, ordered=False)

            context = {
                'object': order,
                'product_type':product_type

            }
            return render(self.request, 'api/order_summary.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "คุณไม่มีสินค้าในตะกร้าสินค้า")
            return redirect("/")

@login_required(login_url='/login') 
def add_to_cart(request, id):
    product = get_object_or_404(Product, id=id)
    order_product, created = OrderItem.objects.get_or_create(
        product=product,user=request.user, ordered=False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    # if there is a order
    # หากมีการสั่งซื้อ
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order ==(order ache,for same-orderitem
        # ตรวจสอบว่ารายการสั่งซื้ออยู่ในคำสั่งซื้อหรือไม่ == (สั่งซื้อสำหรับรายการสั่งซื้อเดียวกัน
        if order.products.filter(product__id=product.id).exists():
            order_product.quantity += 1
            if order_product.quantity  <= product.quantity:
                # order_product.price=product.price 
                # order_product.price=order_product.get_total_product_price()  
                messages.info(request, "เพิ่มสินค้าเข้าตะกร้าสำเร็จ")
                order_product.save()  
            else:
                messages.warning(request, "สินค้าในสต๊อกไม่พอ")
            return redirect("order-summary")
        else:
            # ==(order ache, different-orderitem ache)
            # สั่งซื้อสั่งซื้อที่แตกต่างกัน
            # order_product.price= order_product.get_total_product_price()  
            # order_product.save()
            if order_product.quantity  <= product.quantity and product.quantity >0:
                order.products.add(order_product)
            
                messages.info(request, "เพิ่มสินค้าเข้าตะกร้าสำเร็จ")
            else:
                messages.warning(request, "สินค้าในสต๊อกไม่พอ")
            return redirect("order-summary")
    # if there is no ordequantityr..first time order and first item
    # หากไม่มีคำสั่งซื้อ.. สั่งครั้งแรกและสินค้าชิ้นแรก
    else:
        if order_product.quantity  <= product.quantity and product.quantity >0:
            # ordered_date = timezone.now()
            order = Order.objects.create(user=request.user, )
            order.products.add(order_product)

            messages.info(request, "เพิ่มสินค้าเข้าตะกร้าสำเร็จ")
        else:
             messages.warning(request, "สินค้าในสต๊อกไม่พอ")
        return redirect("order-summary")

def remove_from_cart(request, id):
    product = get_object_or_404(Product, id=id)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.products.filter(product__id=product.id).exists():
            order_product = OrderItem.objects.filter(
                product=product,
                user=request.user,
                ordered=False
            )[0]
            order_product.quantity = 1
            order_product.save()
            order.products.remove(order_product)
            messages.info(request, "ลบสินค้าออกจากตระสินค้าสำเร็จ")
            return redirect("order-summary")
        else:
            messages.info(request, "สินค้านี้ไม่ได้อยู่ในรถเข็นของคุณ")
            return redirect("product-detail", id=id)
    else:
        messages.info(request, "คุณไม่มีคำสั่งซื้อที่ใช้งานอยู่")
        return redirect("product-detail", id=id)


def remove_single_item_from_cart(request, id):
    product = get_object_or_404(Product, id=id)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.products.filter(product__id=product.id).exists():
            order_product = OrderItem.objects.filter(
                product=product,
                user=request.user,
                ordered=False
            )[0]
            if order_product.quantity > 1:
                order_product.quantity -= 1
                messages.info(request, "ลดจำนวนสินค้าสำเร็จ")
                order_product.save()
            else:
                # order.products.remove(order_product)ห
                messages.warning(request, "ไม่สามารถลดสินค้าได้ ต้องมีสินค้าชนิดนี้อย่างน้อย1 รายการ")
            return redirect("order-summary")
        else:
            messages.info(request, "สินค้านี้ไม่ได้อยู่ในรถเข็นของคุณ")
            return redirect("product-detail", id=id)

    else:
        messages.info(request, "คุณไม่มีคำสั่งซื้อที่ใช้งานอยู่")
        return redirect("product-detail", id=id)


class CheckoutView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        form = CheckoutForm()
        product_type=Product_Type.objects.all()
        order = Order.objects.filter(user=self.request.user, ordered=False)
        context = {
            'order': order,
            'form': form,
            'product_type':product_type,
            'delivery_options': Delivery_Options.objects.all(),          
   }
        return render(self.request, 'api/checkout-page.html', context)

    def post(self, *args, **kwargs):
         
        form = CheckoutForm(self.request.POST or None)
        if form.is_valid():
            order = Order.objects.get(user=self.request.user, ordered=False)           
            order.address = self.request.POST['address']
            order.delivery_options =Delivery_Options.objects.get(pk=self.request.POST['delivery_options'])
            order.save()
         
            payment_option = form.cleaned_data.get('payment_option')
            if payment_option == 'โอนผ่านบัญชีธนาคาร':
                order.payment_option = payment_option
                order.save()             
                return redirect('payment', payment_option='โอนผ่านบัญชีธนาคาร')
        
            elif payment_option == 'เงินสด':
                order_products = order.products.all()
                order_products.update(ordered=True)
                order.ordered_date = timezone.now()
 
                order.ordered = True
                order.payment_option = payment_option
               
                for order_product in order_products:
                    order_product.product.quantity -=order_product.quantity
                    order_product.product.save()
                
                order.save()
                messages.success(self.request, "สั่งซื้อสินค้าสำเร็จ!")
                return redirect('/order', )
            
            # else:
            #     messages.warning(
            #         self.request, "ตัวเลือกการชำระเงินไม่ถูกต้อง")
            #     return redirect('check-out')  

class PaymentView(View):
    def get(self, *args, **kwargs):
        bankTransfer = BankTransfer.objects.all()
        product_type=Product_Type.objects.all()
        order = Order.objects.get(user=self.request.user, ordered=False)
        # if order.user:           
        context = {
                'order': order,
                'bankTransfer' :bankTransfer,
                'product_type':product_type
            }
        return render(self.request, 'api/payment.html', context)
    def post(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        payment_option = Payment()
        # payment_option.time = self.request.POST['time']
        # payment_option.ppp = self.request.POST['ppp']
        payment_option.img = self.request.FILES['img']
        payment_option.user = self.request.user
        payment_option.amount = order.get_total()
        payment_option.order= order
        payment_option.save()

        order_products = order.products.all()
        order_products.update(ordered=True)    
        # assign the payment
        order.ordered_date = timezone.now()
 
        order.ordered = True
        order.save()
        for order_product in order_products:
            order_product.product.quantity -=order_product.quantity
            order_product.product.save()
        messages.success(self.request, "สั่งซื้อสินค้าสำเร็จ!")
        return redirect("/order")
    

# Searchสินค้า
def search (request): 
    q=request.GET['q']
    data=Product.objects.filter(name__icontains=q).order_by('id')
    product_type=Product_Type.objects.all()
    return render(request,'api/search.html',{
    'data':data,
    'product_type':product_type
    })

#หน้าโปรไฟล์
def profile(request):   
    users = Users.objects.get(username=request.user.username)
    product_type=Product_Type.objects.all()
    return render(request, 'api/profile.html', {
        'users': users,
        'product_type':product_type,
    })

def editprofile(request, id=0):
    users = Users.objects.get(username=request.user.username)
    product_type=Product_Type.objects.all()
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=users)
        if form.is_valid():
            form.save()
            messages.info(request, "แก้ไขข้อมูลผู้ใช้สำเร็จ")
            return redirect('/profile')
        else:
            print("==== form.errors ====")
            print(form.errors)
    else:
        form = EditProfileForm(users)  

    return render(request, 'api/editprofile.html' ,{ 
        'form': form,
        'users':users,
        'product_type':product_type,
    })

def logout(req):
    auth_logout(req)
    return redirect('/')

def login(request):
    if request.method == 'POST':
        users = authenticate(username=request.POST['username'], password=request.POST['password'])
        if users is not None:
            print(users)
            auth_login(request, users)
            messages.info(request, "เข้าสู่ระบบสำเร็จ")
            if request.user.is_superuser :

                return redirect('/store')
            else:
                  return redirect('/')
        else: 
            messages.warning(request, "เข้าสู่ระบบไม่สำเร็จ")
    else:
        print('ยังไม่ได้กรอก login/password')
    return render(request, 'api/login.html')

def register(request):
    print('register()')
    form = UsersForm()
    print(request)
    if request.method == 'POST':
        form = UsersForm(request.POST, request.FILES)
        # print("request.POST")
        # print(request.POST)
        if form.is_valid():
            # print('form valid')
            form.instance.password = make_password(request.POST['password'])
            form.save()
            messages.info(request, "สมัครสมาชิกสำเร็จ")
            return redirect('/login')
        else:            
            print("==== form.errors ====")
            print(form.errors)
            # messages.warning(request, "เข้าสู่ระบบไม่สำเร็จ " )
    return render(request, 'api/register.html', { 
        'form': form,
       
        })

# หน้ารวมช่าง
def mechanicUser(request):
    mechanic= Mechanic.objects.all()
    product_type=Product_Type.objects.all()
    paginator = Paginator(mechanic,8) #จำนวนรายการ/หน้า
    page = request.GET.get('page')
    try:
        mechanics = paginator.page(page)
    except PageNotAnInteger:
        mechanics = paginator.page(1)
    except EmptyPage:
        mechanics = paginator.page(paginator.num_pages)
   
    return render(request, 'api/mechanicUser.html',{
        'mechanics' :mechanics ,
        'product_type':product_type,
    })

# หน้ารายละเอียดช่าง
def mechanicDetailUser(request,id=0):
    product_type=Product_Type.objects.all()
    mechanic= Mechanic.objects.get(pk=id)
    return render(request, 'api/mechanicDetailUser.html',{
        'mechanic' :mechanic,
        'product_type':product_type,
    })

def base2(req):
    return render(req, 'api/base2.html')

def register1(req):
    return render(req, 'api/register1.html')

# หน้าข้อมูลร้าน
def storeUser(request,id=0):
    product_type=Product_Type.objects.all()
    store = Store.objects.get(id=1)
    return render(request, 'api/storeUser.html', {
        'store' :store,
        'product_type' :product_type,
    })
# หมวดหมู่สินค้าบนแทป
# def producttype(req):
#     producttype = Product_Type.objects.get()
#     return render(req, 'api/base1.html', {
#         'producttype' :producttype
#     })

##############################Admin#########################################################################

# ข้อมูลร้าน
def store(req,id=0):
    
    store = Store.objects.get(id=1) 
    # users = Users.objects.get(username=req.user.username)
    return render(req, 'api/store.html', {
        'store': store,
       
    })

# แก้ไขข้อมูลร้าน
def editstore(request,id):
    store = Store.objects.get(pk=id)
    if request.method == 'POST':
        form = StoreForm(request.POST, request.FILES, instance=store)
        if form.is_valid():
            form.save()
            messages.info(request, "แก้ไขข้อมูลร้านสำเร็จ")
            return redirect('/store')
        else:
            print("==== form.errors ====")
            print(form.errors)
    else:
        form = StoreForm(store)
    return render(request, 'api/editstore.html' ,{ 
        'form': form,
        'store': store,
    }) 

# เพิ่มหมวดหมู่สินค้า
def addproductType(request):
    product_type = Product_Type.objects.all()
    if request.method == 'POST':
        form = Product_TypeForm(request.POST ,request.FILES)
        if form.is_valid():
            messages.info(request, "เพิ่มหมวดหมู่สินค้าสำเร็จ")
            form.save()
            return redirect('/addproductType')
    else:
        form = Product_TypeForm()
    return render(request, 'api/addproductType.html',
                  {
                      'form': form,
                      'product_type':product_type

                  }) 

def editproductType(request, id=0):
    product_type = Product_Type.objects.get(pk=id)
    if request.method == 'POST':
        form = Product_TypeForm(request.POST, request.FILES, instance=product_type)
        if form.is_valid():
            form.save()
            messages.success(request, 'แก้ไขหมวดหมู่สินค้าสำเร็จ')
            return redirect('/addproductType')
        else:
            print("==== form.errors ====")
            print(form.errors)
    else:
        form = Product_Type(product_type)
       
    return render(request, 'api/editproductType.html' ,{ 
        'form': form,
        'product_type': product_type,
    })

@login_required(login_url='/login') 
def deleteproductType(req, id=0):
    product_types = Product_Type.objects.get(pk=id)
    product_types.delete()
    messages.success(req, "ลบหมวดหมู่สินค้าสำเร็จ")
    return HttpResponseRedirect(req.META.get('HTTP_REFERER'))

@login_required(login_url='/login')    
def deleteproduct(req, id=0):
    product = Product.objects.get(pk=id)
    product.delete()
    messages.success(req, "ลบสินค้าสำเร็จ")
    return HttpResponseRedirect(req.META.get('HTTP_REFERER'))

# เพิ่มสินค้า
def addproduct(request):
    if request.method == 'POST':
        form = ProductForm(request.POST ,request.FILES)
        if form.is_valid():
            messages.info(request, "เพิ่มสินค้าสำเร็จ")
            form.save()
            return redirect('/product')
    else:
        form = ProductForm()
    return render(request, 'api/addproduct.html',
                  {
                      'form': form,
                      'product_types': Product_Type.objects.all(),
                  }) 
# แก้ไขสินค้า
def editproduct(request, id=0):
    product = Product.objects.get(pk=id)
    product_types = Product_Type.objects.all()
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'แก้ไขสินค้าสำเร็จ')
            return redirect('/product')
        else:
            print("==== form.errors ====")
            print(form.errors)
    else:
        form = ProductForm(product)
       
    return render(request, 'api/editproduct.html' ,{ 
        'form': form,
        'product': product,
        'product_types': product_types,
        # 'product_statuss': product_statuss,
    })

# ลบสินค้า


# แสดงสินค้า //
def product(request):
    products_list = Product.objects.all()
    paginator = Paginator(products_list,4) #1 หน้าแสดง 5รายการ
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        products = paginator.page(1)
    except EmptyPage:
        # # If page is out of range (e.g. 9999), deliver last page of results.
        products = paginator.page(paginator.num_pages)
    return render(request, 'api/product.html', {'products': products})


# หน้าคลังสินค้า 
# def stock(request):
#     products = Product.objects.all()
#     # comment = get_object_or_404(Comment, pk=comment_id)
#     # users = get_object_or_404(Users,username=request.user.username)
#     return render(request, 'api/stock.html', {'products': products,
#     # 'users':users
#     })

# def issue_item(request, pk):
#     product = Product.objects.get(id = pk)
#     form = SaleForm(request.POST)  
      
#     if request.method == 'POST':     
#         if form.is_valid():
#             new_sale = form.save(commit=False)
#             new_sale.product = product
#             # # new_sale.unit_price = product.unit_price   
#             # new_sale.save()
#             #To keep track of the stock remaining after sales
#             # product =Product()
#             quantity =int(request.POST['quantity'])
#             product.quantity -=  quantity
#             if product.quantity >= 0:
#                 messages.success(request, "Issued success. " )
#                 product.save()
#             else:
#                 messages.warning(request, "สินค้าในสต๊อกไม่พอ")
#             # product.save()

#             print(product.name) #ชื่อ
#             print(request.POST['quantity']) #จำนวน
#             # print(product.total_quantity)

#             return redirect('/stock') 

#     return render (request, 'api/issue_item.html',
#      {
#     'form': form,
#     })

#เพิ่มจำนวนสินค้าในสต๊อก
# def add_to_stock(request, pk):
#     product = Product.objects.get(id = pk)
#     form = AddStockForm(request.POST)  #จำนวนสินค้าในสต๊อก
#     if request.method == 'POST':
#         if form.is_valid():
#             added_quantity = int(request.POST['received_quantity'])
#             product.quantity += added_quantity
#             product.save()
#             #To add to the remaining stock quantity is reducing
#             print(added_quantity)
#             print (product.quantity)
#             return redirect('/product')
#     return render (request, 'api/add_to_stock.html', {'form': form})

#ข้อมูลช่าง
def mechanic(request):
    mechanic = Mechanic.objects.all()
    paginator = Paginator(mechanic,8) #จำนวนรายการ/หน้า
    page = request.GET.get('page')
    try:
        mechanics = paginator.page(page)
    except PageNotAnInteger:
        mechanics = paginator.page(1)
    except EmptyPage:
        mechanics = paginator.page(paginator.num_pages)
   
    return render(request, 'api/mechanic.html', {
        'mechanics': mechanics,
      })

def addmechanic(request):
    # users = Users.objects.get(username=request.user.username)
    if request.method == 'POST':
        form = MechanicForm(request.POST ,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/mechanic')
    else:
        form = MechanicForm()
    return render(request, 'api/addmechanic.html',
                  {
                      'form': form,
                      'mechanic_type': Mechanic_Type.objects.all(),
                    #   'product_statuss': Product_Status.objects.all(),
                    #   'users':users

                  }) 
def editmechanic(request, id=0):
    mechanic = Mechanic.objects.get(pk=id)
    mechanic_types = Mechanic_Type.objects.all()
    if request.method == 'POST':
        form = MechanicForm(request.POST, request.FILES, instance=mechanic)
        if form.is_valid():
            messages.success(request, 'แก้ไขข้อมูลช่างสำเร็จ')
            form.save()
            return redirect('/mechanic')
        else:
            print("==== form.errors ====")
            print(form.errors)
    else:
        form = MechanicForm(mechanic)
    return render(request, 'api/editmechanic.html' ,{ 
        'form': form,
        'mechanic': mechanic,
        'mechanic_types' : mechanic_types,
    })
@login_required(login_url='/login')    
def deletemechanic(req, id=0):
    mechanic = Mechanic.objects.get(pk=id)
    mechanic.delete()
    messages.success(req, "ลบข้อมูลช่างสำเร็จ")
    return HttpResponseRedirect(req.META.get('HTTP_REFERER'))

def addmechanicType(request):
    # users = Users.objects.get(username=request.user.username)
    mechanic_type = Mechanic_Type.objects.all()
    if request.method == 'POST':
        form = Mechanic_TypeForm(request.POST ,request.FILES)
        if form.is_valid():
            messages.info(request, "เพิ่มประเภทช่างสำเร็จ")
            form.save()
            return redirect('/addmechanicType')
    else:
        form = Mechanic_TypeForm()
    return render(request, 'api/addmechanicType.html',
                  {
                      'form': form,
                      
                    #   'users':users,
                      'mechanic_type':mechanic_type

                  }) 

def editmechanicType(request, id=0):
    mechanic_type = Mechanic_Type.objects.get(pk=id)
    # users = Users.objects.get(username=request.user.username)
    if request.method == 'POST':
        form = Mechanic_TypeForm(request.POST, request.FILES, instance=mechanic_type)
        if form.is_valid():
            form.save()
            messages.success(request, 'แก้ไขประเภทช่างสำเร็จ')
            return redirect('/addmechanicType')
        else:
            print("==== form.errors ====")
            print(form.errors)
    else:
        form = Mechanic_TypeForm(mechanic_type)
       
    return render(request, 'api/editmechanicType.html' ,{ 
        'form': form,
        'mechanic_type': mechanic_type,
        # 'users':users
    })
@login_required(login_url='/login')    
def deletemechanicType(req, id=0):
    mechanic_types = Mechanic_Type.objects.get(pk=id)
    mechanic_types.delete()
    messages.success(req, "ลบประเภทช่างสำเร็จ")
    return HttpResponseRedirect(req.META.get('HTTP_REFERER'))

# หน้ารายการสั่งซื้อทั้งหมด
def orderAll(req,id=0):
    order = Order.objects.filter(ordered=True,).order_by('-ordered_date')
    # payment = Payment.objects.filter(order=id)
    # print(order.id)
    paginator = Paginator(order,8) #จำนวนรายการ/หน้า
    page = req.GET.get('page')
    try:
        orders = paginator.page(page)
    except PageNotAnInteger:
        orders = paginator.page(1)
    except EmptyPage:
        orders = paginator.page(paginator.num_pages)
    return render(req, 'api/orderAll.html',{
        'orders':orders,
        # 'payment':payment,
        'money_status': Money_Status.objects.all()
    })
def payment_detail(request,id=0):
    payment = Payment.objects.filter(order=id)
    return render(request, 'api/payment_detail.html',{
        'payment':payment,
       
    })
    #แก้ไขสถานะการชำระเงิน
def editOrder(request, id=0):
    order = Order.objects.get(pk=id)
    money_statuss = Money_Status.objects.all()
    if request.method == 'POST':
        form = EditOrderForm(request.POST, request.FILES, instance=order)
        if form.is_valid():
            messages.success(request, 'แก้ไขสถานะการชำระเงินสำเร็จ')
            form.save()
            return redirect('/orderAll')
        else:
            print("==== form.errors ====")
            print(form.errors)
    else:
        form = EditOrderForm(order)
    return render(request, 'api/editOrder.html' ,{ 
        'form': form,
        'order': order,
        'money_statuss' : money_statuss,
    })

# หน้ารายการสินค้า
def orderproductAll(req,id):
    order = Order.objects.filter( ordered=True,id=id)
    return render(req, 'api/orderproductAll.html',{
        'order':order
    })

# เพิ่มสินค้า
def addbank(request):
    if request.method == 'POST':
        form = BankTransferForm(request.POST ,request.FILES)
        if form.is_valid():
            messages.info(request, "เพิ่มข้อมูลบัญชีธนาคารสำเร็จ")
            form.save()
            return redirect('/bank')
    else:
        form = BankTransferForm()
    return render(request, 'api/addbank.html',
                  {
                      'form': form,
                    #   'product_types': Product_Type.objects.all(),
                  }) 
def bank(request):
    bankTransfer = BankTransfer.objects.all()
    return render(request, 'api/bank.html', {
        'bankTransfer': bankTransfer})

@login_required(login_url='/login')    
def deletebank(req, id=0):
    bankTransfer = BankTransfer.objects.get(pk=id)
    bankTransfer.delete()
    messages.success(req, "ลบข้อมูลบัญชีธนาคารสำเร็จ")
    return HttpResponseRedirect(req.META.get('HTTP_REFERER'))

def editbank(request, id=0):
    bankTransfer = BankTransfer.objects.get(pk=id)
    if request.method == 'POST':
        form = BankTransferForm(request.POST, request.FILES, instance=bankTransfer)
        if form.is_valid():
            form.save()
            messages.success(request, 'แก้ไขข้อมูลบัญชีธนาคารสำเร็จ')
            return redirect('/bank')
        else:
            print("==== form.errors ====")
            print(form.errors)
    else:
        form = BankTransferForm(bankTransfer)
    return render(request, 'api/editbank.html' ,{ 
        'form': form,
        'bankTransfer': bankTransfer,
    })


# class Mechanic_TypeViewSet(viewsets.ModelViewSet):
#     queryset = Mechanic_Type.objects.all()
#     serializer_class = Mechanic_TypeSerializer

# class MechanicViewSet(viewsets.ModelViewSet):
#     queryset = Mechanic.objects.all()
#     serializer_class = MechanicSerializer

# class StoreViewSet(viewsets.ModelViewSet):
#     queryset = Store.objects.all()
#     serializer_class = StoreSerializer

# class Product_TypeViewSet(viewsets.ModelViewSet):
#     queryset = Product_Type.objects.all()
#     serializer_class = Product_TypeSerializer

# class Product_StatusViewSet(viewsets.ModelViewSet):
#     queryset = Product_Status.objects.all()
#     serializer_class = Product_StatusSerializer

# class ProductViewSet(viewsets.ModelViewSet):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer

# class Money_StatusViewSet(viewsets.ModelViewSet):
#     queryset = Money_Status.objects.all()
#     serializer_class = Money_StatusSerializer

# class Delivery_OptionsViewSet(viewsets.ModelViewSet):
#     queryset = Delivery_Options.objects.all()
#     serializer_class = Delivery_OptionsSerializer


# class OrderViewSet(viewsets.ModelViewSet):
#     queryset = Order.objects.all()
#     serializer_class = OrderSerializer



# router = routers.DefaultRouter()

# router.register(r'Mechanic_Type', Mechanic_TypeViewSet)
# router.register(r'Mechanic', MechanicViewSet)
# router.register(r'Store', StoreViewSet)
# router.register(r'Product_Type', Product_TypeViewSet)
# router.register(r'Product_Status', Product_StatusViewSet)
# router.register(r'Product', ProductViewSet)
# router.register(r'Money_Status', Money_StatusViewSet)
# router.register(r'Delivery_Options', Delivery_OptionsViewSet)
# # router.register(r'Payment_Options', Payment_OptionsViewSet)
# # router.register(r'Order', OrderViewSet)



