#!/usr/bin/env python
from time import sleep
import pigpio

pi= pigpio.pi()

RESOLUTION= { 'Full': (0,0,0),
              'Half': (1,0,0),
              '1/4': (0,1,0),
              '1/8': (1,1,0),
              '1/16': (0,0,1),
              '1/32':(1,0,1) }


class stepper(object):
    "stepper object"
    def __init__(self,Name,DIR=None,STEP=None,Res=(1,0,1)):
        self.Name= Name
        self.Res= Res
        CW=1
        CCW=0
        STEP_PER_REVOLUTION= 200
        step_count = STEP_PER_REVOLUTION * 32
        if self.Name == "L":
            if DIR==None and STEP==None:
                self.DIR= 17
                self.STEP= 27
            else:
                self.DIR= DIR
                self.STEP= STEP
            self.MODE= [2,3,4]

        elif self.Name == "R":
            if DIR== None and STEP == None:
                self.DIR= 20
                self.STEP= 21
            else:
                self.DIR = DIR
                self.STEP = STEP
            self.MODE= [14,15,18]

        pi.set_mode(self.DIR,pigpio.OUTPUT)
        pi.set_mode(self.STEP,pigpio.OUTPUT)
        for i in range(3):
            pi.set_mode(self.MODE[i],1)
            pi.write(self.MODE[i],self.Res[i])

    def SetDir(self, Direction):
        if Direction=="CW":
             if self.Name == "L":
                  pi.write(self.DIR, 1)
             elif self.Name == "R":
                  pi.write(self.DIR, 0)

        elif Direction == "CCW":
             if self.Name == "L":
                  pi.write(self.DIR, 0)
             elif self.Name == "R":
                  pi.write(self.DIR, 1)

    def move(self,Direction):
        self.SetDir(Direction)           
        pi.set_PWM_dutycycle(self.STEP, 128)
        pi.set_PWM_frequency(self.STEP, 2000)

    def stop(self):
        pi.set_PWM_frequency(self.STEP, 0)
        pi.set_PWM_dutycycle(self.STEP, 0)
