
Eval,Abs,Pow = eval,abs,pow

    # separate file to prevent the usage
    # of unwanted eval features
from math import *

    # Lambert W-function (why?! XD)
    # inverted function to f(x)=x*e^x
def W(x):
        # y-result, d-10-exponent, s-y*e^y, t-previous s
    y,d,s,t = 0,-2,0,-1
        # relation of s to x
    f = r = 1 if y*Pow(e,y)<x else -1
    
    while d<17:                 # python calculates with 16 float digits
        while r==f:             # if relation of s to x changed - calc next digit
            if s==t:return y    # return if y*e^y == result
            t = s
            if Abs(y) > 10000:return "NaN"    # x not in W(x)
            y += f*Pow(10, -d)      # in/decrease a digit dependent on f
            s = y*Pow(e, y)         # calculate x of current y value
            f = 1 if s < x else -1  # recalculate relation of s to x
            
        r, d = f, d+1
    return y

    # calculate int from string via eval
def toInt(s):
    try: return Eval(s)
    except ZeroDivisionError:
        return 'division by zero!'
    except: return 'Error!'
