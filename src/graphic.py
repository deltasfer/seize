

import pyglet



### LABELS

class MyLabel(pyglet.text.Label):


    def __init__(self,text='', font_name=None, font_size=None, bold=False, italic=False, \
                    color=(255, 255, 255, 255), x=0, y=0, width=None, height=None, \
                    anchor_x='left', anchor_y='baseline', align='left', multiline=False, dpi=None, batch=None, group=None):

        super(MyLabel,self).__init__(text=text,font_name=font_name, font_size=font_size, bold=bold, italic=italic, \
                        color=color, x=x, y=y, width=width, height=height, \
                        anchor_x=anchor_x, anchor_y=anchor_y, align=align, multiline=multiline, dpi=dpi, batch=batch, group=group)


    def get_end(self,cursor):
        if cursor == 'end':
            cursor = len(self.text)
        return self.text[cursor:]

    def del_end(self,cursor):
        if cursor == 'end':
            cursor = len(self.text)
        self.text = self.text[:cursor]

    def change(self,cursor,char):

        text = self.text

        if cursor == 'end':
            cursor = len(text)

        self.text = text[:cursor] + char + text[cursor:]

    def modif(self,cursor,key):

        text = self.text

        if cursor == 'end':
            cursor = len(text)

        if key == 'back':
            if cursor != 0:
                self.text = text[:cursor-1] + text[cursor:]

### SEIZE

class Seize():

    def __init__(self,name, x=0, y=0, batch=None, group=None):

        self.name = name
        self.cursor = [0,"end"]

        self.x = x
        self.y = y
        self.padding = 10

        self.batch = batch
        self.group = group

        self.font_name={'normal':'arial','title':'arial','subtitle':'arial'}
        self.font_size={'normal':16,'title':32,'subtitle':24}

        self.cont = [MyLabel(font_name=self.font_name['normal'],font_size=self.font_size['normal'],color=(255,255,255,255), x=x, y=y, batch=self.batch, group=self.group)]
        self.summary = ['normal']

        #self.comment = [...]

    def motion(self,motion):

        if motion == 'right':
            if self.cursor[1] == -1:
                self.cursor[1] = 'end'
            elif self.cursor[1] != 'end':
                self.cursor[1]+=1
            else:
                final_line = self.cursor[0] != len(self.cont)-1
                self.motion('down')
                if final_line:
                    self.motion('begin')

        elif motion == 'left':
            endup = False
            if self.cursor[1] == 'end':
                if len(self.cont[self.cursor[0]].text) != 0:
                    self.cursor[1] = -1
                else:
                    endup = True
            elif self.cursor[1] != -len(self.cont[self.cursor[0]].text):
                self.cursor[1]-=1
            else:
                endup = True

            if endup:
                first_line = self.cursor[0] != 0
                self.motion('up')
                if first_line:
                    self.motion('end')

        elif motion == 'up':
            self.cursor[0] -= 1
            if self.cursor[0] < 0:
                self.cursor[0] = 0

        elif motion == 'down':
            self.cursor[0] += 1
            if self.cursor[0] >= len(self.cont):
                self.cursor[0] = len(self.cont) -1

        elif motion == 'begin':
            self.cursor[1]=-len(self.cont[self.cursor[0]].text)
            if self.cursor[1] == 0:
                self.cursor[1] = 'end'

        elif motion == 'end':
            self.cursor[1] = 'end'

    def modif(self,key):

        if key in ['back']:
            self.cont[self.cursor[0]].modif(self.cursor[1],key)

        elif key == 'enter':

            newtext = self.cont[self.cursor[0]].get_end(self.cursor[1])
            self.cont[self.cursor[0]].del_end(self.cursor[1])

            self.add_Lab(self.cursor[0]+1,newtext)
            self.motion('down')
            self.motion('begin')

    def change(self,char):
        self.cont[self.cursor[0]].change(self.cursor[1],char)

    def add_Lab(self,cursor,text='',style='normal'):

        y = self.y
        for i in range(cursor):
            y = y - self.font_size[self.summary[i]] - self.padding

        labs = self.cont
        self.cont = labs[:cursor] + [MyLabel(text=text,font_name=self.font_name[style],font_size=self.font_size[style], \
                            color=(255,255,255,255), x=self.x, y=y, batch=self.batch, group=self.group)] + labs[cursor:]

        self.summary = self.summary[:cursor] + [style] + self.summary[cursor:]

        for i in range(cursor+1,len(self.cont)):
            self.cont[i].y = self.cont[i].y - self.font_size[style] - self.padding

    def refresh(self):

        y = self.y
        #print(self.x,self.y)

        for i in range(len(self.cont)):
            self.cont[i].y = y
            self.cont[i].x = self.x
            y = y - self.font_size[self.summary[i]] - self.padding

    def move(self,pos):
        self.x,self.y = pos
        self.refresh()

    def movedx(self,vec):
        self.x,self.y = self.x+vec[0],self.y+vec[1]
        self.refresh()



"""
    ## littles functions


    def get_square(color=(255,255,255,255),size=(100,100)):

        img = pyglet.image.SolidColorImagePattern(color)
        return img.create_image(*size)
"""
