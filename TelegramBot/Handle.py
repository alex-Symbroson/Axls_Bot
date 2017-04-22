
from superCommands import Commands as superCMD, hasCmd as isSuperCMD
from sudoCommands import Commands as sudoCMD, hasCmd as isSudoCMD
from Commands import Commands as normalCMD, hasCmd as isNormalCMD
from Modules import Load, Save, perm, path
from traceback import print_exc
from Messages import Message

    # return bool wether user has required rights
def checkPermission(chatID, userID, required):
    User = Load('User', {})
    if User[userID]['username'] == 'Symbroson': return True
    elif User[userID]['id'] < required:
        if chatID: Message.sendMessage(chatID, 'You need ' + ['normal', 'superuser', 'admin'][required-1] + ' permissions to do this!')
        return False
    return True

    # handles an update message
def handle(reply, answerAsReply=False):
        # get message from message type
    msgType = eval(" or ".join("\"%s\"" % Type if Type+'.' in "edited_message.callback_query." else "None" for Type in reply))
    if not msgType: return
    
    if msgType in 'edited_message':
        msg = reply[msgType]
        userID = str(msg['from']['id'])
    elif msgType == 'callback_query':
        msg = reply[msgType]['message']
        userID = str(reply[msgType]['from']['id'])
    else: return
    
    chatID = str(msg['chat']['id'])
        
        # saves user data if not known yet
    User = Load('User', {})
    if User.get(userID) == None:
        User[userID] = msg['from'].copy()
        User[userID]['id'] = 1
        Save('User', User)

        # saves new chatIDs
    Chats = Load('Chats', {})
    if not chatID in Chats:
        Chats[chatID] = 1
        Save('Chats', Chats)

        # select handle function dependent on message type
    
    if msgType in 'edited_message':
        isCmd = msg['text'].strip()[0] == '/'
        print('%s %s:%s: %s' % ('cmd' if isCmd else 'msg', chatID, msg['from']['username'], str(msg['text'].encode())[1:]))
        if isCmd: handleMessage(msg, userID, chatID, answerAsReply)
    elif msgType == 'callback_query':
        print('cbq %s:%s: %s' % (msgID, reply[msgType]['from']['username'], str(chat['text'].encode())[1:]))
        handleQuery(reply['callback_query'], userID, chatID)


    # handle normal messages
def handleMessage(msg, userID, chatID, Reply=False):
    msgText = msg['text'].strip()
    
        # break if message is no command
    if msgText[0] != '/' : return
    
    data = msgText[1:].split(' ')
        # make commands not case sensitive
    data[0] = data[0].lower()
    data[0] = data[0].replace('@axls_bot', '')
    
        # command object
    cmd = None
    
        # check for special permissions
    try: permission = ['slave', 'normal', 'super', 'sudo'].index(data[0])
    except: permission = 1
    else: data = data[1:] if permission > 1 else data
    
        # check if help wanted
    Help = data[0].lower() == 'help'
    if Help and len(data) > 1:
        data = data[1:]
        if data[0][0] == '/':
            data[0] = data[0][1:]

        # handle getcmdlst command
    if data[0] == 'getcmdlst' and checkPermission(chatID, userID, 3):
            # make a dict with all commands
        Cmds = {}
        Cmds.update([normalCMD, superCMD, sudoCMD])
        cmds = list(Cmds.keys())
        cmds.sort()
            # returns a list of all commands 'cmd-info'
        Message.sendMessage(chatID, '\n'.join('%s-%s' % (cmd, Cmds[cmd]['info'])for cmd in cmds), Reply*msg['message_id'])
        return
    
        # get required permission for the command
    required = (1*isNormalCMD(data[0]) or 2*isSuperCMD(data[0]) or 3*isSudoCMD(data[0]))
        # command not found
    if required == 0:
        Message.sendMessage(chatID, 'Command \'' + data[0] + '\' not found!', Reply*msg['message_id'])
        return
    
        # break if user hasn't required permissions for this command
    if not checkPermission(chatID, userID, required):
        return
        # warn user if tried to use higher permission
        # but continue because command is useable
    elif not checkPermission(None, userID, permission):
        Message.sendMessage(chatID, 'Warning: You are not ' + perm(permission) + '!', Reply*msg['message_id'])
    
        # find right command dict where to get the help from
    if Help:
            # search command in given permission - command dict
        cmd = [normalCMD, superCMD, sudoCMD][permission-1].get('help')
            # if command not found, find with required permissions
        if cmd['reply'](chatID, userID, data) == 'unknown':
            cmd = [normalCMD, superCMD, sudoCMD][required-1].get('help')
    else:
            # same again - search command in given or required dict
        cmd = [normalCMD, superCMD, sudoCMD][permission-1].get(data[0])
        if not cmd:
            cmd = [normalCMD, superCMD, sudoCMD][required-1].get(data[0])
    
        # catch errors in the unusual case that it wasnt found until now
    if not cmd:
        print(permission, required, Help, data)
        Message.sendMessage('me', 'BOT ERROR: tried to handle: '+str(data), Reply*msg['message_id'])
        return
    
    try:
        # call function dependent on action type
            # msg   : send returned message back
            # call  : function called with command
            # scall : function called with whole message
        if cmd['action'] == 'msg': Message.sendMessage(chatID, cmd['reply'](chatID, userID, data), Reply*msg['message_id'])
        elif cmd['action'] == 'call' : cmd['reply'](chatID, userID, data)
        elif cmd['action'] == 'scall' : cmd['reply'](chatID, msg)
    except:
             # return error if command execution failed
        Message.sendMessage(chatID, 'an error occured!', Reply*msg['message_id'])

            # put error message in log file
        f = open(path + 'Store/Errors', 'a')
        f.write('-'*100 + '\n')
        print_exc(None, f)
        f.close()


    # handle query (from poll inline keyboard)
def handleQuery(msg, userID, chatID):
    
        # data: 'pollID|reply_index'
    data = msg['data'].split('|')
    
        # load poll
    poll = Load('Poll', {}).get(data[0])
    if not poll:
        Message.answerQuery(msg['id'], 'this poll does not exist')
        return
    
    poll['replies'][userID] = data[1]
    Save('Poll', Poll)

        # build list with answer count
    cnt = []
    for i in Poll[data[0]]['answers']: cnt.append(0)
    for i in Poll[data[0]]['replies'].values(): cnt[int(i)-1] += 1

        # make notify text
    text = '%s chose %s' (msg['from']['username'], poll['answers'][int(data[1])-1])

        # make summary text
    sumText = 'Poll summary:\n%s\n\n' % poll['question']
    for i in range(0, len(poll['answers'])):
        sumText +=  '%s: %s\n\tchosen by %s member%s\n' % (chr(i + 65), poll['answers'][i], str(cnt[i]), 's'*(cnt[i]==1))

        # update poll summary
    s = Message.editMessage(msg['message']['chat']['id'], poll['sumID'], sumText)
        # notify chat who selected which answer
    Message.answerQuery(msg['id'], text)
