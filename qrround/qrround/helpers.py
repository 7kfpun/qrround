import random
import string


def unique_generator(size=16, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))