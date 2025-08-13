
# from typing import KeysView
from django.contrib import admin
from django.urls import path, include
# from django.contrib.auth.models import User
from api.models import *
from api import views
from api import cart
from api.views import CheckoutView, OrderSummaryView, PaymentView, remove_from_cart, remove_single_item_from_cart
from django.conf import settings # new

from django.conf.urls.static import static 
# from django.conf.urls import urls

from django.urls import path, include
# from . import \
# CheckoutView,\
#     add_to_cart,\
  


urlpatterns = [  
    path('users/<int:pk>/',views.ProfileDetailView.as_view(),name='profile_detail'),
    # path('bankTransfer/<int:pk>/',views.bankTransferlView.as_view() ,name='bankTransfer'),
    path('',views.index, name='index'), 
    path('index',views.index),
     path('payment_detail/<int:id>/',views.payment_detail),
    # path('login',views.login),
    # path('register',views.register),
    path('login/',views.login),
    path('register/',views.register), 
    path('logout/',views.logout),     
    path('editstore/<int:id>/', views.editstore),  
    
    # path('editstore', views.editstore), 
    path('store',views.store),
   
    path('product/',views.product),
    path('addproductType',views.addproductType),
    path('editproductType/<int:id>/', views.editproductType),
    path('deleteproductType/<int:id>', views.deleteproductType),
    # path('showproductType',views.showproductType),
    path('addproduct',views.addproduct),
    # path('editproduct',views.editproduct),
    path('editproduct/<int:id>/', views.editproduct),
    path('deleteproduct/<int:id>', views.deleteproduct),
    # path('product_search/', views.product_search, name='product_search'),
    path('mechanic',views.mechanic),
    path('addmechanic',views.addmechanic),
    path('editmechanic/<int:id>/', views.editmechanic),
    path('deletemechanic/<int:id>/', views.deletemechanic),  
    path('addmechanicType',views.addmechanicType),
    path('deletemechanicType/<int:id>/', views.deletemechanicType),  
    path('editmechanicType/<int:id>/', views.editmechanicType),  

    path('orderAll',views.orderAll),
    path('editOrder/<int:id>/', views.editOrder), 
    path('orderproductAll/<int:id>/',views.orderproductAll),
    
    # path('stock',views.stock),
    path('addbank',views.addbank), 
    path('bank',views.bank),
    path('deletebank/<int:id>/', views.deletebank), 
    path('editbank/<int:id>/', views.editbank),  
    # path('payment',views.payment),  

    # path('home2',views.home2),  
    # path('home',views.home), 
    path('base2',views.base2), 
    
    path('mechanicDetailUser/<int:id>/',views.mechanicDetailUser),   
    path('storeUser',views.storeUser),  
    path('register1',views.register1),
    path('mechanicUser',views.mechanicUser),    
    # path('product_type',views.product_type,name='product_type'),
    path('productTypeUser/<int:id>',views.productTypeUser,name='productTypeUser'),
    path('productDetail/<int:id>',views.productDetail,),
    # path('product/<int:pk>', ItemDetailView.as_view(), name='product-detail'),
    # path('test',views.test), 
    # path('cart',views.cart), 
    # path('checkout',views.checkout),  

    path('add-to-cart/<int:id>', views.add_to_cart, name='add-to-cart'),
    path('checkout/', CheckoutView.as_view(), name='check-out'),
    path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),
    path('remove-from-cart/<int:id>', remove_from_cart, name='remove-from-cart'),
    path('remove-single-item-from-cart/<int:id>', remove_single_item_from_cart, name='remove-single-item-from-cart'),
    path('payment/<payment_option>', PaymentView.as_view(), name='payment'),
    # path('payment/<payment_option>', PaymentMethod.as_view(), name='payment'),
    
 

    path('search',views.search,name='search'),
    # path('addstore',views.addstore,name='addstore'),
    path('showProductAll',views.showProductAll,name='showProductAll'),
    # path('add_to_stock/<str:pk>/', views.add_to_stock, name='add_to_stock'),
    # path('issue_item/<str:pk>/', views.issue_item, name='issue_item'),  
     
    # path('cart/', views.show_cart, name='show_cart'),
    path('home', views.home,),
    # path('checkout/', views.checkout,  name='checkout'),
 

    path('profile',views.profile),
    path('editprofile/<int:id>/', views.editprofile),

    # path('test1/<int:id>/', views.test1),
    path('order',views.order), 
    path('orderproduct/<int:id>/', views.orderproduct),
    # path('orderproduct/<int:id>/', views.orderproduct),
  
   

    path('admin/', admin.site.urls),
    # path('api/', include(router.urls)),
    # path('api-auth/', include('rest_framework.urls'))
]


# if settings.DEBUG: # new
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    # import debug_toolbar
    # urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
