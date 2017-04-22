from Modules import Load, Save, Log, strip
from Objects import newMessage
from Request import Request
from json import loads

'''
    To create your own bot you have to go to the BotFather chat
    and write /newbot . After some settings you'll get a token
    which you have to paste to the bot token string below
    token format: '000000000:xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

    Your private chat id you get when running the bot and
    post a message from your bot (as contact) chat
'''

    # your bot's token
token = '<BOT-TOKEN>'
    # my private chat
myChatID = 000000000
    # offset to avoid receiving messages twice or more
offset   = Load('Offset', 1)

    # contains functions to send messages
class Messages:
        # normal text message
    def sendMessage(self, chatID, text, reply_id=None, markup=None):
        print('sendMessage', chatID, text, reply_id, markup)
        return Message.botRequest('POST', 'sendMessage', newMessage(chatID, text, reply_id, markup))
    
        # sticker
    def sendSticker(self, chatID, image, name='Sticker.png'):
        print('sendSticker', chatID, name)
        return Message.botRequest('POST', 'sendSticker',
                         {'chat_id':chatID, 'sticker':(name, image)})

        # file
    def sendFile(self, chatID, path):
        print('sendDocument', chatID, path)
        f = open(path, 'rb')
        s = Message.botRequest('POST', 'sendDocument',
                    {'chat_id':chatID, 'document':(path.split('/')[-1], f.read())})
        f.close()
        return s

        # query_reply
    def answerQuery(self, queryID, text):
        print('answerQuery', queryID, text)
        return Message.botRequest('POST', 'answerCallbackQuery', {'callback_query_id':queryID, 'text':text})

        # edit message
    def editMessage(self, chatID, msgID, text):
        print('editMessage', chatID, text)
        msg = newMessage(chatID, text)
        msg['message_id'] = msgID
        return Message.botRequest('POST', 'editMessageText', msg)
    
        # update list
    def getUpdates(self):
        global offset
        response = Message.botRequest('GET', 'getUpdates', {'offset':offset + 1})
        updates = response.get('result')
        if not updates:
            return []
        elif len(updates):
                # save updates to log file
            Log('Update', updates)
                # save last update_id as offset
            offset = updates[-1]['update_id']
            Save('Offset', offset)
        return updates

        # sends a message to all known chats
    def sendToAll(self, msg):
        print(msg)
        Log('Status', msg + '\n' + 100*'-')
        for chatID in Load('Chats', {}):
            Message.sendMessage(chatID, msg)
        
        # send HttpRequest
    def send(self, func, asset = None):
            # replace 'me' with private chat id
        if asset['chat_id'] == 'me':
            asset['chat_id'] = myChatIDs 

            # save sent message in log file
        Log('Send', func, asset)
        s = Message.botRequest('POST', func, asset)

            # check for successful request
        if s.get('result'):
            s = s.get('result')
                # save messageID of sent message
            sent = Load('Sent', [])
            sent.append(str(s['chat']['id']) + '|' + str(s['message_id']))
            Save('Sent', sent)
            Log('Sent', s)
            return s
        else:
                # an error occured
            print(s['description'])
            Log('HrError', s['description'])
        return None

        # send bot request
    def botRequest(self, method, func, asset={}):
        s = Message.request(method, 'api.telegram.org', 'bot%s/%s' % (token, func), asset)
        return loads(strip(s))

        # send request
    def request(self, method, host, path='', asset={}):
        return Request.send(method, host, path, asset)

Message = Messages()
