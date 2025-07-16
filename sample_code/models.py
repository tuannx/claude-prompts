
class UserModel:
    def __init__(self, name, email):
        self.name = name
        self.email = email
    
    def get_info(self):
        return f"{self.name} ({self.email})"

class ProductModel:
    def __init__(self, name, price):
        self.name = name
        self.price = price
    
    def get_price_with_tax(self, tax_rate=0.1):
        return self.price * (1 + tax_rate)
