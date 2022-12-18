def validate(user):
    if len(user['name']) < 3:
        return 'too short'
