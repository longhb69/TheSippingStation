from dataclasses import dataclass
from .models import Command

@dataclass
class CartController:
    def Invoke(self, command:Command):
        command.execute()
        
@dataclass
class OrderController:
    def execute(self, command:Command):
        command.execute()