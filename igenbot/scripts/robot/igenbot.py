#!/usr/bin/env python
from time import sleep
import pigpio
from motor import stepper
from motor import servo
pi= pigpio.pi()


 #    dir    w_r   w_l 
Move={ 'f' :('CW','CW',.4),
       'b' :('CCW','CCW',.4),
       'l' :('CCW', 'CW',0.05 ),
       'r' :('CW', 'CCW',0.05),
       'u' :0.02,
       'd' :-0.02}



class Igenbot(object):

    global val
    val=0.4
 
    def __init__(self,name):
        self.name=name
        self.wheel_left=stepper.stepper('L')
        self.wheel_right=stepper.stepper('R')
        self.Servo_tilt=servo.servo('tilt')

# tilt motion for servo head movement
    def tilt(self,cmd):
        self.cmd=cmd
        global val 
        val= val+Move[self.cmd]
        self.Servo_tilt.write(val)

# Ramp generation for stepper motor
    def generate_ramp(self,ramp):
        """Generate ramp wave forms.
        ramp:  List of [Frequency, Steps]    """
        pi.wave_clear()     # clear existing waves
        length = len(ramp)  # number of ramp levels
        wid = [-1] * length

        # Generate a wave per ramp level
        for i in range(length):
            frequency = ramp[i][0]
            micros = int(500000 / frequency)
            wf = []
            wf.append(pigpio.pulse(1 << self.wheel_left.STEP, 0, micros))  # pulse on
            wf.append(pigpio.pulse(1 << self.wheel_right.STEP,0, micros))
            wf.append(pigpio.pulse(0, 1 << self.wheel_left.STEP, micros))  # pulse off
            wf.append(pigpio.pulse(0, 1 << self.wheel_right.STEP, micros))
            pi.wave_add_generic(wf)
            wid[i] = pi.wave_create()

        # Generate a chain of waves
        chain = []
        for i in range(length):
            steps = ramp[i][1]
            x = steps & 255
            y = steps >> 8
            chain += [255, 0, wid[i], 255, 1, x, y]

        pi.wave_chain(chain)  # Transmit chain.

     
    def move_ramp_up(self,dir):
        self.SetDirection(dir)
        self.generate_ramp([[320, 15],[400, 20],[500, 25],[800, 40],[1000,55],[1600,75],[2000,100]])

    def move_ramp_down(self,dir):
        self.SetDirection(dir)
        self.generate_ramp([[2000,100],[1600,75],[1000,55],[800, 40],[500, 25],[400,20],[320, 15]])

    def SetDirection(self,dir):
        self.dir=dir
        self.wheel_right.SetDir(Move[self.dir][0])
        self.wheel_left.SetDir(Move[self.dir][1])


    def move(self,dir):
        self.SetDirection(dir)
        self.generate_ramp([[4000, int(10000*Move[self.dir][2])]])

    def stop(self):
        self.wheel_right.stop()
        self.wheel_left.stop()  
        
    def move1(self,dir):
        self.SetDirection(dir)
        self.wheel_left.move(Move[self.dir][1])
        self.wheel_right.move(Move[self.dir][0])

    def move_degree(self,angle,dir):
        self.angle=angle         
        # 360 degree rotate at 2000 frequency with 150mm wheel space
        # total move 471 = 2*7.5*3.14 mm
        # no of wheel rotation = 471/345.4
        # total pulse in 360 = 6400*1.36
        # postion es= 360/8704=0.041
        required_step= angle*8704/360
        self.SetDirection(dir)
        self.generate_ramp([2000, required_step])
        self.move_ramp_dowm()

    
    def move_distance(self,distance_In_mm,dir):
        self.distance_In_mm = distance_In_mm
        # 360 degreee move at 2000 frequency with 6400 count
        # robot tyre size is 110 mm dia
        # so 345.4 mm move in 6400 step
        #  1mm move in 6400/345.4
        required_step= distance_In_mm * 6400/ 345.4
        self.SetDirection(dir)  
        self.move_ramp_up()
        self.generate_ramp([2000, required_step])
        self.move_ramp_down()




