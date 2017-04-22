
from Handle import handle, handleMessage, handleQuery
from sudoCommands import isRunning, startBot
from Modules import Load, Save, Log
from Messages import Message
from time import time, sleep

    # try statement to check for valid BOT token
outtimed = None
try: outtimed = Message.getUpdates()
except: raise BaseException('No internet connection or invalid BOT token!')

    # handle all outtimed messages
    # loop needed because telegram sends maximum 100 updates
if outtimed:
    print('TIMED OUT:')
    while outtimed:
        for reply in outtimed: handle(reply,True)
        outtimed = Message.getUpdates()
    print('-'*80)
    del reply
del outtimed

    # add new global variable 'in_use'
    # decremented after every update; if eq 0 update itv is 5 sec
globals().update([('in_use', 9)]) # make in_use global

startBot()
    # save time when bot sarted
startTime = time()

    # main update loop
while(isRunning()):
    if in_use: in_use -= 1
    sleep(1 + 4*bool(not in_use))
    for reply in Message.getUpdates():
            # reset in_use status
        globals().update([('in_use', 9)])

        handle(reply)
