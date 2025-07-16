
import utils
from models import UserModel, ProductModel

class Application:
    def __init__(self):
        self.users = []
        self.products = []
    
    def add_user(self, user: UserModel):
        self.users.append(user)
    
    def add_product(self, product: ProductModel):
        self.products.append(product)

def main():
    app = Application()
    print("Application started")

if __name__ == "__main__":
    main()
