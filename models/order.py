class OrderItem:
    def __init__(self, product_id, quantity, item_id=None, total=None):
        self.item_id = item_id
        self.product_id = product_id
        self.quantity = quantity
        self.total = total # Calculado pelo banco, mas útil para leitura

    def __repr__(self):
        return f"<OrderItem(product_id={self.product_id}, qty={self.quantity})>"

class Order:
    def __init__(self, customer_id, order_date, order_id=None):
        self.order_id = order_id
        self.customer_id = customer_id
        self.order_date = order_date
        self.items = [] # Lista de objetos OrderItem

    def add_item(self, product_id, quantity):
        """Adiciona um item à lista do pedido"""
        item = OrderItem(product_id, quantity)
        self.items.append(item)

    def __repr__(self):
        return f"<Order(id={self.order_id}, customer={self.customer_id}, items={len(self.items)})>"