
from Messages import Message

while True:
    s = list(input('cmd: ').split('|'))
    if s!=('',):
        print(eval('Message.%s%s' % (s[0], str(tuple(s[1:])))))
