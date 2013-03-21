from hashlib import md5
from time import time
#import random
#import string


#def unique_generator(size=16, chars=string.ascii_lowercase + string.digits):
#    return ''.join(random.choice(chars) for x in range(size))


def unique_generator(size=16):
    return md5(str(time()) + 'QRROUND').hexdigest()[:size]  # MAX: 32
