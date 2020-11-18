

import pyglet,json
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

        super(App, self).__init__(file_drops=True,resizable=True,style=pyglet.window.Window.WINDOW_STYLE_BORDERLESS)


        ## paths
        self.path = CURRENT_PATH
        self.config_path = '\\config\\'
        self.saves_path = '\\saves\\'


        ## size window

        self.size_scr = 1000,800
        self.set_size(self.size_scr[0],self.size_scr[1])
        self.fscreen = False

        ## screens
        display = pyglet.canvas.get_display()
        self.screens = display.get_screens()
        used_screen = self.get_current_screen()
        self.size_fullscr = [used_screen.width,used_screen.height]
        self.S = self.get_size()

        self.maximize()

    def init(self):

        ### PART I : several thgs

        self.mode = 'showing'

        self.modes = ['showing','editing']

        """
        modes:
        -showing
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


        self.open_config()
        #self.addSeize('megaseize',True)

        #self.seize[self.sz_id[self.sz]] = g.Seize('megaseize',group=self.group0,batch=self.batch,x=-self.S[0]*0.25,y=self.S[1]*0.25)

        ## cursor
        self.cursor = g.Cursor(group=self.group10,batch=self.batch)

        ### PART IV : final launch

        ## launching the machine u know (launching gameloop)
        self.playing = True
        self.draww = True
        self.nb = 0

        pyglet.clock.schedule_interval(self.gameloop,0.0000000000001)
        pyglet.app.run()


    ### ONCE FUNCTIONS

    def addSeize(self,name='jeanluc',main=False,id=None,initial=''):

        if id == None:
            id = get_id('sz')
        self.sz_id.append(id)
        x,y = self.initial_pos
        self.seize[id] = g.Seize(name,id,group=self.group0,batch=self.batch,x=x,y=y,initial=initial)
        if main:
            self.sz = len(self.seize) - 1

    def get_current_screen(self):

        x,y = self.get_location()
        for i in range(len(self.screens)):
            scr = self.screens[i]
            if (x >= scr.x and x <= scr.x + scr.width) and (y >= scr.y and y <= scr.y + scr.height):
                return scr
        return self.screens[0]

    def change_mode(self,mode='editing'):

        if mode == 'editing':
            for id in self.seize:
                if id != self.sz_id[self.sz]:
                    self.seize[id].hide()
                else:
                    self.seize[id].hide(False)
        elif mode == 'showing':
            for id in self.seize:
                self.seize[id].hide(False)
        self.mode = mode

    def roll(self):
        self.sz += 1
        if self.sz >= len(self.sz_id):
            self.sz = 0
        if self.mode == 'editing':
            self.change_mode('editing')
        if len(self.sz_id) > 0:
            print('--'+self.seize[self.sz_id[self.sz]].name+' main--')


    #opening/saving
    def open_file(self,file,main=True):

        text = ''

        if file +'.txt' in os.listdir(self.path + self.saves_path):
            with open(self.path + self.saves_path + file +'.txt','r') as f:
                text = f.read()
            if text[-1] == '\n':
                text = text[:-1]

        self.addSeize(file,main,initial=text)

        print(file + ' opened')

    def close_file(self,id=None):

        if id == None: # on ferme le fichier en cours
            id = self.sz_id[self.sz]
        self.save_file(id)
        self.seize[id].delete()
        del self.seize[id]
        self.sz_id.remove(id)
        self.roll()

    def save_file(self,id=None):

        if id == None: # on sauvegarde le fichier en cours
            id = self.sz_id[self.sz]

        file=self.seize[id].name

        #print('')
        if self.saves_path[1:-1] not in os.listdir(self.path):
            os.makedirs(self.path+self.saves_path)

        with open(self.path+self.saves_path+file+'.txt','w') as f:
            f.write(self.seize[id].get_text())

        print(file + ' saved')

    def open_config(self):

        print('\n----------\n')

        if self.config_path[1:-1] not in os.listdir(self.path):
            os.makedirs(self.path + self.config_path)

        #self.configg= []

        if 'config' in os.listdir(self.path + self.config_path):

            print('opening config file')

            with open(self.path + self.config_path +'config','r') as f:
                try:
                    self.configg= json.load(f)
                except:
                    self.configg = []
        else:
            print('confing file lost in the nean...')
            self.configg = []

        if self.configg != []:
            for file in self.configg:
                name,main = file
                if name+'.txt' in os.listdir(self.path+self.saves_path):
                    self.open_file(name,main)
        else:
            self.open_file('megaseize')

        print('\n----------\n')

    def save_config(self):

        if self.config_path[1:-1] not in os.listdir(self.path):
            os.makedirs(self.path + self.config_path)

        self.update_config()
        for id in self.seize:
            self.save_file(id)

        with open(self.path + self.config_path +'config','w') as f:
            json.dump(self.configg,f)

        print('config file saved')
        print('\n----------\n')

    def update_config(self):

        if self.config_path[1:-1] not in os.listdir(self.path):
            os.makedirs(self.path + self.config_path)

        self.configg= []

        for id in self.seize:
            tab = [self.seize[id].name]
            if self.sz_id[self.sz] == id:
                tab.append(True)
            else:
                tab.append(False)
            self.configg.append(tab)


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
                self.set_size(*self.size_scr)
            else:
                self.size_scr = self.get_size()
                self.fscreen = True
                used_screen=self.get_current_screen()
                self.set_fullscreen(screen=used_screen)
                self.size_fullscr = [used_screen.width,used_screen.height]

        ## controls avec et sans modifieurs

        if self.keys[key.LCTRL]:

            if symbol == key.K:
                yeye,mode = 0,''
                for i in range(len(self.modes)):
                    if self.modes[i] == self.mode:
                        yeye = i
                if yeye +1 == len(self.modes):
                    mode = self.modes[0]
                else:
                    mode = self.modes[yeye+1]
                self.change_mode(mode)

            elif symbol == key.F:
                if self.label_fps.color[3] == 0:
                    self.label_fps.color = [*self.label_fps.color[:3],255]
                elif self.label_fps.color[3] == 255:
                    self.label_fps.color = [*self.label_fps.color[:3],0]

            elif symbol == key.N:
                self.open_file(input('new file name :'))

            elif symbol == key.TAB:
                self.roll()

            elif symbol == key.S:
                self.save_file()

            elif symbol == key.W:
                self.close_file()

        else:

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


        # label fps
        self.label_fps.text = 'FPS : '+str(int(pyglet.clock.get_fps()))
        self.label_fps.x,self.label_fps.y = 20,self.S[1] -20

        # label mode
        self.label_mode.text = self.mode
        self.label_mode.x,self.label_mode.y = self.S[0]-10,self.S[1] -10

    ### GAMELOOP

    def draw(self):

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


        self.cursor.refresh(self.seize[self.sz_id[self.sz]],self.S,self.anchor)

    def gameloop(self,dt):

        pyglet.clock.tick()

        if self.nb == 0:

            self.label_fps = pyglet.text.Label('',font_name='arial',font_size=32,group=self.group10, \
                            batch=self.batch,color=(255,255,255,255),anchor_y='top')
            self.label_mode = pyglet.text.Label('',font_name='arial',font_size=8,group=self.group10, \
                            batch=self.batch,color=(255,255,255,255),anchor_y='top',anchor_x='right')

        self.nb+=1


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

            self.save_config()

            print('\n\nNumber of lines :',compt(self.path))
            save_files(self.path)

            self.close()



"""###########################################################"""

def main():

    app = App()
    app.init()

if __name__ == '__main__':
    main()
