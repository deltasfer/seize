

from src.utils import *
import src.colors as c
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

    def get_width(self,cursor):

        if cursor == 'end':
            if self.text == '':
                return 0
            return self.content_width
        elif cursor <= -len(self.text):
            return 0
        else:
            old = self.text
            self.del_end(cursor)
            w = self.content_width
            self.text = old
            return w

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

    def get_xy(self):
        return self.x,self.y

### SEIZE

class Seize():

    # init

    def __init__(self,name,id, x=0, y=0, batch=None, group=None,initial=''):

        self.name = name
        self.cursor = [0,"end"]

        self.id = id

        self.x = x
        self.y = y
        self.padding = 10

        self.batch = batch
        self.group = group

        self.font_name={'normal':'arial','title':'arial','subtitle':'arial'}
        self.font_size={'normal':16,'title':32,'subtitle':24}

        self.cont = []
        self.summary = []

        if initial == '':
            self.cont = [MyLabel(font_name=self.font_name['normal'],font_size=self.font_size['normal'],color=(255,255,255,255), x=x, y=y, batch=self.batch, group=self.group)]
            self.summary = ['normal']
        else:
            self.load_text(initial)

        #self.comment = [...]

    # main fonctions

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
            else:
                cur = self.convert_cursor_end_to_beg(self.cursor[0]+1,self.cursor[1])
                self.cursor[1] = self.convert_cursor_beg_to_end(self.cursor[0],cur)
                if self.cursor[1] >= 0:
                    self.cursor[1] = 'end'

                """if self.cursor[1] < -len(self.cont[self.cursor[0]].text):
                    self.motion('begin')"""

        elif motion == 'down':

            self.cursor[0] += 1
            if self.cursor[0] >= len(self.cont):
                self.cursor[0] = len(self.cont) -1
            else:
                cur = self.convert_cursor_end_to_beg(self.cursor[0]-1,self.cursor[1])
                self.cursor[1] = self.convert_cursor_beg_to_end(self.cursor[0],cur)
                if self.cursor[1] >= 0:
                    self.cursor[1] = 'end'
                """if self.cursor[1] < -len(self.cont[self.cursor[0]].text):
                    self.motion('begin')"""

        elif motion == 'begin':
            self.cursor[1]=-len(self.cont[self.cursor[0]].text)
            if self.cursor[1] == 0:
                self.cursor[1] = 'end'

        elif motion == 'end':
            self.cursor[1] = 'end'

    def modif(self,key):

        if key in ['back']:
            if self.convert_cursor_end_to_beg(*self.cursor) > 0:
                self.cont[self.cursor[0]].modif(self.cursor[1],key)
            elif self.cursor[0] != 0:
                if self.len_seize() == 0 :
                    self.cont[self.cursor[0]].delete()
                    self.cont = self.cont[:self.cursor[0]] + self.cont[self.cursor[0]+1:]
                    self.cursor = [self.cursor[0]-1,'end']
                else:
                    self.change(self.cont[self.cursor[0]].text,(self.cursor[0]-1,'end'))
                    self.cont[self.cursor[0]].delete()
                    self.cont = self.cont[:self.cursor[0]] + self.cont[self.cursor[0]+1:]
                    self.cursor[0]-=1

        elif key == 'enter':

            newtext = self.cont[self.cursor[0]].get_end(self.cursor[1])
            self.cont[self.cursor[0]].del_end(self.cursor[1])

            self.add_Lab(self.cursor[0]+1,newtext)
            self.motion('down')
            self.motion('begin')

        elif key == 'delete':
            if self.cursor != [len(self.cont)-1,'end']:
                self.motion('right')
                self.modif('back')

    def change(self,char,cur=None):
        if cur == None:
            self.cont[self.cursor[0]].change(self.cursor[1],char)
        else:
            self.cont[cur[0]].change(cur[1],char)

    # one time fonctions

    def load_text(self,text=''):

        text = text.split('\n')
        for i in range(len(text)):
            self.load_line(text[i],i)

    def load_line(self,line='',cursor=0):

        ## là on mettra les séparations pour mettre en gras, italique, etc..
        self.add_Lab(cursor,line)

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

    def move(self,pos):
        self.x,self.y = pos
        self.refresh()

    def movedx(self,vec):
        self.x,self.y = self.x+vec[0],self.y+vec[1]
        self.refresh()

    def adapt_xy(self,oldS,S):
        self.x *= S[0]/oldS[0]
        self.y *= S[1]/oldS[1]


    # refresh

    def hide(self,hide=True):

        for lab in self.cont:
            if hide and (lab.color[3] != 0):
                lab.color = [*lab.color[:3],0]
            elif (not hide)  and (lab.color[3] == 0):
                lab.color = [*lab.color[:3],255]


    def refresh(self,anchor=(0,0)):

        y = self.y + anchor[1]
        #print(self.x,self.y)

        for i in range(len(self.cont)):
            self.cont[i].y = y
            self.cont[i].x = self.x + anchor[0]
            y = y - self.font_size[self.summary[i]] - self.padding

    # getters

    def convert_cursor_end_to_beg(self,line,cur):
        if cur == 'end':
            cur = 0
        return len(self.cont[line].text) + cur

    def convert_cursor_beg_to_end(self,line,cur):
        if cur == 'end':
            cur = 0
        return -len(self.cont[line].text) + cur

    def len_seize(self):
        return len(self.cont[self.cursor[0]].text)

    def get_text(self):

        full_text = ''
        for lab in self.cont:
            full_text += lab.text+'\n'
        #print(full_text)
        return full_text

    # byebye functions

    def delete(self):
        for lab in self.cont:
            lab.delete()


### CURSOR

class Cursor(pyglet.sprite.Sprite):

    def __init__(self,x=0,y=0,group=None,batch=None):

        tman = TextureManager()
        text = tman.add_Texture(1,1)

        super(Cursor,self).__init__(text,x,y,batch=batch,group=group)

        self.cmd = pyglet.text.Label('',font_name='arial',font_size=16,group=group, \
                        batch=batch,color=(255,255,255,255),anchor_y='top')

    def refresh(self,seize,S,anchor=(0,0)):

        self.cmd_refresh(seize,S)
        self.update(scale_x=2,scale_y=seize.font_size[seize.summary[seize.cursor[0]]])

        y = seize.y + anchor[1]
        #print(seize.x,seize.y)

        for i in range(seize.cursor[0]):
            y = y - seize.font_size[seize.summary[i]] - seize.padding
        self.y = y

        self.x = seize.x + anchor[0] + seize.cont[seize.cursor[0]].get_width(seize.cursor[1])

    def cmd_refresh(self,seize,S):

        self.cmd.x,self.cmd.y = 20,S[1] -60
        self.cmd.text = 'cursor '+str(seize.name)+' : '+str(seize.cursor)


### SPRITES, FILTERS, ...

class TextureManager():

    def __init__(self):

        self.textures = []

    def add_Texture(self,w,h,color=(255,255,255,255)):

        pattern = pyglet.image.SolidColorImagePattern(color)
        return pattern.create_image(w,h)

class SpriteManager():

    def __init__(self,batch=None):

        self.sprites = []
        self.batch= batch

    def add_Spr(self,text,x,y,group=None):

        return pyglet.sprite.Sprite(text,x,y,batch=self.batch,group=group)

tman = TextureManager()
#sman = SpriteManager()

### BUTTONS ...

class Button():

    def __init__(self,box,function,color=(255,255,255,0),hover=(255,255,255,50),batch=None,group=None):

        if type(box) == type(()):
            self.box = box(box)
        else:
            self.box = box

        self.function = function
        self.hover = False
        self.visible = True

        self.col = color
        self.col_hover = hover

        self.img = tman.add_Texture(*box.wh,color)
        self.img_hover = tman.add_Texture(*box.wh,hover)

        self.skin = pyglet.sprite.Sprite(self.img,*self.box.xy,batch=batch,group=group)

    def iamhere(self):

        if not self.hover:
            self.hover = True
            self.skin.image = self.img_hover

    def nothere(self):

        if self.hover:
            self.hover = False
            self.skin.image = self.img

    def update(self,x,y):

        if x != self.skin.x:
            self.skin.x = x
        if y != self.skin.y:
            self.skin.y = y

    def _set_xy(self,pos):
        self.skin.x,self.skin.y = pos

    def _xy(self):
        return self.skin.x,self.skin.y

    def _h(self):
        return self.box.h

    def _w(self):
        return self.box.w

    xy = property(_xy,_set_xy)
    h = property(_h)
    w = property(_w)

class ButtonBar():

    def __init__(self,xy,S,buttons,style="w",padding = 50,sec_padding=10,align="right",color=c.air,batch=None,group=None,groupbutt=None):

        self.xy = xy # in percent
        self.butt = buttons
        self.padd = padding
        self.sec_padd = sec_padding
        self.align = align
        self.col = color

        self.batch = batch
        self.groupbutt = groupbutt

        self.img = tman.add_Texture(1,1,color)
        x,y = self.xy[0]*S[0],self.xy[1]*S[1]
        self.skin = pyglet.sprite.Sprite(self.img,x,y,batch=batch,group=group)

        self.style = style
        if self.style == "w":
            self.wh = S[0],0
        else:
            self.wh = 0,S[1]

        self.check_butt_size()

        self.update(S)

    def check_butt_size(self):

        if self.style == "w":
            for butt in self.butt:
                if butt.h > self.wh[1]:
                    self.wh = self.wh[0],butt.h
        else:
            for butt in self.butt:
                if butt.w > self.wh[0]:
                    self.wh = self.w,butt.wh[1]

    def update(self,S):

        #self.check_butt_size()

        if self.xy[0]*S[0] != self.skin.x:
            self.skin.x = self.xy[0]*S[0]
        if self.xy[1]*S[1] != self.skin.y:
            self.skin.y = self.xy[1]*S[1]

        if self.style == "w":
            self.skin.update(scale_x=S[0],scale_y=self.wh[1]+2*self.sec_padd)
            y = self.xy[1]*S[1]+self.sec_padd
            if self.align == "right":
                x = S[0] - self.padd
                dx = -1
            else:
                x = self.padd
                dx = 1

            for butt in self.butt:
                butt.update(x,y)
                x += dx*(butt.w+self.padd)
        else:
            self.skin.update(scale_x=self.wh[0]+2*self.sec_padd,scale_y=S[1])
            x = self.xy[0]*S[0]+self.sec_padd
            if self.align == "top":
                y = S[1] - self.padd
                dy = -1
            else:
                y = self.padd
                dy = 1

            for butt in self.butt:
                butt.update(x,y)
                y += dy*(butt.h+self.padd)
