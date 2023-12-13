from django.db import models
from cloudinary.models import CloudinaryField
from django.db import models
from abc import ABCMeta,ABC, abstractmethod
from django.utils.text import slugify
from unidecode import unidecode 

#import six

#don't forget to specity app path. For example:
#python manage.py makemigrations app
#python manage.py migrate app

class Slug(models.Model):
    slug = models.CharField(max_length=110,null=True, blank=True)
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(unidecode(self.name))
            return super().save(*args, **kwargs)
        return super().save(*args, **kwargs)
    class Meta:
        abstract = True
    
class Category(Slug):
    name = models.CharField(max_length=100, default=None)
    image = CloudinaryField('image', null=True, blank=True)
    slug = models.CharField(max_length=110,null=True, blank=True)
    
    def __str__(self):
        return self.name

class Item(models.Model):
    name = models.CharField(max_length=200,default=None,null=True,blank=True)            
    price = models.DecimalField(max_digits=10, decimal_places=3,default=0,null=True,blank=True)
    
    def __str__(self):
        return self.name
    
    def get_cost(self):
        return self.price
    
    def set_cost(self, price):
        self.price = price
        self.save()
    
    def get_Description(self):
        return self.name
        
    class Meta:
        abstract = True
    
class DecoratorManager(models.Manager):
    def create(self, game, **kwargs):
        kwargs.setdefault('name', game.get_Description())
        kwargs.setdefault('price', game.get_cost())
        
        decorator_instance = super().create(game=game, **kwargs)
        return decorator_instance
    
class Game(Item,Slug):
    overview_description = models.TextField(null=True, blank=True)
    detail_description = models.TextField(null=True, blank=True)
    image = CloudinaryField('image', null=True,blank=True)
    video = CloudinaryField(resource_type='video', null=True,blank=True)
    category = models.ManyToManyField(Category)
    os_min = models.CharField(max_length=50, verbose_name='Minimum OS', null=True, blank=True)
    os_rec = models.CharField(max_length=50, verbose_name='Recommended OS', null=True, blank=True)

    processor_min = models.CharField(max_length=100, verbose_name='Minimum Processor', null=True, blank=True)
    processor_rec = models.CharField(max_length=100, verbose_name='Recommended Processor', null=True, blank=True)

    memory_min = models.CharField(max_length=20, verbose_name='Minimum Memory', null=True, blank=True)
    memory_rec = models.CharField(max_length=20, verbose_name='Recommended Memory', null=True, blank=True)

    storage_min = models.CharField(max_length=20, verbose_name='Minimum Storage', null=True, blank=True)
    storage_rec = models.CharField(max_length=20, verbose_name='Recommended Storage', null=True, blank=True)

    directx_min = models.CharField(max_length=10, verbose_name='Minimum DirectX', null=True, blank=True)
    directx_rec = models.CharField(max_length=10, verbose_name='Recommended DirectX', null=True, blank=True)

    graphics_min = models.CharField(max_length=100, verbose_name='Minimum Graphics', null=True, blank=True)
    graphics_rec = models.CharField(max_length=100, verbose_name='Recommended Graphics', null=True, blank=True)


class DLC(Item,Slug):
    game = models.ForeignKey(Game, on_delete=models.CASCADE,null=True,blank=True, related_name='dlcs')
    overview_description = models.TextField(null=True, blank=True)
    detail_description = models.TextField(null=True, blank=True)
    image = CloudinaryField('image', null=True,blank=True)
    video = CloudinaryField(resource_type='video', null=True,blank=True)
    
class Decorator(Item):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, default=None)
    dlcs = models.ManyToManyField(DLC, blank=True)
    
    objects = DecoratorManager()   
    
    def add_dlc(self, dlc):
        self.dlcs.add(dlc)
        new_cost = self.price + dlc.get_cost()
        self.set_cost(new_cost)
        self.save()
        
        
    # #@property
    # def get_cost(self):
    #     base_cost = self.game.price
    #     dlcs_cost = sum(dlc.get_cost() for dlc in self.dlcs.all())
    #     new_cost = base_cost + dlcs_cost
    #     self.set_cost(new_cost)
    #     return new_cost
    
 


"""
This structure follows the decorator pattern, allowing you to dynamically add responsibilities (toppings and sizes) to objects (beverages) 
without modifying their code directly. It adheres to the principles of composition and separation of concerns
"""





# class Decorator(Item):
#     beverage = models.ForeignKey(Drink, on_delete=models.CASCADE, default=None)
#     toppings = models.ManyToManyField(Topping, blank=True)
#     size = models.ForeignKey(Size, blank=True, default=None, on_delete=models.SET_DEFAULT, null=True)
    
#     objects = DecoratorManager()
    
#     def add_topping(self, topping):
#         self.toppings.add(topping)
#         self.save()
        
#     #@property
#     def get_cost(self):
#         base_cost = self.beverage.price
#         topping_cost = sum(topping.get_cost() for topping in self.toppings.all())
#         size_cost = self.size.price if self.size else 0 
#         new_cost = base_cost + topping_cost + size_cost
#         self.set_cost(new_cost)
#         return new_cost

# class Size(models.Model):
#     class SizeChoice(models.TextChoices):
#         SMALL = 'Small'
#         MEDIUM = 'Medium'
#         LARGE = 'Large'
#     size = models.CharField(max_length=6,choices=SizeChoice)
#     price = models.DecimalField(max_digits=8, decimal_places=3, default=0)
    
#     def __str__(self):
#         return self.size + "-" + str(self.price)
# class Drink(Item):
#     description = models.CharField(max_length=500,null=True,blank=True)
#     image = CloudinaryField('iamge', null=True,blank=True)
#     category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True,blank=True)
#     sizes = models.ManyToManyField(Size)
    
# class Topping(Item):
#     pass    