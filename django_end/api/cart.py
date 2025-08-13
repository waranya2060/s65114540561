# from api.models import *
# from django.shortcuts import render
# from django import template

# register = template.Library()
# @register.filter

# def productTypeUser(request,id=0): 
#     type=Product_Type.objects.get(pk=id)
#     product_type=Product_Type.objects.all()
#     # adminn = Adminn.objects.get(username=request.user.username)
#     product=Product.objects.filter(product_type=type).order_by('id')
#     # item_count = cart.item_count(request)
#     # mechanic= Mechanic.objects.all()
#     print(type)
#     return render(request,'api/productTypeUser.html',{
#         'product':product,
#         'type' :type,
#         'product_type':product_type,
#         # 'cart_item_count':item_count
#         # 'adminn' :adminn
#         })