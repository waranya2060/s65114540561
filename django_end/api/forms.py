from django import forms
from django.forms.widgets import DateInput
from .models import *
  

class BankTransferForm(forms.ModelForm):
    class Meta:
        model = BankTransfer
        fields = '__all__'
        # fields = [  'name','price', 'product_detail', 'product_img','product_type','quantity' ]


PAYMENT_CHOICES = (
    ('โอนผ่านบัญชีธนาคาร', 'โอนผ่านบัญชีธนาคาร'), 
    ('เงินสด', 'เงินสด')
)
# class CartForm(forms.Form):
#     quantity = forms.IntegerField(initial='1')
#     product_id = forms.IntegerField(widget=forms.HiddenInput)

#     def __init__(self, request, *args, **kwargs):
#         self.request = request
#         super(CartForm, self).__init__(*args, **kwargs)




# class CheckoutForm(forms.ModelForm):
#     class Meta:
#         model = Order
#         fields = ['payment_option','delivery_options','address','phone']

# class CheckoutForm(models.Model):
#     # address = forms.CharField(required=False)
#     # phone = forms.CharField(required=False)
#     # delivery_options = forms.CharField(required=False)
#     # same_billing_address = forms.BooleanField(required=False)
#     # payment_options = forms.CharField(required=False)
#     PAYMENT_CHOICES = (
#     ('S', 'โอนผ่านบัญชีธนาคาร'), 
#     ('เงินสด', 'เงินสด')
# )
#     payment_option = forms.CharField(max_length=1 ,
#        widget=forms.Select(choices=PAYMENT_CHOICES))

class CheckoutForm(forms.Form):
    # address = forms.CharField(required=False)
    # phone = forms.CharField(required=False)
    # delivery_options = forms.CharField(required=False)
    # same_billing_address = forms.BooleanField(required=False)
    # payment_options = forms.CharField(required=False)
    payment_option = forms.ChoiceField(
        widget=forms.RadioSelect, choices=PAYMENT_CHOICES)



# class PaymentForm(forms.Form): 
#     stripeToken = forms.CharField(required=False)
#     save = forms.BooleanField(required=False)
#     img = forms.ImageField(required=False)
#     use_default = forms.BooleanField(required=False)
# class CheckoutForm(forms.ModelForm):
#     class Meta:
#         model = Order
#         # exclude = ('paid',)
#         fields = [   'address', 'delivery_options','payment_options']

        # widgets = {
        #     'address': forms.Textarea(attrs={'row': 6, 'col': 8}),
        # }
class EditOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [ 'money_status']


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        # fields = '__all__'
        fields = [  'name','price', 'product_detail', 'product_img','product_type','quantity' ]

class Product_TypeForm(forms.ModelForm):
    class Meta:
        model = Product_Type
        # fields = '__all__'
        fields = [  'product_type']

class StoreForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = '__all__'
        # fields = [  'product_name','product_price', 'product_detail', 'product_img','product_type','product_status','product_amount' ]


class MechanicForm(forms.ModelForm):
    class Meta:
        model = Mechanic
        fields = ['mechanic_fname','mechanic_lname','mechanic_phone','mechanic_email','avatar','mechanic_img','mechanic_detail','mechanic_type']

class Mechanic_TypeForm(forms.ModelForm):
    class Meta:
        model = Mechanic_Type
        # fields = '__all__'
        fields = [  'mechanic_type']

class UsersForm(forms.ModelForm):

    class Meta: 
        model = Users 
        fields = [ 'first_name' ,'last_name', 'email','phone', 'avatar','username','password', ]
    
class EditProfileForm(forms.ModelForm):

    class Meta: 
        model = Users 
        fields = [ 'first_name' ,'last_name',  'avatar','phone']

class StoreForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = '__all__'

# class AddStockForm(forms.ModelForm):
#     class Meta:
#         model = Product
#         fields = ['received_quantity']    #เพิ่มจำนวนสินค้าในสต๊อก

# class SaleForm(forms.ModelForm):
#     class Meta: 
#         model = Sale
#         fields = ["quantity"]

# class LineItemForm(forms.ModelForm):
#     class Meta: 
#         model = LineItem
#         fields = '__all__' 