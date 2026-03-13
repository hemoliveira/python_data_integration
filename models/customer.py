class Customer:
    def __init__(self, name, city, customer_id=None, created_at=None):
        self.customer_id = customer_id
        self.name = name
        self.city = city
        self.created_at = created_at

    def __repr__(self):
        return f"<Customer(name={self.name}, city={self.city})>"