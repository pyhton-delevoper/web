def validate(user):
    if len(user['name']) < 3:
        return 'too short'


def find(id, users):
    for user in users:
        if user['id'] == id:
            return user


def get_user(email, users):
    for user in users:
        if user['email'] == email:
            return user
