"""Python application module"""

class UserService:
    def __init__(self):
        self.users = []
    
    def add_user(self, user):
        self.users.append(user)
        
def main():
    service = UserService()
    print("Python app running")