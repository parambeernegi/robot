#!/usr/bin/env python

import rospy
from std_msgs.msg import String
import sys, select, termios, tty

move = ['f', 'b', 'l', 'r', 'u', 's']
def getKey():
    tty.setraw(sys.stdin.fileno())
    rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
    if rlist:
        key = sys.stdin.read(1)
    else:
        key=''
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key


if __name__=="__main__":
    settings = termios.tcgetattr(sys.stdin)

    rospy.init_node('ignis_talk', anonymous= True)
    pub = rospy.Publisher('/ignis/move', String, queue_size=5)
  
    cmd=None
 
    try:  
        while(1):
            key = getKey()
            if key in move.key():
                cmd=key
                count=0
            elif key == ' ' or key == 'k':
                cmd=None
            else:
                count = count +1
                if count > 4:
                    cmd='x'
                if (key == '\x03'):
                    break
            pub.publish(cmd)
      #      print key
    except Exception as e:
        print e
 
    finally:
        cmd='x'
        pub.publish(cmd)

    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
