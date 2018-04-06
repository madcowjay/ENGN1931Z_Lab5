#!/usr/bin/python3
# This script implements very simple voice control of a stepper motor.
# It uses IBM's Watson for speech recognition, a MotorHAT, and a stepper motor.

import time
import speech_recognition as sr
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor, Adafruit_StepperMotor
import atexit

mh = Adafruit_MotorHAT()

def turnOffMotors(): # recommended for auto-disabling motors on shutdown!
    mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)

atexit.register(turnOffMotors)

myStepper = mh.getStepper(200, 1)  # 200 steps/rev, motor port #1
myStepper.setSpeed(30)             # 30 RPM

def moveleft(): # move counterclockwise
    myStepper.step(100, Adafruit_MotorHAT.FORWARD,  Adafruit_MotorHAT.SINGLE)

def moveright(): # move clockwise
    myStepper.step(100, Adafruit_MotorHAT.BACKWARD,  Adafruit_MotorHAT.SINGLE)

watson_username="<username>"
watson_password="<password>"

r = sr.Recognizer()
m = sr.Microphone()

print("Calibrating for ambient noise ...")
with m as source:
 r.adjust_for_ambient_noise(source)  # calibrating

x=input("Press enter to begin controlling the motor.")
print("Say right and left to change the direction of rotation.")
print("Program will exit after two minutes")

def callback(recognizer, audio):
    try:
        recog=recognizer.recognize_ibm(audio,username=watson_username,password=watson_password)
        print("Recognized command: " + recog)
        if "left" in recog.lower(): moveleft()
        if "right" in recog.lower(): moveright()
    except sr.UnknownValueError:
        print("No audio recognized.")
    except sr.RequestError as e:
        print("Request problem: {0}".format(e))

# The following line initiates a background process that continually
# listens and controls the motor based on the recognized commands.
stop_listening = r.listen_in_background(m, callback,phrase_time_limit=4) # this function can be called to stop background listening.
time.sleep(120)
