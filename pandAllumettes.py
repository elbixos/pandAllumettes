from direct.showbase.ShowBase import ShowBase
from math import pi, sin, cos
from panda3d.core import TextNode
from direct.gui.OnscreenText import OnscreenText


import sys

class MyApp(ShowBase):
    def lineChoice(self, keyname):
        choixLigne = {"a" : 0, "z" : 1,"e" : 2,"r" : 3}
        if keyname in choixLigne:
            ligne = choixLigne[keyname]
            nbAl = self.plateau[ligne]
            self.plateau[ligne] -= 1

            node = self.noeudsPlateau[ligne].pop()
            node.removeNode()
            print(keyname)




    def __init__(self):
        ShowBase.__init__(self)

        self.plateau = [1,3,5,7]

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
                print (j)
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

        self.accept("escape", sys.exit)  # Escape quits

        base.buttonThrowers[0].node().setKeystrokeEvent('keystroke')
        self.accept('keystroke', self.lineChoice)

        self.instructions = \
            OnscreenText(text="chose line with a, z, e or r keys",
                         parent=base.a2dTopLeft, align=TextNode.ALeft,
                         pos=(0.05, -0.08), fg=(1, 1, 1, 1), scale=.06,
                         shadow=(0, 0, 0, 0.5))

        self.instructions2 = \
            OnscreenText(text="chose nb in 1, 2 or 3 keys",
                         parent=base.a2dTopLeft, align=TextNode.ALeft,
                         pos=(0.05, -0.16), fg=(1, 1, 1, 1), scale=.06,
                         shadow=(0, 0, 0, 0.5))

        self.disableMouse()
        camera.setPosHpr(0, -25, 15, 0, -45, 0)  # Place the camera

        base.oobe()

app = MyApp()


app.run()
