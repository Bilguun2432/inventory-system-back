import random, string


def generate_reset_token():
    token_length = 12
    characters = string.ascii_letters + string.digits
    token = ''.join(random.choice(characters) for _ in range(token_length))
    return token