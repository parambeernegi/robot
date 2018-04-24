#!/usr/bin/env python
import rospy
import paho.mqtt.client as mqtt
from std_msgs.msg import String


a = 'x'

def on_connect(client, userdata, flags, rc):
	print("connectin")
	client.subscribe("command")
	print("connected")

def on_message(client, userdata, msg):
	global a 
	a=str(msg.payload.decode())
#	print (a)
	
	
client = mqtt.Client()
client.on_connect = on_connect
if __name__ =="__main__":
	rospy.init_node('Igen_talk',anonymous = True)
	pub = rospy.Publisher('/igen/move', String, queue_size = 1)
	rate = rospy.Rate(5)
	client=mqtt.Client()
	client.on_connect=on_connect
	client.on_message=on_message
	client.username_pw_set("wytntytd","Theu2ZvA4Rww")
	client.connect("m14.cloudmqtt.com",18822,60)
        client.loop_start()
	try:
		#client.on_connect = on_connect
		#client.on_message = on_message
		#client.username_pw_set("wytntytd", "Theu2ZvA4Rww")
		#client.connect("m14.cloudmqtt.com", 18822, 60)
		while not rospy.is_shutdown():
			#client.on_connect = on_connect
			client.on_message = on_message
			#client.username_pw_set("wytntytd","Theu2ZvA4Rww")
			#client.connect("m14.cloudmqtt.com",18822,60)
		  	rospy.loginfo(a)
			pub.publish(a)			
			rate.sleep()
           
	except rospy.ROSInterruptException:
		print "stopped"
