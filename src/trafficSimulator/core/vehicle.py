import uuid
import numpy as np
import random as rand


class Vehicle:
    def __init__(self, config={}):
        # Set default configuration
        self.set_default_config()

        # Update configuration
        for attr, val in config.items():
            setattr(self, attr, val)

        # Calculate properties
        self.init_properties()
        
    def set_default_config(self):    
        self.id = uuid.uuid4()
        self.w = 1.74
        self.l = 4
        self.s0 = 8
        self.T = 1
        self.v_max = 16.6
        self.OG_v_max = 16.6    
        self.a_max = 5
        self.b_max = 4.61
        self.time = 0
        self.path = []
        self.current_road_index = 0
        self.pedestrian = False
        self.colour = (0, 0, 225)

        self.x = 0
        self.v = 16.6
        self.a = 0
        self.stopped = False



    def init_properties(self):
        self.sqrt_ab = 2*np.sqrt(self.a_max*self.b_max)
        self._v_max = self.v_max
        self.OG_v_max = self.v_max

    def update(self, lead, dt):
        # Update position and velocity
        self.time += dt
        if self.v + self.a*dt < 0:
            self.x -= 1/2*self.v*self.v/self.a
            self.v = 0
        else:
            self.v += self.a*dt
            self.x += self.v*dt + self.a*dt*dt/2
        
        # Update acceleration
        alpha = 0
        if lead:
            delta_x = lead.x - self.x - lead.l
            delta_v = self.v - lead.v

            alpha = (self.s0 + max(0, self.T*self.v + delta_v*self.v/self.sqrt_ab)) / delta_x

        self.a = self.a_max * (1-(self.v/self.v_max)**4 - alpha**2)

        if self.stopped: 
            self.a = -3*self.b_max*self.v/self.v_max
            

    def stop(self):
        self.stopped = True

    def unstop(self):
        self.stopped = False


    def slow(self, v):
        self.v_max = v

    def setMax(self, v):
        self.v_max = v
        
    def unslow(self):
        self.v_max = self._v_max
    
    def getColour(self):
        return self.colour