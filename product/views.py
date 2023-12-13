from django.shortcuts import render
from .models import Category,Game,DLC,Decorator
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from django.urls import reverse
from .serializers import CategorySerializer,GameSerializer,GameDetailSerializer,DLCSerializer,DLCDetailSerializer
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import mixins 
from django.shortcuts import get_object_or_404


class CategoryMixinView(mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        GenericAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'name'
    
    def get_object(self, category):
        try:
            category = Category.objects.get(slug=category)
            return Game.objects.filter(category=category)
        except Category.DoesNotExist:
            return JsonResponse("Category doesn't exists!")
    
    def get(self, request, *args, **kwargs):
        category = kwargs.get('slug')
        if category is not None:
            instance = self.get_object(category)
            serializer = GameSerializer(instance, many=True).data
            return Response(serializer)
        return self.list(request, *args, **kwargs)

def index(request):
    game = Game.objects.get(name = "Grand Theft Auto V")
    dlc = DLC.objects.get(name="Cyberpunk 2077: Phantom Liberty")
    dlc2 = DLC.objects.get(name="test")
    test = Decorator.objects.create(game = game)
    test.add_dlc(dlc)
    print(test.get_cost())
    return render(request, "home/inbox.html")

@api_view(["POST", "GET"])
def game_alt_view(request, slug=None, *args, **kwargs):
    method = request.method
    if method == "GET":
        if slug is not None:
            print(slug)
            obj = get_object_or_404(Game, slug=slug)
            data = GameDetailSerializer(obj,many=False).data
            return Response(data)
        queryset = Game.objects.all()
        data = GameSerializer(queryset, many=True).data
        return Response(data) 
    
@api_view(["POST", "GET"])
def dlc_alt_view(request, slug=None, *args, **kwargs):
    method = request.method
    if method == "GET":
        if slug is not None:
            game = get_object_or_404(DLC, slug=slug)
            data = DLCDetailSerializer(game,many=False).data
            return Response(data)
        queryset = Game.objects.all()
        data = GameSerializer(queryset, many=True).data
        return Response(data) 

# def add(request):
#     if request.method == 'POST':
#         condiments_selection = request.POST.getlist('condiments')
#         drink_name = request.POST.get('drink_name')
#         print(drink_name)
#         drink = Drink.objects.get(name=drink_name)
#         toppeddrink = Decorator.objects.create(beverage=drink)
#         print(condiments_selection)
#         for condiment in condiments_selection:
#             if Topping.objects.filter(name=condiment).exists():
#                 topping = Topping.objects.get(name=condiment)
#                 toppeddrink.add_topping(topping)
#                 print(toppeddrink.cost)
#         return render(request, "home/orderfrom.html", {
#             "drink": toppeddrink
#         })
# @api_view(["POST", "GET"])
# def drink_alt_view(request, slug=None, *args, **kwargs):
#     method = request.method
#     if method == "GET":
#         if slug is not None:
#             print(slug)
#             obj = get_object_or_404(Drink, slug=slug)
#             data = DrinkSerializer(obj,many=False).data
#             return Response(data)
#         queryset = Drink.objects.all()
#         data = DrinkSerializer(queryset, many=True).data
#         return Response(data) 

# @api_view(["POST", "GET"])
# def topping_alt_view(request, name=None, *args, **kwargs):
#     method = request.method
#     if method == "GET":
#         if name is not None:
#             obj = get_object_or_404(Topping, name=name)
#             data = ToppingSerializer(obj,many=False).data
#             return Response(data)
#         queryset = Topping.objects.all()
#         data = ToppingSerializer(queryset, many=True).data
#         return Response(data) 