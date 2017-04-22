
from PIL import Image, ImageDraw, ImageFont
from Objects import newPoll, newInBtn
from Modules import Load, Save, toMsg, path
from math import pi, sin, cos
from Messages import Message
from random import randint

    # draw rounded rectangle on PIL draw surface
def roundRect(draw, pos, radius, color, ):
        # adjust corner radius
    if(pos[2] - pos[0] < 2*radius): radius = int((pos[2] - pos[0])/2)
    if(pos[3] - pos[1] < 2*radius): radius = int((pos[3] - pos[1])/2)
    
    draw.rectangle((pos[0] + radius, pos[1], pos[2] - radius, pos[3]), color)
    draw.rectangle((pos[0], pos[1] + radius, pos[2], pos[3] - radius), color)
    
    draw.ellipse((pos[0], pos[1], pos[0] + 2*radius, pos[1] + 2*radius), color)
    draw.ellipse((pos[0], pos[3] - 2*radius, pos[0] + 2*radius, pos[3]), color)
    draw.ellipse((pos[2] - 2*radius, pos[1], pos[2], pos[1] + 2*radius), color)
    draw.ellipse((pos[2] - 2*radius, pos[3] - 2*radius, pos[2], pos[3]), color)

    # make pie chart image
def makeCake(arr):
        # constants
    size = 400  # pie chart diameter
    maxr = 2    # number coloumns in footer    3-(len(arr)%3)%2
    d = 1250    # number of lines to draw circle
    
    fs = int(size/4.7/maxr)  # fontsize
    fh = int(fs*1.3)         # (font)height
    
        # height: time_space + int(diameter + footer_distance + fontheight*lines)
    img = Image.new('RGBA', (size, 70 + int(size + 20 + fh*int(len(arr)/maxr))))
    draw = ImageDraw.Draw(img, 'RGBA')
        # set font file
    font = ImageFont.truetype(path + 'assets/arial.ttf', fs)

        # answers, ?, radius, seperation_lines_list
    s, n, r, lines = sum(arr), 0, int(size/2), []
        # roundRect(draw, (0, diameter + footer_distance/2, diameter, h - time_space), rad, (r, g, b, a))
    roundRect(draw, (0, size + 10, size, img.size[1] - 70), 15, (70, 70, 70, 150))
    
    for i in range(len(arr)):
            # random color
        col = (randint(100, 255), randint(100, 255), randint(100, 255))
            # ((intendation + diameter*coloumn/max_coloumns))
        draw.text((10 + size*(i%maxr)/maxr, size + 20 + fh*int(i/maxr)),
                    # [A-Z]: 0__.0%
                  chr(i + 65) + ': ' + format(100*arr[i]/s, '0.1f') + '%', col, font)

            # draw colored portion lines
        for n in range(n, n + int(d*arr[i]/s + 2)):
            draw.line((r, r, int(r + r*sin(2*pi*n/d)), int(r - r*cos(2*pi*n/d))), col, 2)
            continue

            # save seperation line coordinates
        lines.append((r, r, int(r + r*sin(2*pi*n/d)), int(r - r*cos(2*pi*n/d))))
        continue

        # draw seperation lines after main circle drawing because otherwise overdrawn
    for line in lines:
        draw.line(line, (0, 0, 0), 2)
        continue

        # save pie chart image
    img.save(path + 'Store/Cake.png')
    f = open(path + 'Store/Cake.png', 'rb')
    st = f.read()
    f.close()
        # return image file data
    return st

    # open new poll
def createPoll(chatID, userID, data):
    msg = toMsg(data).split('\n')

        # return if less than two possible responses given
    if len(msg) < 2:
        Message.sendMessage(chatID, 'A poll needs minimum two response possibilities!')
        return

        # inline keyboard
    keyboard = []

        # random pollID
    pollID = str(chatID) + str(randint(1000, 9999))

        # load and update polls
    Poll = Load('Poll', {})
    Poll[pollID] = newPoll(userID, msg[0][8:], msg[1:])

        # make summary text
    sumText = 'Poll summary:\n' + Poll[pollID]['question'] + '\n\n'
    for i in range(1, len(msg)):
        if i%2: keyboard.append([])
        
            # max two btns per row | newInBtn('answer', 'pollID|answer_index')
        keyboard[int(i/2) - 1].append(newInBtn(msg[i], str(pollID) + '|' + str(i)))
        
            # [A-Z]: answer \n\t chosen by 0 members
        sumText += chr(i + 65) + ': ' + msg[i] + '\n\tchosen by 0 members\n'
        continue

        # send question and inline keyboard
    Message.sendMessage(chatID, Poll[pollID]['question'], {'inline_keyboard':keyboard})
        # send summary
    s = Message.sendMessage(chatID, sumText)
        # save summaryID in poll dict
    Poll[pollID]['sumID'] = s['message_id']
    Save('Poll', Poll)
    return

    # cancel running poll
def cancelPoll(chatID, msg):
        # check for several errors
    error = 0
        # msg is not a reply to a msg
    if msg.get('reply_to_message') == None: error = 1
    else:
        # load polls
        Poll = Load('Poll', {})
        repID = msg['reply_to_message']['message_id']
        found = False
        
            # check each poll if summaryId is equal to replyID
        for poll in Poll.values():
            if poll['sumID'] == repID:
                found = True
                break
            elif not poll['active']: continue

            # poll is cancelled
        if not poll['active']: error = 2
            # replyID is no poll summary
        elif not found: error = 3
            # no votes
        elif not len(poll['replies']):
            error = 4
            # no superuser or creator of poll
        elif Load('User', {})[str(msg['from']['id'])]['id'] < 2:
            error = 5

        # return error message if required
    if error:
        Message.sendMessage(chatID, [
            'cancel poll as reply to the poll summary!',
            'poll already cancelled!',
            'this is no valid poll summary!',
            'can\'t cancel the poll because no user has voted yet!',
            'just the creator or a superuser can cancel this poll!'
            ][error - 1])
        return

        # build list with answer count
    cnt = []
    for rep in poll['answers']: cnt.append(0)
    for i in poll['replies'].values(): cnt[int(i) - 1] += 1

        # update poll status and save poll
    poll['active'] = False
    Save('Poll', Poll)

        # send pie chart
    Message.sendSticker(chatID, makeCake(cnt), 'Piechart.png')
    return
