class User(object):
    def __init__(self,username=None,password=None,email = None):
        self.username = username
        self.password =  password
        self.email = email

    @classmethod
    def Admin(cls):
        return cls(username='admin',password="admin")

    @classmethod
    def User(cls, RegUser, RegPassword):
        return cls(username=str(RegUser),password=str(RegPassword))

