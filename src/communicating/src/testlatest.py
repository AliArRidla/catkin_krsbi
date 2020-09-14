#!/usr/bin/python
import rospy
import pyaudio
import wave
import scipy
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
	
	
def func():
	#ROS Init
	rospy.init_node('toneDetector', anonymous=True)
	pub = rospy.Publisher("toneDetector/received", UInt8, queue_size=1)
		
	time.sleep(1)
		
	chunk = 2048  # Record in chunks of 1024 samples
	sample_format = pyaudio.paInt16  # 16 bits per sample
	channels = 1
	fs = 44100  # Record at 44100 samples per second
	seconds = 30
	lowcut = 5000.0
	highcut = 9000.0
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
		f1 = 8450
		f2 = 8520
		f3 = 7999
		f4 = 8020
		f5 = 8890
		f6 = 8910
		#print ("Nilai 5 Tertinggi :")
		#print (sorzmagf[:5])
		peaksf = []
		for j in range(1):
			#print ("Nilai rata-rata = ", np.average(zmagf))
			if sorzmagf[j] > 4:
				ind=np.where(zmagf==sorzmagf[j])
				peaksf.append(f[ind])
				peaksf[j] > np.average(zmagf)
				ind=np.where(zmagf==sorzmagf[j])
				peaksf.append(f[ind])
				#aa = peaksf[j]
				#pp = aa [0:3]
				#print (pp)
				if (peaksf[j] > f1) & (peaksf[j] < f2):
					if 1:
						print (peaksf[j]) 
						state = 1
						print ('kode 1 berdiri')
						pub.publish(1)
						time.sleep(0.1)
						data = 0
				elif (peaksf[j] > f3) & (peaksf[j] < f4):
					if 1:
						print (peaksf[j])
						state = 0
						print ('kode 2 duduk')
						pub.publish(2)
						time.sleep(0.1)
						data = 0
				elif (peaksf[j] > f5) & (peaksf[j] < f6):
					if 1:
						print (peaksf[j])
						state = 2
						print ('kode 3 Jongkok')
						pub.publish(3)
						time.sleep(0.1)
						data = 0
					#if (peaksf[j] < f4) & (peaksf[j] > f3) & state == 0:
					#	print (peaksf[j])
					#	state = 1
					#	print ('kode 2 duduk')
			else:
				peaksf.append(0.0)
			#print (peaksf[0:2])
			#print("Frekuensi peak terjadi")
			#print(peaksf[0])
	#	aw = []
	#	for g in range(5):
	#		if peaksf[g] >= 5997.94520548 <=6000.9999999 :
	#			aw.append(f[g])
	#		else:
	#			ae.append(0.0)
	#		print("Peaks terdeteksi", aw)
			#aa = peaksf
	#for s in range(5):
	#		#print ("Nilai rata-rata = ", np.average(zmagf))
	#		if aa[s] > np.average(zmagf) :
	#			ind=np.where(zmagf==sorzmagf[s])
	#			peaksf.append(f[ind])
	#			#print (np.where(f[aa]))	
	#			#print (aa)
	#		else:
	#			peaksf.append(0.0)
			#print (aa)
		
		#print(f)

	#pp = aa[0:2]
	#b = ('kode satu = Berdiri')
	#c = ('kode dua = Duduk')
	#f1 = 5900
	#f2 = 6050
	#print (pp)
	#for k in range(1):
	#	if  (pp[k] < f2) & (pp[k] > f1):
	#		print (b)
		#elif pp == 8000:
		#	print (c)
	#	else:
	#		print ('nothing')

		
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

		
