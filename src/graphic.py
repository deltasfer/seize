

import pyglet



### LABELS

class MyLabel(pyglet.text.Label):


    def __init__(self,text='', font_name=None, font_size=None, bold=False, italic=False, \
                    color=(255, 255, 255, 255), x=0, y=0, width=None, height=None, \
                    anchor_x='left', anchor_y='baseline', align='left', multiline=False, dpi=None, batch=None, group=None):

        super(MyLabel,self).__init__(text=text,font_name=font_name, font_size=font_size, bold=bold, italic=italic, \
                        color=color, x=x, y=y, width=width, height=height, \
                        anchor_x=anchor_x, anchor_y=anchor_y, align=align, multiline=multiline, dpi=dpi, batch=batch, group=group)

    def change(self,cursor,char):

        text = self.text

        if cursor == 'end':
            cursor = len(text)

        self.text = text[:cursor] + char + text[cursor:]


### SEIZE

class Seize():

    def __init__(self,name, x=0, y=0, batch=None, group=None):

        self.name = name
        self.cursor = [0,"end"]

        self.text = [MyLabel(font_name='arial',font_size=16,color=(0,0,0,255), x=x, y=y, batch=batch, group=group)]

        #self.comment = [...]

    def motion(self,motion):
        print('ouaiouai')

    def change(self,char):
        self.text[self.cursor[0]].change(self.cursor[1],char)





## littles functions


def get_square(color=(255,255,255,255),size=(100,100)):

    img = pyglet.image.SolidColorImagePattern(color)
    return img.create_image(*size)
