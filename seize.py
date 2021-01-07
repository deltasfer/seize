##  "seize" by deltasfer
##
##  more explanations on
##  https://github.com/deltasfer/seize

import pyglet,json
import pyglet.gl as gl
from pyglet.window import key
from src.utils import *
from src import graphic as g
from src.dic import *
import src.colors as c

FULLSCREEN = False

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__)) # fopatouché
if ' ' in CURRENT_PATH:
    print('Le chemin d\'acces contient un espace. Le programme va BUGUER SA MERE.')
    print('Changez le programme de place pour un path sans espace svp.')


"""###########################################################"""

class App():


    ### INIT FUNCTIONS

    def __init__(self):

        initial_size = 1000,800
        self.window = pyglet.window.Window(*initial_size,file_drops=True,resizable=True)
        self.window.push_handlers(self)

        self.icon = pyglet.resource.image("icon.ico")
        self.window.set_icon(self.icon)


        ## paths
        self.path = CURRENT_PATH
        self.config_path = '\\config\\'
        self.saves_path = '\\saves\\'


        ## size window

        self.style = 'normal'
        self.tmp_style = 'maximize'

        self.normal_size = initial_size
        self.window.set_minimum_size(275,200)


        ## screens
        display = pyglet.canvas.get_display()
        self.screens = display.get_screens()
        self.maximized_sizes = {}
        for scr in self.screens:
            self.maximized_sizes[scr] = 0,0

        self.S = self.window.get_size()

    def init(self):

        ### PART I : several thgs

        self.mode = 'showing'

        self.modes = ['showing','editing']

        """
        modes:
        -showing
        -editing
        """

        ## pending tasks
        #self.pending_tasks = []


        ## keys
        self.keys = key.KeyStateHandler()
        self.window.push_handlers(self.keys)

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
        self.group1 = pyglet.graphics.OrderedGroup(1)
        self.group5 = pyglet.graphics.OrderedGroup(5)
        self.group10 = pyglet.graphics.OrderedGroup(10)

        ## managers
        #self.tman = g.TextureManager()
        #self.sman = g.SpriteManager(self.batch)

        ## sprites


        ### PART III : labels / cursor => Seizes

        ## seizes
        self.sz_id = []
        self.seize = {}
        self.sz = 0

        self.anchor = (self.S[0]*0.5,self.S[1]*0.5)
        self.initial_pos = (-self.S[0]*0.25,self.S[1]*0.25)


        ### PART IV : buttons, ..

        self.buttons = {}
        self.buttons['save'] = g.Button(box(self.S[0]-100,self.S[1] -150,30,30),self.save_file,c.oldlace,c.blue,self.batch,group=self.group5)
        self.buttons['thg'] = g.Button(box(self.S[0]-100,self.S[1] -150,30,30),self.get_out,c.deepskyblue,c.blue,self.batch,group=self.group5)
        self.butbar = {}
        self.butbar['main'] = g.ButtonBar((0,0.8),self.S,[self.buttons['save'],self.buttons['thg']],align='right',batch=self.batch,group=self.group1,groupbutt=self.group5)

        self.open_config()
        #self.addSeize('megaseize',True)

        #self.seize[self.sz_id[self.sz]] = g.Seize('megaseize',group=self.group0,batch=self.batch,x=-self.S[0]*0.25,y=self.S[1]*0.25)

        ## cursor
        self.cursor = g.Cursor(group=self.group10,batch=self.batch)

        ### PART V : final launch

        ## launching the machine u know (launching gameloop)
        self.playing = True
        self.draww = True
        self.nb = 0
        pyglet.clock.schedule_interval(self.gameloop,0.0000000000001)

        if FULLSCREEN:
            self.change_size('borderless')

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

        x,y = self.window.get_location()
        for i in range(len(self.screens)):
            scr = self.screens[i]
            if (x >= scr.x and x <= scr.x + scr.width) and (y >= scr.y and y <= scr.y + scr.height):
                return scr
        return self.screens[0]

    def load_maximized_sizes(self):

        ## return the potential sizes of maximized window for each screen

        self.maximized_sizes = {}

        for screen in self.screens:

            windo = pyglet.window.Window(resizable=True,screen=screen,visible=False)
            #self.window.set_location(screen.x+1,screen.y+1)
            windo.maximize()
            #os.system('pause')
            self.maximized_sizes[screen] = windo.get_size()
            windo.close()

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

    def change_size(self,style='maximize'):

        if self.style != style:
            self.tmp_style = self.style

            if self.style == 'borderless':

                newwindow = pyglet.window.Window(file_drops=True,resizable=True)
                newwindow.push_handlers(self)
                newwindow.push_handlers(self.keys)
                self.window.close()
                self.window = newwindow
                self.window.set_icon(self.icon)

                ## size window
                self.window.set_minimum_size(275,200)
                self.style = style

                self.window.set_size(*self.normal_size)

                if style == 'maximize':
                    self.window.maximize()

            elif style == 'borderless':

                if self.style == 'normal':
                    self.normal_size = self.window.get_size()

                self.style = style


                old_pos = self.window.get_location()

                newwindow = pyglet.window.Window(file_drops=True,resizable=True,style=pyglet.window.Window.WINDOW_STYLE_BORDERLESS)
                newwindow.push_handlers(self)
                newwindow.push_handlers(self.keys)
                self.window.close()
                self.window = newwindow
                self.window.set_location(*old_pos)
                self.window.set_minimum_size(275,200)
                self.window.set_icon(self.icon)


                self.window.maximize()

            elif style == 'maximize' and self.style == 'normal':

                self.style = style
                self.window.maximize()

            elif style == 'normal' and self.style == 'maximize':
                self.window.set_size(*self.normal_size)
                self.style = style

    def get_out(self):
        self.playing = False


    #opening/saving
    def open_file(self,file,main=True):

        text = ''

        if self.saves_path[1:-1] not in os.listdir(self.path):
            os.makedirs(self.path + self.saves_path)

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

        #print(file + ' saved')
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

        ## controls globaux

        if symbol == key.ESCAPE:
            self.get_out()
            #self.playing = False

        elif symbol == key.F11:

            if self.style == 'borderless':
                self.change_size(self.tmp_style)
            else:
                self.change_size('borderless')

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


        for bar in self.butbar:
            if self.butbar[bar].visible :
                self.butbar[bar].check_mouse(x,y)

    def on_mouse_drag(self,x, y, dx, dy, buttons, modifiers):

        self.M = [x,y]
        self.mouse_speed = module(dx,dy)

        if self.mode == 'showing':
            hovers = []
            for bar in self.butbar:
                if self.butbar[bar].visible :
                    hovers = self.butbar[bar].get_hovers()
            if hovers == [] :
                self.seize[self.sz_id[self.sz]].movedx((dx,dy))
        else:
            for bar in self.butbar:
                if self.butbar[bar].visible :
                    self.butbar[bar].check_mouse(x,y)

    def on_mouse_press(self,x, y, button, modifiers):

        if button == pyglet.window.mouse.LEFT :
            for bar in self.butbar:
                if self.butbar[bar].visible :
                    self.butbar[bar].check_pressed()

    def on_mouse_release(self,x, y, button, modifiers):

        if button == pyglet.window.mouse.LEFT :
            for bar in self.butbar:
                if self.butbar[bar].visible :
                    self.butbar[bar].check_released()
                    self.butbar[bar].check_mouse(x,y)

    def on_close(self):

        self.save_config()

        print('\n\nNumber of lines :',compt(self.path))
        save_code(self.path)

    def on_resize(self,width,height):

        #print('ahhhh on me resuize',width,height,self.maximized_sizes[self.get_current_screen()])

        max_size = self.maximized_sizes[self.get_current_screen()]
        if (width,height) == self.maximized_sizes[self.get_current_screen()] and self.style != 'maximize' : #si la taille correspond à la taille de maximized
            #print('ouee')
            self.tmp_style = self.style
            self.style = 'maximize'

        elif width < max_size[0] and height < max_size[1] and self.style != 'normal' : #si la taille correspond à la taille de maximized
            self.tmp_style = self.style
            self.style = 'normal'
            self.normal_size = width,height

        elif self.style == 'normal':
            self.normal_size = width,height

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

        if self.window.get_size() != self.S:
            for id in self.seize:
                self.seize[id].adapt_xy(self.S,self.window.get_size())
            self.S = self.window.get_size()

        self.anchor = self.S[0]*0.5,self.S[1]*0.5

        ## buttons
        self.butbar["main"].update(self.S)

        ### refresh seize
        for id in self.seize:
            self.seize[id].refresh(self.anchor)

        self.cursor.refresh(self.seize[self.sz_id[self.sz]],self.S,self.anchor)

        #print(self.style,self.normal_size)


        ### PENDING TASKS

        """while len(self.pending_tasks) != 0 :
            if self.pending_tasks[0] != None:
                self.pending_tasks[0]()
            self.pending_tasks[1:]"""

    def gameloop(self,dt):

        pyglet.clock.tick()

        if self.nb == 0:

            self.label_fps = pyglet.text.Label('',font_name='arial',font_size=32,group=self.group10, \
                            batch=self.batch,color=(255,255,255,255),anchor_y='top')
            self.label_mode = pyglet.text.Label('',font_name='arial',font_size=8,group=self.group10, \
                            batch=self.batch,color=(255,255,255,255),anchor_y='top',anchor_x='right')

            self.load_maximized_sizes()
            print('screens initialised ->',self.maximized_sizes)

        self.nb+=1


        #print(self.playing)

        if self.playing:

            ### EVENTS
            self.events()

            gl.glClearColor(1/35,1/35,1/35,1)
            ### CLEAR
            self.window.clear()

            ### REFRESH
            self.refresh()

            ### DRAW
            self.draw()
            #print("aaaaaaah")


        else:

            self.on_close()
            self.window.close()



"""###########################################################"""

def main():

    app = App()
    app.init()

if __name__ == '__main__':
    main()
