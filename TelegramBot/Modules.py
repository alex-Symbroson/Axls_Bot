
from os.path import isfile, isdir
from json import loads, dumps
from _random import Random
from os import makedirs
from re import sub
from math import *

random = Random()
ranint = lambda m:int(m*random.random())

    # get current project path
path = __file__[:__file__.rfind('/') + 1]

def strip(s):
    s = sub('\t|\r',' ',s)
    while s.find('  ') > -1:
        s = s.replace('  ',' ') 
    return s

    # saves data into the log file
def Log(Logtype, *args):
    print(Logtype, *args)
    f = open(path + 'Store/Log.txt', 'a')
    f.write('%s\t%s\n\n' % (Logtype, '\n\t'.join(str(arg) for arg in args)))
    f.close()
    return

    # loads a variable from the store-folder
def Load(file, default,decode=True):
    dpath = path + 'Store/'
    fpath = dpath + file + '.txt'
    
        # create store folder if not exist
    if not isdir(dpath): makedirs(dpath)

    exist = isfile(fpath)
    if exist:
        f = open(fpath, 'r')
        s = f.read()

            # mark file as not existent if it is empty
        if s.strip() == '':
            exist = False
            f.close()
        elif decode:   # load value
            s = loads(s)

        # writes default data to file if it is empty or doesn't exist
    if not exist:
        f = open(fpath, 'w')
        f.write(dumps(default) if decode else default)
        s = default
        
    f.close()
    return s

    # saves a variable to the store-folder
def Save(file, value, encode=True):
    dpath = path + 'Store/'
    fpath = dpath + file + '.txt'
    
        # create store folder if not exist
    if not isdir(dpath): makedirs(dpath)
    
    f = open(fpath, 'w')
    f.write(dumps(value) if encode else value)
    f.close()
    return

    # return permission name by index
def perm(i):
    return ['slave', 'normal', 'super', 'admin'][i]

    # allowed functions
allowed = ('abs|acos|acosh|asin|asinh|atan|atan2|atanh|ceil|copysign|cos|cosh|'
           'degrees|e|erf|erfc|exp|expm1|fabs|factorial|f1|floor|fmod|frexp|'
           'fsum|gamma|hypot|isfinite|isinf|isnan|ldexp|lgamma|log|log1|log2p|'
           'modf|pi|radians|round|sin|sinh|sqr|sqrt|tan|tanh|trunc|W|\+|\-|\*|'
           '\/|\^|\<|\>|\%|\&|\||\(|\)|[0-9]| |.|,')

sqr = lambda x:x**2

    # Lambert W-function (why?! XD)
    # inverted function to f(x)=x*e^x
def W(x):
        # y-result, d-digit as 10exponent, s-y*e^y, t-previous s
    y,d,s,t = 0,-2,0,-1
        # relation of s to x
    f = r = 1 if y*pow(e,y)<x else -1
    
    while d<17:                 # python calculates with 16 float digits
        while r==f:             # if relation of s to x changed - calc next digit
            if s==t:return y    # return if y*e^y == result
            t = s
            if abs(y) > 10000:return "NaN"    # x not in W(x)
            y += f*pow(10, -d)      # in/decrease a digit dependent on f
            s = y*pow(e, y)         # calculate x of current y value
            f = 1 if s < x else -1  # recalculate relation of s to x
            
        r, d = f, d+1
    return y

    # calculate int from string via eval
def toInt(s):
    if sub(allowed,"",s.lower()): return "not allowed!"
    try: return eval(s.lower())
    except ZeroDivisionError: return 'division by zero!'
    except: return 'Error!'
