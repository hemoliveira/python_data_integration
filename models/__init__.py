from .customer import Customer
from .product import Product
from .order import Order, OrderItem

# Isso define o que será importado ao usar "from models import *"
__all__ = ['Customer', 'Product', 'Order', 'OrderItem']