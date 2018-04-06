#!/usr/bin/python3

import time
import speech_recognition as sr

watson_username="<username>"
watson_password="<password>"

r = sr.Recognizer()
m = sr.Microphone()

print("Calibrating for ambient noise ...")
with m as source:
 r.adjust_for_ambient_noise(source)  # calibrating

print("Testing speech recognition ...")
print('Hit Ctrl+C to exit.')

def callback(recognizer, audio):
	try:
		recog=recognizer.recognize_ibm(audio,username=watson_username,password=watson_password)
		print("Watson thinks you said: " + recog)
	except sr.UnknownValueError:
		print("Watson could not understand audio")
	except sr.RequestError as e:
		print("Could not request results from Watson; {0}".format(e))

stop_listening = r.listen_in_background(m, callback) # this function can be called to stop background listening.
