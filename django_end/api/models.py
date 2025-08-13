
from django.contrib.admin.sites import DefaultAdminSite
from django.db import models
from django.db.models.deletion import CASCADE
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.shortcuts import reverse

class Users(AbstractUser): 
    first_name = models.CharField(max_length=100,default=' ',verbose_name = 'ชื่อ')
    last_name = models.CharField(max_length=100,default=' ',verbose_name = 'นามสกุล')
    email = models.CharField(max_length=50,default=' ',verbose_name = 'อีเมล')
    phone = models.CharField(max_length=100,default=' ',verbose_name = 'เบอร์โทรศัพท์')
    avatar = models.ImageField(upload_to='images/users/', default='images/users/no-img.png' ,verbose_name = 'รูปโปรไฟล์')
    password = models.CharField(max_length=500,default=' ')
    def __str__(self):
        return f'{self.username} '

    # def name(self):
    #     return self.username    
   
    # class Meta:
    #     verbose_name = 'แอดมิน2' 

class Mechanic_Type (models.Model):
    # mechanicCategory_id = models.AutoField(primary_key=True)
    mechanic_type= models.CharField(max_length=100,default=' ',verbose_name = 'ประเภทช่าง')
    def __str__(self):
        return f'{self.mechanic_type} '
    class Meta:
        verbose_name = 'ประเภทช่าง'

class Mechanic(models.Model): 
    mechanic_fname =models.CharField(max_length=100,default=' ',verbose_name = 'ชื่อ')
    mechanic_lname =models.CharField(max_length=100,default=' ',verbose_name = 'นามสกุล')
    mechanic_phone =models.CharField(max_length=100,default=' ',verbose_name = 'เบอร์โทรศัพท์')
    mechanic_email =models.CharField(max_length=100,default=' ',verbose_name = 'อีเมล')
    avatar = models.ImageField(upload_to='images/mechanic/', default='images/mechanic/no-img.png', verbose_name = 'รูปโปรไฟล์')
    mechanic_img = models.ImageField(upload_to='images/mechanic/', default='images/mechanic/no-img.png', verbose_name =  'รูปงานช่าง')
    mechanic_detail =models.TextField(max_length=1000,default=' ',verbose_name = 'รายละเอียดงานช่าง')
    mechanic_type= models.ForeignKey(Mechanic_Type,on_delete=models.CASCADE) 
 
    def __str__(self):
        return f'{self.mechanic_email}  '
    class Meta:
        verbose_name = 'ช่าง'

class Store (models.Model):
    store_name = models.CharField(max_length=100,default='- ',verbose_name = 'ชื่อร้าน',null=True)
    store_img = models.ImageField(upload_to='images/store/', default='images/store/no-img.png', verbose_name = 'รูปร้าน',null=True)
    store_phone = models.CharField(max_length=100,default=' -',verbose_name = 'เบอร์โทรศัพท์ร้าน',null=True)
    store_address = models.CharField(max_length=100,default=' -',verbose_name = 'ที่อยู่ร้าน',null=True)
    store_detail= models.CharField(max_length=100,default=' -',verbose_name = 'อื่น ๆ',null=True)
  
    def __str__(self):
        return f'{self.store_name} '
    class Meta:
        verbose_name = 'ข้อมูลร้าน'



# หมวดหมู่สินค้า
class Product_Type (models.Model):
    product_type = models.CharField(max_length=100,default=' ',verbose_name = 'หมวดหมู่สินค้า')
    def __str__(self):
        return f'{self.product_type} '
    class Meta:
        verbose_name = 'หมวดหมู่สินค้า'

# สถานะสินค้า
# class Product_Status (models.Model):
#     product_status= models.CharField(max_length=100,default=' ',verbose_name = 'สถานะสินค้า') #สถานะสินค้า หมดแล้ว /ยังคงเหลือ
#     def __str__(self):
#         return f'{self.product_status} '
#     class Meta:
#         verbose_name = 'สถานะสินค้า'

#สินค้า
class Product(models.Model): 
    name = models.CharField(max_length=1000,default=' ',verbose_name = 'ชื่อสินค้า')
    price = models.DecimalField(max_digits=7, decimal_places=2)
    product_detail = models.TextField(max_length=10000,default=' ',verbose_name = 'รายละเอียดสินค้า')
    product_img = models.ImageField(upload_to='images/product/', default='images/product/no-img.png' ,verbose_name = 'รูปสินค้า')
    product_type = models.ForeignKey(Product_Type,on_delete=models.CASCADE,verbose_name = 'หมวดหมู่สินค้า') #หมวดหมู่สินค้า
    # product_status =  models.ForeignKey(Product_Status,on_delete=models.CASCADE,verbose_name = 'สถานะสินค้า', default=1,null=True,)  #สถานะสินค้า
    quantity = models.IntegerField(verbose_name = 'จำนวนสินค้า') #จำนวนสินค้า
    # received_quantity = models.IntegerField(default = 0, null = True, blank = True) #ตัวแปรเพิ่มจำนวนสินค้าในสต๊อก
    # quantityS = models.IntegerField(default = 0, null = True, blank = True)
  
    def __str__(self):
        return f'{self.name}  '
    class Meta:
        verbose_name = 'สินค้า'

#สถานะการชำระเงิน
class Money_Status(models.Model):
    money_status =  models.CharField(max_length=100,default=' ',verbose_name = 'สถานะการชำระเงิน') 
    def __str__(self):
        return f'{self.money_status} '
    class Meta:
        verbose_name = 'สถานะการชำระเงิน'
   

#ตัวเลือกการจัดส่ง

class Delivery_Options (models.Model):
    delivery_options =  models.CharField(max_length=1000,verbose_name = 'ตัวเลือกการจัดส่ง') 
    def __str__(self):
        return f'{self.delivery_options} '
    class Meta:
        verbose_name = 'ตัวเลือกการจัดส่ง'

class OrderItem(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    # price =  models.DecimalField(max_digits=7, decimal_places=2,default=1,null=True,)
    quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False)  

    def __str__(self):
        return f" {self.id }  // {self.quantity} of {self.product.name}"
        # return f"  {self.quantity} {self.product.quantity} "

    def get_total_product_price(self):
        return self.quantity * self.product.price

    def get_quantity(self):
        return self.product.quantity - self.quantity


    # def get_total_discount_product_price(self):
    #     return self.quantity * self.product.discount_price

    def get_amount_saved(self):
        return self.get_total_product_price() - self.get_total_discount_product_price()

    # def get_final_price(self):
    #     if self.product.discount_price:
    #         return self.get_total_discount_product_price()
    #     return self.get_total_product_price()


class Order(models.Model):
    
    # def get_final_price(self):
    #     if self.product.discount_price:
    #         return self.get_total_discount_product_pri# payment = models.ForeignKey(Payment, on_delete=models.CASCADE,null=True,blank=True)

    user = models.ForeignKey(Users, on_delete=models.CASCADE, null=True)
    money_status = models.ForeignKey(Money_Status,on_delete=models.CASCADE,default=1,null=True,verbose_name = 'สถานะการชำระเงิน') #สถานะการชำระเงิน
    delivery_options = models.ForeignKey(Delivery_Options,verbose_name = 'ตัวเลือกการจัดส่ง',on_delete=models.SET_NULL, blank=True, null=True)
    # payment_option = models.CharField(max_length=191)
    PAYMENT_CHOICES = (
    ('โอนผ่านบัญชีธนาคาร', 'โอนผ่านบัญชีธนาคาร'), 
    ('เงินสด', 'เงินสด')
)
    payment_option = models.CharField(max_length=100,choices=PAYMENT_CHOICES)
    address = models.CharField(max_length=191)
    # phone = models.CharField(max_length=100)
    ordered_date = models.DateTimeField(auto_now_add=True)
    # date = models.DateTimeField(auto_now_add=True)
    products = models.ManyToManyField(OrderItem)
    # pp = models.ForeignKey(OrderItem, on_delete=models.CASCADE, null=True)
    ordered = models.BooleanField(default=False,null=True)
    # quantity = models.IntegerField(default=1)
  
    def __str__(self):
        return f" {self.user.username}  {self.id} "

    def get_total(self):
        total = 0
        for order_product in self.products.all():
            total += order_product.get_total_product_price()
        # if self.coupon:
        #     total -= self.coupon.amount
        return total
    def as_bootstrap_status(self):
        if self.money_status.money_status =='ชำระเงินแล้ว':
            return 'success'
        elif self.money_status.money_status == 'ยังไม่ชำระ' :
            return 'danger'
 


class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE ,blank=True, null=True)

    # ppp = models.CharField(max_length=100 ,null=True)
    # stripe_charge_id = models.CharField(max_length=50)
    img = models.ImageField(upload_to='images/payment/', default='images/payment/no-img.png', verbose_name = 'รูป')
    # user = models.ForeignKey(
    #     Users, on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    # datetime = models.DateTimeField(null=True, blank=True)
    # timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return f" {self.id} {self.user.username} " 

    # def get_order(self):
    #     return self.order ==  self.order.id


class BankTransfer(models.Model):
    accountNo = models.CharField(max_length=100 ,null=True,verbose_name = 'เลขบัญชีธนาคาร')
    accountName = models.CharField(max_length=100 ,null=True,verbose_name = 'ชื่อบัญชีธนาคาร')
    bankName = models.CharField(max_length=100 ,null=True,verbose_name = 'ชื่อธนาคาร')
    qrcode = models.ImageField(upload_to='images/bankTransfer/', default='images/bankTransfer/no-img.png', verbose_name = 'qrcode',null=True)
    def __str__(self):
        return f'{self.bankName} '
    class Meta:
        verbose_name = 'ข้อมูลบัญชีธนาคาร'

# class Sale(models.Model):
#     # item = models.ForeignKey(Product, on_delete = models.CASCADE)
#     products = models.ManyToManyField(OrderItem)
#     quantity = models.IntegerField(default = 0, null = True, blank = True)








# #รายการสินค้า
# class LineItem(models.Model):
#     user = models.ForeignKey(Users,on_delete=models.CASCADE , null=True)
#     order = models.ForeignKey(Order, on_delete=models.CASCADE)
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     price = models.DecimalField(max_digits=7, decimal_places=2)
#     quantity = models.IntegerField()
#     date_added = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return "{}:{}".format(self.product.name, self.id)

#     def cost(self):
#         return self.price * self.quantity







