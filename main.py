class User():
    
    def __init__(self, id, username, email, password):
        self.id = id  # should be random unique int, change later
        self.username = username
        self.email = email  # should also be unique 
        self.password = password
        self.balance = 0  # user should add balance after account creation
    
    def get_id(self):
        return self.id
    
    def get_username(self):
        return self.username

    def get_email(self):
        return self.email
    
    def get_password(self):
        return self.password

if __name__ == "__main__":
    test = User(0, "kanchshres", "abcdef@gmail.com", "password123")
    print("ID: ", test.get_id())
    print("Username: ", test.get_username())
    print("Email: ", test.get_email())
    print("Password: ", test.get_password())
