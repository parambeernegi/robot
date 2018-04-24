#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from robot import Ignisbot
import pigpio
from time import sleep

pi=pigpio.pi()

ignis=Ignisbot.Ignisbot('v1')

global xcount, a , prv_cmd, cmd
xcount=0
a=0
prv_cmd='x'

def set_cmd(msg):
    global xcount ,a, prv_cmd, cmd 

    rospy.loginfo(rospy.get_caller_id() + " I heard direction: %s ",msg.data)
   
    cmd=msg.data
    
    if (cmd == 'f' or cmd == 'b' or cmd == 'l' or cmd == 'r'):
      
       if (prv_cmd !='f' and cmd !='f'):

           if (prv_cmd !=cmd and a ==0):
               ignis.move_ramp_up(cmd)
               sleep(.1)          
               print "U"
               ignis.move1(cmd)
               print "M" 
               a=1
           elif (prv_cmd !=cmd and a ==1):
               ignis.move_ramp_down(prv_cmd)
               sleep(.1)
               print "D"
               ignis.stop()
               print "S"
               sleep(.8)
               if (prv_cmd !='x'):
                   ignis.move_ramp_up(cmd)
                   sleep(.1)
                   print "U"
                   ignis.move1(cmd)
                   print "M" 
           else:
               ignis.move1(cmd)   
               print "M"

       elif (prv_cmd =='f' or cmd == 'f'):
          
           if (prv_cmd !=cmd and a ==0):
               ignis.move_ramp_up(cmd)
               sleep(.1)
               print "U"
               ignis.move1(cmd)
               print "M"
               a=1
 
           elif (cmd == 'b' or prv_cmd =='x' and a ==1):
               ignis.move_ramp_down(prv_cmd)
               sleep(.1)
               print "D"
               ignis.stop()
               print "S" 
               sleep(.8)
               if (prv_cmd !='x'):
                   ignis.move_ramp_up(cmd)
                   sleep(.1)
                   print "U" 
                   ignis.move1(cmd)
                   print "M"
           else:
               ignis.move1(cmd)
               print "M"
       prv_cmd = cmd
       xcount=0
       print "prv_cmd",prv_cmd    
    elif cmd =='u' or cmd == 'd':
         ignis.tilt(cmd)     

    else:
         xcount=xcount+1 
         if xcount >1 and prv_cmd !='x':
             ignis.move_ramp_down(prv_cmd)
             sleep(.1)
             ignis.stop()   
             pi.stop()
             xcount=0
             prv_cmd = 'x'
             a=0
             print "x stop"   
                


def ignis_feed():
    rospy.init_node('Ignis_feed', anonymous=True)
    rospy.Subscriber("/ignis/move", String, set_cmd)
    rospy.spin()
   
if __name__=='__main__':
    try:
        ignis_feed()
    except rospy.ROSInterruptException:
        pass 
   
    finally:
        pi.stop()
