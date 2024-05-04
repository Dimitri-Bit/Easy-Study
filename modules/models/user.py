class User:

    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

def mapUser(id, username, password):
    return User(id, username, password)

def mapUser(touple):
    return User(touple[0], touple[1], touple[2])