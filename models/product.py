class Product:
    def __init__(self, name, category, price, product_id=None):
        self.product_id = product_id
        self.name = name
        self.category = category
        self.price = price

    def __repr__(self):
        return f"<Product(name={self.name}, price={self.price})>"