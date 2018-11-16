from direct.showbase.ShowBase import ShowBase
from math import pi, sin, cos

class MyApp(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)

        plateau = [1,3,5,7]

        # Load the environment model.
        self.scene = self.loader.loadModel("models/environment")
        # Reparent the model to render.
        self.scene.reparentTo(self.render)
        # Apply scale and position transforms on the model.
        self.scene.setScale(0.25, 0.25, 0.25)
        self.scene.setPos(-8, 42, 0)

        for i in range(len(plateau)) :
            for j in range(plateau[i]) :
                print (j)
                self.jar = self.loader.loadModel("./assets/netted_jar.egg")
                self.jar.reparentTo(self.render)
                self.jar.setScale(0.5, 0.5, 0.5)
                self.jar.setPos(-5+j*2, -10+i*4, 0)

        self.disableMouse()
        camera.setPosHpr(0, -25, 15, 0, -45, 0)  # Place the camera

        base.oobe()

app = MyApp()


app.run()
