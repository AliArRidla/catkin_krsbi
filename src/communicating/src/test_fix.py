#!/usr/bin/python
import rospy
import pyaudio
import wave
from scipy.fftpack import fft
import struct
import scipy.signal
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter
from std_msgs.msg import UInt8
import time



def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a


def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y
    
def check_peaks(peaksf):
	f = [7000, 8000, 9000, 10000]
	for m in range(0,4):
		if(peaksf>(f[m]-20)) & (peaksf<(f[m]+20))	:
			fr=convtofreq(m)
			return fr
	return 0
				

def convtofreq(argument): 
    switcher = { 
        0: 7000, 
        1: 8000, 
        2: 9000,
        3: 10000
    } 
    fr=switcher.get(argument, 0)
    return fr
    
    
def func():
	#ROS Init
	rospy.init_node('toneDetector', anonymous=True)
	pub = rospy.Publisher("toneDetector/received", UInt8, queue_size=1)
		
	time.sleep(1)
    
	chunk = 2048  # Record in chunks of 1024 samples
	sample_format = pyaudio.paInt16  # 16 bits per sample
	channels = 1
	fs = 44100  # Record at 44100 samples per second
	seconds = 120
	lowcut = 5000.0
	highcut = 13000.0
	#filename = "hasiltest.wav"

	p = pyaudio.PyAudio()  # Create an interface to PortAudio

	print('Recording')

	stream = p.open(format=sample_format,
					channels=channels,
					rate=fs,
					frames_per_buffer=chunk,
					input=True)

	frames = []  # Initialize array to store frames
	state = 0
	# Store data in chunks for 3 seconds
	#for i in range(0, int(fs / chunk * seconds)):
	while not rospy.is_shutdown():
		data = stream.read(chunk)
		wf_data = struct.unpack(str(2 * chunk) + 'B', data)
		wf_data = np.array(wf_data, dtype='b')[::2] + 128    
		wf_data = butter_bandpass_filter(wf_data, lowcut, highcut, fs, order=6)
		yf = fft(np.array(wf_data, dtype='int16') - 128)
		x = np.arange(0, 2 * chunk, 2) 
		f = np.linspace(0, fs / 2, chunk / 2)
		l=len(x)
		magf= np.abs(2.0/l * np.abs(yf[:l//2]))
		zmagf=np.array(magf)
		zmagf[0]=0
		sorzmagf = np.sort(zmagf)[::-1]

		peaksf = []
		cd=[]
		for j in range(2):
			#print ("Nilai rata-rata = ", np.average(zmagf))
			if sorzmagf[j] > 4:
				ind=np.where(zmagf==sorzmagf[j])
				peaksf.append(f[ind])
				cp=check_peaks(peaksf[j])
				cd.append(cp)			
			else:
				peaksf.append(0.0)
		
			sorcd = np.sort(cd)
			print (sorcd)			
			if (len(sorcd)==2):	
				if (sorcd[0] == 7000) & (sorcd[1] == 8000):
					if state !=0:
						print (sorcd)
						state = 0
						print ('DUDUK')
						#pub.publish(1)
						time.sleep(0.1)
				elif (sorcd[0] == 7000) & (sorcd[1] == 9000):
					if state !=1:
						print (sorcd)
						state = 1
						print ('LOOK')
						#pub.publish(2)
						time.sleep(0.1)
				elif (sorcd[0] == 7000) & (sorcd[1] == 10000):
					if state !=2:
						print (sorcd)
						state = 2
						print ('BERDIRI')
						#pub.publish(3)
						time.sleep(0.1)
				elif (sorcd[0] == 8000) & (sorcd[1] == 9000):
					if state !=3:
						print (sorcd)
						state = 3
						print ('THANK YOU')
						#pub.publish(4)
						time.sleep(0.1)
				elif (sorcd[0] == 8000) & (sorcd[1] == 10000):
					if state !=4:
						print (sorcd)
						state = 4
						print ('PUSH UP')
						#pub.publish(5)
						time.sleep(0.1)
				elif (sorcd[0] == 9000) & (sorcd[1] == 10000):
					if state !=5:
						print (sorcd)
						state = 5
						print ('YES GO')
						#pub.publish(6)
						time.sleep(0.1)
			

	# Stop and close the stream 
	stream.stop_stream()
	stream.close()
	# Terminate the PortAudio interface
	p.terminate()
	print('Finished recording')

if __name__ == '__main__':
	try:
		func()
	except rospy.ROSInterruptException:
		pass
		