
from os.path import isfile, isdir
from json import loads, dumps
from _random import Random
from os import makedirs
from re import sub

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
    f = open(path + 'Store/Log.txt', 'a')
    log = Logtype + '\t'
    for arg in args: log += str(arg) + '\n\t'
    f.write(dumps(log[:-1]))
    f.close()
    return

    # loads a variable from the store-folder
def Load(file, default,decode=True):
    fpath = path + 'Store/'
    
        # create store folder if not exist
    if not isdir(fpath):
        makedirs(fpath)

    exist = isfile(fpath + file)
    if exist:
        f = open(fpath + file, 'r')
        s = f.read()

            # mark file as not existent if it is empty
        if s.strip() == '':
            exist = False
            f.close()
        elif decode:   # load value
            s = loads(s)

        # writes default data to file if it is empty or doesn't exist
    if not exist:
        f = open(fpath + file, 'w')
        f.write(dumps(default) if decode else default)
        s = default
        
    f.close()
    return s

    # saves a variable to the store-folder
def Save(file, value, encode=True):
    fpath = path + 'Store/'
    
        # create store folder if not exist
    if not isdir(fpath):
        makedirs(fpath)
    
    f = open(fpath + file, 'w')
    f.write(dumps(value) if encode else value)
    f.close()
    return

    # return string by command array
def toMsg(data):
    s = ''
    for v in data: s +=v + ' '
    return s

    # return permission name by index
def perm(i):
    return ['slave', 'normal', 'super', 'admin'][i]
