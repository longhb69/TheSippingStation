from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from product.models import ProductDecorator,DLC,SpecialEditionGame
from product.serializers import ProductDecoratorSerializer
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
import datetime
from django.http import JsonResponse
from django.contrib.contenttypes.models import ContentType
from .command import  AddToCartCommand,RemoveFromCartCommand
from .controller import CartController



class CartView(APIView):
    def get(self, request):
        user = User.objects.get(username="long1")
        cart = Cart.objects.get(user=user)
        serializer = CartSerializer(cart, many=False).data
        #test = ProductDecorator.objects.get(name="Cyberpunk 2077")
        #serializer = ProductDecoratorSerializer(test, many=False).data
        return Response(serializer)
    
    #{"special": false,"dlc":true,"game_id":2,"cart_id":2}
    def post(self, request, *args, **kwargs):
        special = request.data.get('special')
        dlc = request.data.get('dlc')
        game_id = request.data.get('game_id')
        cart_id = request.data.get('cart_id')
        
        cart = get_object_or_404(Cart,pk=cart_id)            
        if dlc: 
            #cart_item_content_type = ContentType.objects.get_for_model(DLC)
            product = get_object_or_404(DLC,pk=game_id)
        elif special:
            product = get_object_or_404(SpecialEditionGame, pk=game_id)
        else:
            product = get_object_or_404(ProductDecorator, pk=game_id)
        try:
            cart_item = CartItem.objects.create(cart=cart,  product=product)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
                
        return JsonResponse({'message': 'CartItem created successfully'}, status=201)
    
    def delete(self, request, *args, **kwargs):
        item_pk = kwargs.get('item_pk')
        cart_item = CartItem.objects.get(pk=item_pk)
        cart_item.delete()
        return Response('item delete')
        

@api_view(["DELETE"])
def delete_dlc_in_cart(requset, *args, **kwargs):
    #cart_item = get_object_or_404(CartItem, pk=pk)
    cart_pk = kwargs.get('cart_pk')
    item_pk = kwargs.get('item_pk')
    product_pk = kwargs.get('product_pk')
    dlc_pk = kwargs.get('dlc_pk')
    
    cart_item = CartItem.objects.get(pk=item_pk)
    cart = Cart.objects.get(pk=cart_pk)
    dlc = DLC.objects.get(pk=dlc_pk)
    product = ProductDecorator.objects.get(pk=product_pk)
    product.delete_dlc(dlc)
    cart_item.save()
    return Response(' ')



def checkout(request):
    # user = User.objects.get(username="long1")
    # transaction_id = datetime.datetime.now().timestamp()
    # order, created = Order.objects.get_or_create(user=user)
    # order_item = OrderItem.objects.get(pk=1)
    # print(order.get_order_total)
    #dlc = CartItem.objects.get(pk=3)
    #game = CartItem.objects.get(pk=10)
    game = SpecialEditionGame.objects.get(pk=1) 
    user = User.objects.get(username="long1")
    cart = Cart.objects.get(user=user)
    controller = CartController()
    controller.Invoke(AddToCartCommand(cart=cart, item=game))
    return render(request, "home/inbox.html")
