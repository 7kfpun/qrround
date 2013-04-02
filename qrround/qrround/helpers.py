#from hashlib import md5
#from time import time
import random
import string


def unique_generator(
        size=6,
        chars=string.ascii_uppercase + string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))


#def unique_generator(size=8):
#    return md5(str(time()) + 'QRROUND').hexdigest()[:size]  # MAX: 32
