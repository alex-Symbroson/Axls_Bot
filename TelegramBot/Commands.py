
from Modules import Load, Save, perm, ranint, toInt
from Poll import createPoll, cancelPoll
from Objects import newCommand
from Messages import Message
from Request import Request
from time import ctime
from re import split

    # returns bool wether cmd exists or not
hasCmd = lambda cmd: bool(Commands.get(cmd))

    # returns command syntax and description
def sendHelp(chatID, userID, data):
    if len(data) == 0: return '''AxlsBot reference\n
type \'/lscmds\' to get a list of all available commands
type \'/help <cmd>\' to get informations about a command
informate me about bugs or feature request and I'll try to fix/add them
have fun :D
'''
        # return eror if command not exist
    if Commands.get(data[0]) == None: return 'unknown super command \'%s\'' % data[0]
        # return command syntax and description
    else: return 'Syntax:\n%s\n\nDescription:\n%s' % (Commands[data[0]]['syntax'], Commands[data[0]]['info'])
    
    # save bug report to report log file
def reportBug(chatID, userID, data):
    if len(data) == 1: return 'write a bug report after \n/bugreport!'
    Save('Reports', '%s%s|%s:\n%s\n%s\n' % (Load('Reports', '',False), chatID, userID, ' '.join(data[1:]), 70*'-'),False)
    return 'bug reported!'

    # returns date in format 'day, DD. month YYYY HH:MM'
def getDate():
    s = ctime().split(' ')
    day = {'Mon':'Montag', 'Tue':'Dienstag', 'Wed':'Mittwoch', 'Thu':'Donnerstag',
           'Fri':'Freitag', 'Sat':'Samstag', 'Sun':'Sonntag'
           }.get(s[0])
    mon = {'Jan':'Januar', 'Feb':'Februar', 'Mar':'M\xe4rz', 'Apr':'April', 'May':'Mai',
           'Jun':'Juni', 'Jul':'Juli', 'Aug':'August', 'Sep':'September',
           'Oct':'Oktober', 'Nov':'November', 'Dec':'Dezember'
           }.get(s[1])
    return '%s, %s. %s %s %s' % (day, s[2], mon, s[4], s[3][:5])

    # return random number btw min and max seperated by ' ' or ', '
def ranInt(s):
    s = split(' |, ', s)

        # catch errors while parsing -> wrong syntax
    try: s = [toInt(s[0]), toInt(s[1])]
    except: return 'invalid arguments!\nType \'/help ranint\''
    
        # sort array because randint requires minimum first
    s.sort()
    return int(s[0] + ranint(s[1]-s[0]))
    
    # return list of users with given Rank
def getUsersByRank(rank):
    users = ''
    User = Load('User', {})
    for userID in User:
        if User[userID]['id'] == rank or rank == '*':
            users += User[userID]['username'] + '\n'

    if users == '': return 'no users with rank %s found!' % perm(rank) 
    else: return 'Users with rank %s:\n\n%s' % (perm(rank), users)

def getFunfact(chatID, userID, data):
    funfact = Message.request('GET', 'www.randomfunfacts.com', '').split('i>')[1][:-2]
    del Request.sockets['www.randomfunfacts.com']
    return funfact

    # dict with command objects
Commands = {
    'dice' : newCommand('/dice',
            'returns a random Number between 1 and 6',
            'msg', lambda chatID, userID, data : 1 + ranint(6)
        ),
    'active' : newCommand('/active',
    	    'returns \'I\'m active!\' if bot is active',
    	    'msg', lambda chatID, userID, data : 'I\'m active!'
    	),
    'ranint' : newCommand('/ranint min max',
            'returns random number between min and max.',
            'msg', lambda chatID, userID, data : ranInt(' '.join(data[1:]))
        ),
    'lscmds' : newCommand('/lscmds',
            'returns a list of all commands',
            'msg', lambda chatID, userID, data : '\n'.join(Commands.keys())
        ),
    'echo' : newCommand('/echo msg',
            'returns the text (not useful! :p)',
            'msg', lambda chatID, userID, data : ' '.join(data[1:]) or 'empty message text!'
        ),
    'help' : newCommand('/help + cmd',
            'returns general help or if given of a command',
            'msg', sendHelp
        ),
    'date' : newCommand('/date',
            'returns the current date and time',
            'msg', lambda chatID, userID, data : getDate()
        ),
    'calc' : newCommand('/calc term',
            'calculates a term with math functions',
            'msg', lambda chatID, userID, data : toInt(' '.join(data[1:]))
        ),
    'bugreport' : newCommand('/bugreport report',
            'report a bug you\'ve found',
            'msg', reportBug
        ),
    'help' : newCommand('/help + cmd',
            'returns help of a command',
            'msg', sendHelp
        ),
    'funfact' : newCommand('/funfact',
            'random funfact',
            'msg', getFunfact
        ),
    'cancelpoll' : newCommand('[summary-reply] /cancelpoll',
            'cancels the poll of the replied poll summary',
            'scall', cancelPoll
        ),
    'newpoll' : newCommand('/newpoll question \nanswer_1\nanswer_n',
            'creates a poll with answers seperated by enter',
            'call', createPoll
        ),
    'user' : newCommand('/user',
            'returns own user data',
            'msg', lambda chatID, userID, data : # returns data of sender; replace 'id: n' by 'rank: (rank)'
                        '\n'.join(('%s: %s'%('rank'if k=='id'else k, perm(v)if k=='id'else v))
                                  for k, v in Load('User', {})[userID].items())
        ),
    'slaves' : newCommand('/slaves',
            'returns a list with all users without rights',
            'msg', lambda chatID, userID, data : getUsersByRank(0)
        ),
    'supers' : newCommand('/supers',
            'returns a list with all superusers',
            'msg', lambda chatID, userID, data : getUsersByRank(2)
        ),
    'admins' : newCommand('/admins',
            'returns a list with all administrators',
            'msg', lambda chatID, userID, data : getUsersByRank(3)
        )
}
