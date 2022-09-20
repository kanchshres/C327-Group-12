class User():
    
    def __init__(self):
        self._myID = 0  # should be random unique int, change later
        self._myUsername = ""
        self._myEmail = ""   # should also be unique 
        self._myPassword = ""
        self._myBalance = 0  # user should add balance after account creation

    @property
    def myID(self):
        return self._myID

    @myID.setter
    def myID(self, id):
        self._myID = id
    
    @property
    def myUsername(self):
        return self._myUsername
    
    @myUsername.setter
    def myUsername(self, username):
        self._myUsername = username

    @property
    def myEmail(self):
        return self._myEmail

    @myEmail.setter
    def myEmail(self, email):
        self._myEmail = email
        
    @property
    def myPassword(self):
        return self._myPassword

    @myPassword.setter
    def myPassword(self, password):
        self._myPassword = password

    @property
    def myBalance(self):
        return self._balance