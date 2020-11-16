

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

        self.keys_pressed = {} # example {key.A:[145124 sec,"modif"]}

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

        ## managers
        self.tman = g.TextureManager()
        self.sman = g.SpriteManager(self.batch)

        ## sprites


        ### PART III : labels / cursor => Seizes

        ## seizes
        self.sz_id = []
        self.seize = {}
        self.sz = 0

        self.anchor = (self.S[0]*0.5,self.S[1]*0.5)
        self.initial_pos = (-self.S[0]*0.25,self.S[1]*0.25)

        self.addSeize('megaseize',True)

        #self.seize[self.sz_id[self.sz]] = g.Seize('megaseize',group=self.group0,batch=self.batch,x=-self.S[0]*0.25,y=self.S[1]*0.25)

        ## cursor
        self.cursor = g.Cursor(self.sz_id[0],group=self.group10,batch=self.batch)

        ### PART IV : final launch

        ## launching the machine u know (launching gameloop)
        self.playing = True
        self.draww = True
        self.nb = 0

        pyglet.clock.schedule_interval(self.gameloop,0.0000000000001)
        pyglet.app.run()

    ### ONCE FUNCTIONS

    def addSeize(self,name='jeanluc',main=False,id=None):

        if id == None:
            id = get_id('sz')
        self.sz_id.append(id)
        x,y = self.initial_pos
        self.seize[id] = g.Seize(name,group=self.group0,batch=self.batch,x=x,y=y)
        if main:
            self.sz = len(self.seize) - 1

    def open_file(self,file):

        self.addSeize(file,True)

    def save_file(self,file,idsz=None):

        if idsz == None: # on sauvegarde le fichier en cours
            idsz = self.sz_id[self.sz]

        if 'saves' not in os.listdir(self.path):
            os.makedirs(self.path+'\\saves')

        with open(self.path+'\\saves\\'+file+'.txt','w') as f:
            f.write(self.seize[idsz].get_text())

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
                self.seize[self.sz_id[self.sz]].change(up_dic[symbol])
                self.keys_pressed[symbol] = [time.time(),"up"]

        else:
            if symbol in low_dic:
                self.seize[self.sz_id[self.sz]].change(low_dic[symbol])
                self.keys_pressed[symbol] = [time.time(),"low"]

        if symbol in motion_dic:
            self.seize[self.sz_id[self.sz]].motion(motion_dic[symbol])
            self.keys_pressed[symbol] = [time.time(),"motion"]
        elif symbol in modif_dic:
            self.seize[self.sz_id[self.sz]].modif(modif_dic[symbol])
            self.keys_pressed[symbol] = [time.time(),"modif"]

    def on_key_release(self,symbol,modifiers):

        if symbol in self.keys_pressed:
            del self.keys_pressed[symbol]

    def on_mouse_motion(self,x,y,dx,dy):

        self.M = [x,y]
        self.mouse_speed = module(dx,dy)

    def on_mouse_drag(self,x, y, dx, dy, buttons, modifiers):

        self.M = [x,y]
        self.mouse_speed = module(dx,dy)

        #print(dx,dy)

        self.seize[self.sz_id[self.sz]].movedx((dx,dy))

    ### EVENTS

    def events(self):

        if self.action == 'playing':
            print(self.M)

        delay_pressed = 0.4
        current_time = time.time()

        for key in self.keys_pressed:
            if current_time - self.keys_pressed[key][0] > delay_pressed:
                if self.keys_pressed[key][1] == "up":
                    self.seize[self.sz_id[self.sz]].change(up_dic[key])
                elif self.keys_pressed[key][1] == "low":
                    self.seize[self.sz_id[self.sz]].change(low_dic[key])
                elif self.keys_pressed[key][1] == "motion":
                    self.seize[self.sz_id[self.sz]].motion(motion_dic[key])
                elif self.keys_pressed[key][1] == "modif":
                    self.seize[self.sz_id[self.sz]].modif(modif_dic[key])


    ### GAMELOOP

    def draw(self):

        if self.draww:
            self.batch.draw()

    def refresh(self):

        if self.get_size() != self.S:
            for id in self.seize:
                self.seize[id].adapt_xy(self.S,self.get_size())
            self.S = self.get_size()

        self.anchor = self.S[0]*0.5,self.S[1]*0.5

        ### refresh seize
        for id in self.seize:
            self.seize[id].refresh(self.anchor)


        self.cursor.refresh(self.seize[self.cursor.sz],self.S,self.anchor)

    def gameloop(self,dt):

        pyglet.clock.tick()

        if self.nb == 0:

            self.label_fps = pyglet.text.Label('',font_name='arial',font_size=32,group=self.group10, \
                            batch=self.batch,color=(255,255,255,255),anchor_y='top')

        self.nb+=1
        self.label_fps.x,self.label_fps.y = 20,self.S[1] -20
        self.label_fps.text = 'FPS : '+str(int(pyglet.clock.get_fps()))

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

            self.save_file('test',self.sz_id[self.sz])

            print('\n\nNumber of lines :',compt(self.path))
            save_files(self.path)

            self.close()



"""###########################################################"""

def main():

    app = App()
    app.init()

if __name__ == '__main__':
    main()
