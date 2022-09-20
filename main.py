class User():
    
    def __init__(self, id, username, email, password):
        self.id = id  # should be random unique int, change later
        self.username = username
        self.email = email  # should also be unique 
        self.password = password
        self.balance = 0  # user should add balance after account creation