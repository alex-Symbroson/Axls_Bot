
from json import dumps

    # command
def newCommand(syntax, info, action, reply):
    return {'reply'  : reply,
            'info'   : info,
            'syntax' : syntax,
            'action' : action
            }

    # poll
def newPoll(creator, question, answers):
    return {'creator'  : creator,
            'question' : question,
            'answers'  : answers,
            'replies'  : {},
            'sumID'    : '',
            'active'   : True
            }

    # inline Button
def newInBtn(text, callback_data):
    return {'text'          : text,
            'callback_data' : callback_data
            }

    # message
def newMessage(chatID, text, reply_id=None, markup=None):
    msg = {'chat_id' : chatID,
           'text'    : text
           }
    if markup: msg['reply_markup'] = dumps(markup)
    if reply_id: msg['reply_to_message_id'] = reply_id
    return msg
