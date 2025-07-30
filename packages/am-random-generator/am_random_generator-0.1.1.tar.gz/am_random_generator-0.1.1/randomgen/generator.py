import random
import string

def generate_random(length, type='both'):
    if length <= 0:
        raise ValueError("Length must be a positive integer.")

    if type == 'number':
        chars = string.digits
    elif type == 'char':
        chars = string.ascii_letters
    elif type == 'both':
        chars = string.ascii_letters + string.digits
    else:
        raise ValueError("Type must be 'number', 'char', or 'both'.")

    return ''.join(random.choice(chars) for _ in range(length))