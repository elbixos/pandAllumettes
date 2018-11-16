from direct.showbase.ShowBase import ShowBase
from math import pi, sin, cos
from panda3d.core import TextNode
from direct.gui.OnscreenText import OnscreenText


import sys

class MyApp(ShowBase):

    def compteAllumettes(self):
        sum = 0
        for i in self.plateau :
            sum+=i
        return sum

    def changePlayer(self):
        self.numJoueur = (self.numJoueur+1)%2
        self.title.setText("Player "+str(self.numJoueur+1))



    def removeAllumettes(self):
        # Remove if the user already chose a line and nbAl

        if (not self.ligne =="") and (not self.nbAl ==0) :
            ligne = self.ligne

            # remove matches from plateau
            self.plateau[ligne] -= self.nbAl

            # remove matches from the scene graph
            for i in range(self.nbAl):
                node = self.noeudsPlateau[ligne].pop()
                node.removeNode()

            self.ligne = ""
            self.nbAl = 0
            self.changePlayer()

            if self.compteAllumettes() == 0 :
                self.state = "gameOver"
                self.gameOver = \
                    OnscreenText(text="Player "+str(self.numJoueur+1)+ " Win !",
                                 fg=(1, 1, 1, 1), pos=(-0.1, 0.1), scale=.08,
                                 shadow=(0, 0, 0, 0.5))


    def chooseStrategy(self, keyname):
        choixLigne = {"a" : 0, "z" : 1,"e" : 2,"r" : 3}
        print (keyname)

        if keyname in choixLigne:
            self.ligne = choixLigne[keyname]
            print(keyname)

        nbAl = {"1" : 1, "2" : 2,"3" : 3}
        if keyname in nbAl :
            # note the user choice
            wantedNb = nbAl[keyname]

            # check if enough matches are on the line
            if wantedNb <= self.plateau[self.ligne]:
                self.nbAl = nbAl[keyname]

    def __init__(self):
        ShowBase.__init__(self)

        self.plateau = [1,3,5,7]
        self.ligne = ""
        self.ligne = 0
        self.numJoueur = 0

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

        self.accept("enter", self.removeAllumettes)  # Escape quits
        self.accept("escape", sys.exit)  # Escape quits

        base.buttonThrowers[0].node().setKeystrokeEvent('keystroke')
        self.accept('keystroke', self.chooseStrategy)

        # This code puts the standard title and instruction text on screen
        self.title = \
            OnscreenText(text="Player "+str(self.numJoueur+1),
                         parent=base.a2dBottomRight, align=TextNode.ARight,
                         fg=(1, 1, 1, 1), pos=(-0.1, 0.1), scale=.08,
                         shadow=(0, 0, 0, 0.5))

        self.instructions = \
            OnscreenText(text="choose line with a, z, e or r keys",
                         parent=base.a2dTopLeft, align=TextNode.ALeft,
                         pos=(0.05, -0.08), fg=(1, 1, 1, 1), scale=.06,
                         shadow=(0, 0, 0, 0.5))

        self.instructions2 = \
            OnscreenText(text="choose nb in 1, 2 or 3 keys",
                         parent=base.a2dTopLeft, align=TextNode.ALeft,
                         pos=(0.05, -0.16), fg=(1, 1, 1, 1), scale=.06,
                         shadow=(0, 0, 0, 0.5))

        self.instructions3 = \
            OnscreenText(text="validate with Enter",
                         parent=base.a2dTopLeft, align=TextNode.ALeft,
                         pos=(0.05, -0.24), fg=(1, 1, 1, 1), scale=.06,
                         shadow=(0, 0, 0, 0.5))



        self.disableMouse()
        camera.setPosHpr(0, -25, 15, 0, -40, 0)  # Place the camera

        #base.oobeCull()
        base.oobe()

app = MyApp()


app.run()
