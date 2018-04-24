#/usr/bin/env python
import pigpio
from time import sleep 
import numpy as np
pi= pigpio.pi()

class servo(object):
    global currentPosition, targetPosition
    currentPosition= 0.4 
    def __init__(self, name, PIN=None):
          self.name=name
          self.PIN=PIN
          
          if self.name=="tilt":
               self.PIN=13
          pi.set_mode(self.PIN, pigpio.OUTPUT)
          pi.set_servo_pulsewidth(self.PIN, 1360)         

    def SetAngle(self,Lim):
         self.Lim=Lim
         MIN=600
         Range=1900
         
         if  Lim>1:
             Lim=1
         elif Lim<0:
              Lim=0

         angle = MIN + (Range*Lim)
         pi.set_servo_pulsewidth(self.PIN, int(angle))
 #        print "angle: ", angle

    def write(self,Lim):
        global currentPosition, targetPosition
        targetPosition = Lim
        r= targetPosition- currentPosition
        angles = np.array((range(190))[0::4])-90
        m= (np.sin(angles*np.pi/180.) +1)/2
 
        for mi in np.nditer(m):
            pos = currentPosition + mi*r
#            print "pos: ",pos
            self.SetAngle(pos)
            sleep(.004)
        currentPosition = targetPosition
        print "pos-e:", currentPosition
         
   

