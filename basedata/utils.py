from functools import reduce
from decimal import Decimal
import random



def decimal_add(x, y):
    '''
    This is an operator for a decimal addition.
    '''
    return Decimal(x) + Decimal(y)



def pin_generator(length=8):
    """Generates alphanumeric ids or keys
    
    Keyword Arguments:
        length {int} -- length of the pin (default: {8})
    
    Returns:
        {string} -- the pin generated
    """
    #List of characters to generate token from
    num = '0123456789'
    upper_alpha = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    lower_alpha = upper_alpha.lower()
    gen_base = [num,upper_alpha,lower_alpha]
    alphanum = ''.join(gen_base)

    token = ''

    for x in range(length):
        token += alphanum[random.randint(1,len(alphanum)-1)]
    return token


def convert_to_percent(value, total):
    try:
        percent = "%.2f" % ((value/total)*100)
        return float(percent)
    except ZeroDivisionError:
        return 0.0

        
