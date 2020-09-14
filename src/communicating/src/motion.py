#!/usr/bin/python
import rospy
import time
from std_msgs.msg import UInt8
from std_msgs.msg import Int32
from std_msgs.msg import String
	
toneData = 0
actionStand = 1
actionSit = 15
actionLook = 204
actionThankyou = 4
actionPushup = 126
actionYesgo = 23

#Subs Callback
def toneCallback(msg):	
	global toneData
	toneData = msg.data
	print("Callback")

#Program
def run():
	rospy.init_node('motion', anonymous=True)
	enablePub = rospy.Publisher("/robotis/enable_ctrl_module", String, queue_size=10)
	actionPub = rospy.Publisher("/robotis/action/page_num", Int32, queue_size=4)
	rospy.Subscriber("/toneDetector/received", UInt8, toneCallback)
	rate = rospy.Rate(50)
	time.sleep(1)
	
	enablePub.publish('action_module')
	time.sleep(0.1)
	
	print("RUN")
	
	global toneData
	
	while not rospy.is_shutdown():
		if toneData == 1:
			print("Sit")
			actionPub.publish(actionSit)
			time.sleep(2)
			toneData = 0
		elif toneData == 2:
			print("Look")
			actionPub.publish(actionLook)
			time.sleep(2)
			toneData = 0
		elif toneData == 3:
			print("Stand")
			actionPub.publish(actionStand)
			time.sleep(2)
			toneData = 0
		elif toneData == 4:
			print("Thank YOu")
			actionPub.publish(actionThankyou)
			time.sleep(2)
			toneData = 0
		elif toneData == 5:
			print("Push Up")
			actionPub.publish(actionPushup)
			time.sleep(2)
			toneData = 0
		elif toneData == 6:
			print("Yes Go")
			actionPub.publish(actionYesgo)
			time.sleep(2)
			toneData = 0					
		rate.sleep()
	
	
#Main 	
if __name__ == '__main__':
	try:
		run()
	except rospy.ROSInterruptException:
		pass
