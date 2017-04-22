
from Modules import Load, Save, path
from Objects import newCommand
from os.path import isfile
from os import remove
from Messages import Message

    # running status
running = False

    # 'start' bot
def startBot():
    global running
    running = True

    # return bool wether bot is runing or not
isRunning = lambda: running

    # returns bool wether cmd exists or not
hasCmd = lambda cmd: bool(Commands.get(cmd))

    # schedule stop
def stopBot(chatID, userID, data):
    global running
    running = False
    Message.sendToAll('Bot stopped!')
    return

    # return bool wether command exists
def hasCmd(cmd):
    return bool(Commands.get(cmd))

    # do smth with a file
def dofile(chatID, userID, data):
    fpath = path + 'Store/'
    
        # handle 'help' operation
    if len(data) > 1 and data[1] == 'help':
        return 'functions:\nmake\nget\ndelete\nclear'

        # handle wrong syntax
    if len(data) < 3:
        return 'Syntax:\n/file path action\ntype /file help for a list of all actions'
    
        # return error if file does not exist
    if not isfile(fpath):
        return 'File \'%s\' does not exist!' % fpath
    
    f = None
    ret = ''
    
            # file created with open(p,'w')
    if data[1] == 'make':
        f = open(fpath, 'w')
        ret = 'file %s created'
        
            # send the requested file
    elif data[1] == 'get':
        Message.sendFile(chatID, fpath)
        ret = 'sent %s'
        
            # deletes the file
    elif data[1] == 'delete':
        remove(fpath)
        ret = '%s deleted'
        
            # clear file
    elif data[1] == 'clear':
        f = open(fpath,'w')
        f.write('')
        ret = '%s cleared'
        
    else:   # handle unknown operations
        ret = 'unknown operation \'%s\' on %s' % data[1]
    
    if f: f.close()
    return ret % data[2]

    # return command list
def getCmds(chatID, userID, data):
    s = ''
    for key in Commands:
        s += key + '\n'
        continue
    return s

    # return command syntax and info
def sendHelp(chatID, userID, data):
    if len(data) == 0:
        return 'Welcome home! This is the admin part!\ntype /sudo help cmd to get help of any sudo command'
        # return eror if command not exist
    if Commands.get(data[0]) == None: return 'unknown super command \'%s\'' % data[0]
        # return command syntax and description
    else: return 'Syntax:\n%s\n\nDescription:\n%s' % (Commands[data[0]]['syntax'], Commands[data[0]]['info'])

    # delete inactive polls from file
def delPolls(chatID, userID, data):
    if isfile(path + 'Store/Poll'):
            # create new poll dict
        newPolls = {}
        Polls = Load('Poll', {})

            # copy active polls to new poll dict
        for poll in Polls:
            if Polls[poll]['active']:
                newPolls[poll] = Polls[poll]
            continue

            # save new poll dict
        Save('Poll', newPolls)
    else:
        return 'Poll file does not exist'
    return 'deleted'

    # in- / decrease user rank
def chRank(uname, inc, userID):
        # load users
    User = Load('User', {})
        # catch tries to degrade me, Symbroson, the big developer
    if uname == 'Symbroson' and inc == -1:
            # catch if I try do that
        if User[userID]['username'] != 'Symbroson':
                # set user rank to lowest
            User[userID]['id'] = 0
            Save('User', User)
            return '@%s has no rights any more because of trying to degrade the big developer' % User[userID]['username']
        else:
            return 'also you, the big developer, can\'t degrade the big developer'

        # find userID by username
    user = None
    for targetID in User:
        if User[targetID]['username'] == uname:
            user = User[targetID]
            break
        continue

        # user not found
    if user == None: return 'User \'%s\' not found!' % uname
        # user already on lowest rank
    elif user['id'] + inc < 0: return '@%s couldn\'t be degraded' % uname
    elif user['id'] + inc > 3: return '@%s couldn\'t be promoted' % uname
        # user is already superuser and I, Symbroson, the big developer, was not the promoter
    elif user['id'] + inc == 3 and not User[userID]['username'] == 'Symbroson':
        return 'Just @Symbroson can promote users to admin'

        # in- / decrease rank
    user['id'] += inc
        # save users
    Save('User', User)
        # send current user rank
    return '@%s is %s now!' % (uname, ['without rights', 'normal user', 'superuser', 'admin'][user['id']])

    # command dict
Commands = {
    'file' : newCommand('/file func path',
            'sends a file from the Store folder',
            'msg', dofile
        ),
    'delpolls' : newCommand('/delpolls',
        'deletes closed polls from file',
            'msg', delPolls
        ),
    'lscmds' : newCommand('/lscmds',
            'lists all sudo functions',
            'msg', getCmds
        ),
    'help' : newCommand('/help + cmd',
            'returns help of a sudo command',
            'msg', sendHelp
        ),
    'stop' : newCommand('/stop',
            'stops the bot',
            'call', stopBot
        ),
    'promote' : newCommand('/promote @user',
            'upgrades to superuser',
            'msg', lambda chatID, userID, data : chRank(data[1][1:], 1, userID)
        ),
    'degrade' : newCommand('/degrade @user',
            'degrades to normal user',
            'msg', lambda chatID, userID, data : chRank(data[1][1:], -1, userID)
        ),
    'start' : newCommand('/start',
            'send start message to all known chats',
            'call', lambda chatID, userID, data : Message.sendToAll('Bot started!')
        )
}
