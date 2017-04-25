
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

    # contains functions to send messages
class Messages:
        # normal text message
    def sendMessage(self, chatID, text, reply_id=None, markup=None):
        return self.send('sendMessage', newMessage(chatID, text, reply_id, markup))
    
        # sticker
    def sendSticker(self, chatID, image, name='Sticker.png'):
        return self.send('sendSticker',
                         {'chat_id':chatID, 'sticker':(name, image)})

        # file
    def sendDocument(self, chatID, path):
        f = open(path, 'rb')
        response = self.sendFile('sendDocument',
                    {'chat_id':chatID, 'document':(path.split('/')[-1], f.read())})
        f.close()
        return response
    
        # query_reply
    def answerQuery(self, queryID, text):
        return self.send('answerCallbackQuery', {'callback_query_id':queryID, 'text':text})

        # edit message
    def editMessage(self, chatID, msgID, text):
        msg = newMessage(chatID, text)
        msg['message_id'] = msgID
        return self.send('editMessageText', msg)
    
        # update list
    def getUpdates(self):
        response = self.botRequest('GET', 'getUpdates', {'offset':Load('Offset',0) + 1})
        updates = response.get('result')
        if not updates: return []
        elif len(updates):
                # save last update_id as offset
            Save('Offset', updates[-1]['update_id'])
        return updates

        # sends a message to all known chats
    def sendToAll(self, msg):
        Log('sendToAll', msg + '\n' + 100*'-')
        for chatID in Load('Chats', {}):
            self.sendMessage(chatID, msg)
        
        # handle post request
    def send(self, func, asset = None):
            # replace 'me' with private chat id
        Log(func, asset['chat_id'], asset)
        if asset['chat_id'] == 'me':
            asset['chat_id'] = myChatID 

        response = self.botRequest('POST', func, asset)
        
            # check for successful request
        if response.get('result'):
            response = response.get('result')
                # save messageID of sent message
            sent = Load('Sent', [])
            sent.append('%s|%s' % (response['chat']['id'], response['message_id']))
            Save('Sent', sent)
            Log('Sent', response['chat']['id'], response['message_id'])
            return response
        else:
                # an error occured
            print('Error:', response['description'])
            Log('HrError', response['description'])
        return None

    def sendFile(self, func, asset):
        Log(func, asset['chat_id'], asset[func[4:].lower()][0])
        
            # replace 'me' with private chat id
        if asset['chat_id'] == 'me':
            asset['chat_id'] = myChatID 

        response = self.botRequest('POST', func, asset)
        
            # check for successful request
        if response.get('result'):
            response = response.get('result')
                # save messageID of sent message
            sent = Load('Sent', [])
            sent.append('%s|%s' % (s['chat']['id'], response['message_id']))
            Save('Sent', sent)
            Log('Sent', response['chat']['id'], response['message_id'])
            return response
        else:
                # an error occured
            print('Error:', response['description'])
            Log('HrError', response['description'])
        return None
    
        # send bot request
    def botRequest(self, method, func, asset={}):
        response = self.request(method, 'api.telegram.org', 'bot%s/%s' % (token, func), asset)
        return loads(strip(response))

        # send request
    def request(self, method, host, path='', asset={}):
        return Request.send(method, host, path, asset)

Message = Messages()
