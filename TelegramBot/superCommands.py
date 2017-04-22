
from Commands import getUsersByRank
from Modules import toMsg, Load, Save, perm
from Objects import newCommand
from Messages import Message
from random import randint

    # returns bool wether cmd exists or not
hasCmd = lambda cmd: bool(Commands.get(cmd))

    # return command syntax and description
def sendHelp(chatID, userID, data):
    if len(data) == 0:
        return '''
AxlsBot reference

type \'/lscmds\' to get a list of all available commands
type \'/help <cmd>\' to get informations about a command
informate me about bugs or feature request and I'll try to fix/add them
have fun :D
'''
        # return eror if command not exist
    if Commands.get(data[0]) == None: return 'unknown super command \'%s\'' % data[0]
        # return command syntax and description
    else: return 'Syntax:\n%s\n\nDescription:\n%s' % (Commands[data[0]]['syntax'], Commands[data[0]]['info'])

    # replace all messages sent by the bot with non-whitespace whitespace character
def minifyBotMsgs(chatID, userID, data):
    sent = Load('Sent', [])

    # ID format: 'chatID|messageID'
    for ID in sent:
        d = ID.split('|')
        if d[0] == chatID:
            Message.editMessage(d[0], d[1], '\u008d')
            sent.remove(ID)
        continue

    Save('Sent', sent)
    return 'minified'

    # returns stored data of one or all user
def getUser(username):
    User = Load('User', {})
        # '*' as placeholder for all
    if username == '*':
        s = 'registered users:'
            # creates a list of all users
        for userID in User:
            s += '\n' + User[userID]['username']
                    # add stars if super or admin
            if User[userID]['id'] > 1:
                s += ' (' + (User[userID]['id']-1)*'\u272c' + ') '
                # add symbol like dead head if user has slave rank
            if not User[userID]['id']:
                s += ' (\u0bd0)'
        return s

        # find user by username
    userID = None
    for userID in User:
        if User[userID]['username'] == username:
            break
        else: userID = None
        continue
    
        # break if user not found
    if not userID:
        return 'User \'' + username + '\' not found!'

        # returns detailed data about one user
    s = 'id: ' + str(userID) + '\n'
    for key in User[userID]:
        s += ('rank' + ': ' + perm(User[userID][key]) if key == 'id'
               else key + ': ' + str(User[userID][key])
              ) + '\n'
        continue
    return s
    
    # dict with command objects
Commands = {
    'minifybotmsgs' : newCommand('/minifybotmsgs',
            'edits all messages to nothing',
            'msg', minifyBotMsgs
        ),
    'lscmds' : newCommand('/lscmds',
            'returns a list of all commands',
            'msg', lambda chatID, userID, data : '\n'.join(Commands.keys())
        ),
    'help' : newCommand('/help + cmd',
            'returns help of a super command',
            'msg', sendHelp
        ),
    'getuser' : newCommand('/getuser @username',
            'returns data about a user',
            'msg', lambda chatID, userID, data : getUser(data[1].replace('@', ''))
        )
    }
