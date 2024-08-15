from string import ascii_letters
from random import choice


def generate_url(length: int = 10):
    """
    Return the ASCII symbol sequence with provided length
    """
    
    return ''.join(choice(ascii_letters) for _ in range(length))