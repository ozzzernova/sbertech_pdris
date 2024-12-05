from hashlib import *


def hash_function(text):
    tmp = hash(text) % 2
    if tmp == 1:
        action = "upgrade click by "
    else:
       action = "upgrade autoclick by "
    sign = (-1)**(hash(text) % 2)
    change = hash(text) % 3
    action += str(sign * change)
    return action, tmp, sign, change
