from direct.showbase.ShowBase import ShowBase
from math import pi, sin, cos
from panda3d.core import TextNode
from direct.gui.OnscreenText import OnscreenText
from direct.actor.Actor import Actor


import sys

class MyApp(ShowBase):
    def camMove(self,move,value):
        if move =="forward" :
            self.moveCam["forward"]=value

        if move == "backward" :
            self.moveCam["backward"]=value

        if move =="left" :
            self.moveCam["left"]=value

        if move == "right" :
            self.moveCam["right"]=value


    def updateCam(self):
        #print (self.moveCam)
        if self.moveCam["forward"] == 1 :
            self.camera.setY(self.camera,0.5)

        if self.moveCam["backward"] == 1  :
            self.camera.setY(self.camera,-0.5)

        if self.moveCam["left"] == 1 :
            self.camera.setH(self.camera.getH()+1)

        if self.moveCam["right"] == 1 :
            self.camera.setH(self.camera.getH()-1)

    def compteAllumettes(self):
        sum = 0
        for i in self.plateau :
            sum+=i
        return sum

    def changePlayer(self):
        self.numJoueur = (self.numJoueur+1)%2
        self.title.setText("Player "+str(self.numJoueur+1))
        self.setPanda()

    def setPanda(self):
        if self.numJoueur ==  1 :
            self.pandaActor.setColorScale((0.6, 0.6, 1.0, 1.0))
        else :
            self.pandaActor.setColorScale((1.0, 0.1, 0.1, 1.0))

        self.pandaActor.setPos(-7,-10+self.ligne*4,0)


    def removeAllumettes(self):
        # Remove if the user already chose a line and nbAl
        ligne = self.ligne
        # remove matches from plateau
        self.plateau[ligne] -= self.nbAl

        # remove matches from the scene graph
        for i in range(self.nbAl):
            node = self.noeudsPlateau[ligne].pop()
            node.removeNode()

        #self.pandaActor.detachNode()
        self.nbAl = 0
        self.changePlayer()

        if self.compteAllumettes() == 0 :
            self.state = "gameOver"
            self.gameOver = \
                OnscreenText(text="Player "+str(self.numJoueur+1)+ " Win !",
                             fg=(1, 1, 1, 1), pos=(-0.1, 0.1), scale=.08,
                             shadow=(0, 0, 0, 0.5))


    def chooseStrategy(self, keyname):
        moveLigne = {"a" : 1, "q" : -1}
        print (keyname)

        if keyname in moveLigne:
            self.ligne +=moveLigne[keyname]
            if self.ligne <0 :
                self.ligne =0
            if self.ligne >3 :
                self.ligne =3

            self.setPanda()
            #self.pandaActor.reparentTo(self.render)
            print(keyname)

        nbAl = {"1" : 1, "2" : 2,"3" : 3}
        if keyname in nbAl :
            # note the user choice
            wantedNb = nbAl[keyname]

            # check if enough matches are on the line
            if wantedNb <= self.plateau[self.ligne]:
                self.nbAl = nbAl[keyname]
                self.removeAllumettes()

    def updateTask(self, task):
        self.updateCam()

        return task.cont

    def __init__(self):
        ShowBase.__init__(self)

        self.plateau = [1,3,5,7]
        self.ligne = 0
        self.nbAll = 0
        self.numJoueur = 0

        self.moveCam={}
        self.moveCam["forward"] = 0
        self.moveCam["backward"]= 0
        self.moveCam["left"]    = 0
        self.moveCam["right"]   = 0

        # Load the environment model.
        self.scene = self.loader.loadModel("models/environment")
        # Reparent the model to render.
        self.scene.reparentTo(self.render)
        # Apply scale and position transforms on the model.
        self.scene.setScale(0.25, 0.25, 0.25)
        self.scene.setPos(-8, 42, 0)


        self.noeudsPlateau = []

        for i in range(len(self.plateau)) :
            self.noeudsPlateau.append([])
            for j in range(self.plateau[i]) :
                #print (j)
                jar = self.loader.loadModel("./assets/netted_jar.egg")
                jar.reparentTo(self.render)
                jar.setScale(0.5, 0.5, 0.5)
                jar.setPos(-5+j*2, -10+i*4, 0)
                self.noeudsPlateau[i].append(jar)

        for i in range(3):
            for j in range (i+1) :
                self.barrier = self.loader.loadModel("assets/construction Barrier.egg")
                self.barrier.reparentTo(self.render)
                # Apply scale and position transforms on the model.
                self.barrier.setPos(-4+j*3.2, -8 + i*4, 0)
                self.barrier.setScale(0.5, 0.5, 0.5)
                self.barrier.setH( 90)

        #self.accept("enter", self.removeAllumettes)  # Escape quits
        self.accept("escape", sys.exit)  # Escape quits
        self.accept("arrow_up", self.camMove, ["forward",1])
        self.accept("arrow_down", self.camMove, ["backward",1])
        self.accept("arrow_left", self.camMove, ["left",1])
        self.accept("arrow_right", self.camMove, ["right",1])
        self.accept("arrow_up-up", self.camMove, ["forward",0])
        self.accept("arrow_down-up", self.camMove, ["backward",0])
        self.accept("arrow_left-up", self.camMove, ["left",0])
        self.accept("arrow_right-up", self.camMove, ["right",0])

        base.buttonThrowers[0].node().setKeystrokeEvent('keystroke')
        self.accept('keystroke', self.chooseStrategy)

        # This code puts the standard title and instruction text on screen
        self.title = \
            OnscreenText(text="Player "+str(self.numJoueur+1),
                         parent=base.a2dBottomRight, align=TextNode.ARight,
                         fg=(1, 1, 1, 1), pos=(-0.1, 0.1), scale=.08,
                         shadow=(0, 0, 0, 0.5))

        self.instructions = \
            OnscreenText(text="move panda with a or q",
                         parent=base.a2dTopLeft, align=TextNode.ALeft,
                         pos=(0.05, -0.08), fg=(1, 1, 1, 1), scale=.06,
                         shadow=(0, 0, 0, 0.5))

        self.instructions2 = \
            OnscreenText(text="select nb with 1, 2 or 3 ",
                         parent=base.a2dTopLeft, align=TextNode.ALeft,
                         pos=(0.05, -0.16), fg=(1, 1, 1, 1), scale=.06,
                         shadow=(0, 0, 0, 0.5))

        self.instructions3 = \
            OnscreenText(text="last removal lose the game",
                         parent=base.a2dTopLeft, align=TextNode.ALeft,
                         pos=(0.05, -0.24), fg=(1, 1, 1, 1), scale=.06,
                         shadow=(0, 0, 0, 0.5))

        self.pandaActor = Actor("models/panda-model",
                                {"walk": "models/panda-walk4"})
        self.pandaActor.setScale(0.002, 0.002, 0.002)
        self.pandaActor.setH(90)
        self.pandaActor.reparentTo(self.render)
        # Loop its animation.
        self.pandaActor.loop("walk")

        self.setPanda()

        #self.pandaActor.detachNode()


        self.disableMouse()
        camera.setPosHpr(0, -25, 15, 0, -40, 0)  # Place the camera

        self.taskMgr.add(self.updateTask, "update")

        #base.oobeCull()
        #base.oobe()

app = MyApp()


app.run()
