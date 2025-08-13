# from rest_framework import routers, serializers, viewsets
# from .models import *
# # Serializers define the API representation.
# # class RoleSerializer(serializers.HyperlinkedModelSerializer):
# #     class Meta:
# #         model = Role
# #         fields = '__all__'

# # class UserSerializer(serializers.HyperlinkedModelSerializer):
# #     class Meta:
# #         model = User
# #         fields = '__all__'

# # class CustomerSerializer(serializers.HyperlinkedModelSerializer):
# #     class Meta:
# #         model = Customer
# #         fields = '__all__'

# # class AdminSerializer(serializers.HyperlinkedModelSerializer):
# #     class Meta:
# #         model = Admin
# #         fields = '__all__'

# class Mechanic_TypeSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Mechanic_Type
#         fields = '__all__'

# class MechanicSerializer(serializers.ModelSerializer):
#     mechanic_type = Mechanic_TypeSerializer(many=False, read_only=True)

#     class Meta:
#         fields = '__all__'
#         model = Mechanic

# # class MechanicSerializer(serializers.HyperlinkedModelSerializer):
# #     class Meta:
# #         model = Mechanic
# #         fields = '__all__'

# class StoreSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Store
#         fields = '__all__'

# class Product_TypeSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Product_Type
#         fields = '__all__'

# class Product_StatusSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Product_Status
#         fields = '__all__'
# class ProductSerializer(serializers.ModelSerializer):
#     product_type = Product_TypeSerializer(many=False, read_only=True)

#     class Meta:
#         fields = '__all__'
#         model = Product
# # class ProductSerializer(serializers.HyperlinkedModelSerializer):
# #     class Meta:
# #         model = Product
# #         fields = '__all__'
    
# class Money_StatusSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Money_Status
#         fields = '__all__'

# class Delivery_OptionsSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Delivery_Options
#         fields = '__all__'

# class Payment_OptionsSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Payment_Options
#         fields = '__all__'

# class OrderSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Order
#         fields = '__all__'

# # class PaymentSerializer(serializers.HyperlinkedModelSerializer):
# #     class Meta:
# #         model = Payment
# #         fields = '__all__'

# # class Order_ProductSerializer(serializers.HyperlinkedModelSerializer):
# #     class Meta:
# #         model = Order_Product
# #         fields = '__all__'

# # class CartsSerializer(serializers.HyperlinkedModelSerializer):
# #     class Meta:
# #         model = Carts
# #         fields = '__all__'

# # class ConversationsSerializer(serializers.HyperlinkedModelSerializer):
# #     class Meta:
# #         model = Conversations
# #         fields = '__all__'

# # class StorckSerializer(serializers.HyperlinkedModelSerializer):
# #     class Meta:
# #         model = Storck
# #         fields = '__all__'