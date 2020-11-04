

import pyglet
import pyglet.gl as gl
from pyglet.window import key
from src.utils import *
from src import graphic as g
from src.dic import *


CURRENT_PATH = os.path.dirname(os.path.abspath(__file__)) # fopatouché
if ' ' in CURRENT_PATH:
    print('Le chemin d\'acces contient un espace. Le programme va BUGUER SA MERE.')
    print('Changez le programme de place pour un path sans espace svp.')


"""###########################################################"""

class App(pyglet.window.Window):


    ### INIT FUNCTIONS

    def __init__(self):

        super(App, self).__init__()

        self.path = CURRENT_PATH

        self.size_scr = 1000,800
        self.set_size(self.size_scr[0],self.size_scr[1])

        self.fscreen = False

        ## screens
        display = pyglet.canvas.get_display()
        self.screens = display.get_screens()
        used_screen = self.get_current_screen()
        self.size_fullscr = [used_screen.width,used_screen.height]
        self.S = self.get_size()

    def init(self):

        ### PART I : several thgs

        self.action = 'editing'

        """
        actions:
        -editing
        """


        ## keys
        self.keys = key.KeyStateHandler()
        self.push_handlers(self.keys)

        ## mouse
        self.R,self.L = False,False
        self.M = [0,0]


        ### PART II : sprites etc

        ## dics, batch / group
        self.textures = {}
        self.sprites = {}

        self.batch = pyglet.graphics.Batch()

        self.group_10 = pyglet.graphics.OrderedGroup(-10)
        self.group0 = pyglet.graphics.OrderedGroup(0)
        self.group10 = pyglet.graphics.OrderedGroup(10)


        ### PART III : labels / cursor => Seizes

        self.seize = g.Seize('megaseize',group=self.group0,batch=self.batch,x=self.S[0]/2,y=self.S[1]/2)

        ### PART IV : final launch

        ## launching the machine u know (launching gameloop)
        self.playing = True
        self.draww = True
        self.nb = 0

        pyglet.clock.schedule_interval(self.gameloop,0.0000000000001)
        pyglet.app.run()

    def get_current_screen(self):

        x,y = self.get_location()
        for i in range(len(self.screens)):
            scr = self.screens[i]
            if (x >= scr.x and x <= scr.x + scr.width) and (y >= scr.y and y <= scr.y + scr.height):
                return scr
        return self.screens[0]

    ### PYGLET EVENTS

    def on_key_press(self,symbol,modifiers):

        #print(symbol)

        ## controls globaux

        if symbol == key.ESCAPE:
            self.playing = False

        elif symbol == key.F11:
            #print(self.fscreen)
            if self.fscreen:
                self.fscreen = False
                self.set_fullscreen(False)
                self.set_size(self.size_scr[0],self.size_scr[1])
            else:
                self.fscreen = True
                used_screen=self.get_current_screen()
                self.set_fullscreen(screen=used_screen)
                self.size_fullscr = [used_screen.width,used_screen.height]

        ## controls avec et sans modifieurs

        if self.keys[key.LCTRL]:

            if symbol == key.K:
                self.draww = not self.draww

            elif symbol == key.F:
                if self.label_fps.color[3] == 0:
                    self.label_fps.color = [*self.label_fps.color[:3],255]
                elif self.label_fps.color[3] == 255:
                    self.label_fps.color = [*self.label_fps.color[:3],0]

        if self.keys[key.LSHIFT]:

            if symbol in up_dic:
                self.seize.change(up_dic[symbol])

        else:

            if symbol in low_dic:
                self.seize.change(low_dic[symbol])

        if symbol in motion_dic:
            self.seize.motion(motion_dic[symbol])
        elif symbol in modif_dic:
            self.seize.modif(modif_dic[symbol])

    def on_mouse_motion(self,x,y,dx,dy):

        self.M = [x,y]
        self.mouse_speed = module(dx,dy)

    def on_mouse_drag(self,x, y, dx, dy, buttons, modifiers):

        self.M = [x,y]
        self.mouse_speed = module(dx,dy)

        #print(dx,dy)

        self.seize.movedx((dx,dy))

    ### EVENTS

    def events(self):

        if self.action == 'playing':
            print(self.M)

    """def on_my_resize(self):
        self.S = self.get_size()
        print("tamer")"""

    ### GAMELOOP

    def draw(self):

        if self.draww:
            self.batch.draw()

    def refresh(self):

        self.S = self.get_size()

        ### refresh seize
        #self.seize.move((self.S[0]/2,self.S[1]/2))
        self.seize.refresh()


    def gameloop(self,dt):

        pyglet.clock.tick()

        if self.nb == 0:

            self.label_fps = pyglet.text.Label('',font_name='arial',font_size=32,group=self.group10, \
                            batch=self.batch,color=(255,255,255,255),anchor_y='top')


            self.cursor = pyglet.text.Label('',font_name='arial',font_size=16,group=self.group10, \
                            batch=self.batch,color=(255,255,255,255),anchor_y='top')

        self.nb+=1
        self.label_fps.x,self.label_fps.y = 20,self.S[1] -20
        self.label_fps.text = 'FPS : '+str(int(pyglet.clock.get_fps()))

        self.cursor.x,self.cursor.y = 20,self.S[1] -60
        self.cursor.text = 'cursor '+str(self.seize.name)+' : '+str(self.seize.cursor)

        #print(self.S)

        if self.playing:

            ### EVENTS
            self.events()

            gl.glClearColor(1/35,1/35,1/35,1)
            ### CLEAR
            self.clear()

            ### REFRESH
            self.refresh()

            ### DRAW
            self.draw()


        else:
            print('\n\nNumber of lines :',compt(self.path))
            save_files(self.path)

            self.close()



"""###########################################################"""

def main():

    app = App()
    app.init()

if __name__ == '__main__':
    main()
