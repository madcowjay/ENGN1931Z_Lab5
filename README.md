# lab5
# Right and left

In this lab we take advantage of IBM's Watson Speech recognition API to voice-control a motor. Lab consists of three parts: setting up the motor, setting up the speech API, and putting them together. Two repos must be cloned, begin by cloning this one.

## Motor setup

The [Adafruit DC and Stepper Motor HAT](https://www.adafruit.com/product/2348) is an add-on that enables your RPi to drive up to 4 DC or 2 Stepper motors with pulse width modulation(PWM) speed control. There is a dedicated PWM driver chip onboard to control motor direction and speed. As the chip handles all the motor and speed controls over [I2C](https://en.wikipedia.org/wiki/I%C2%B2C) (Inter-Integrated Circuit), other I2C devices or HATs can be connected to the same pins. You can actually stack up to 32 such Motor HATS, to control 64 stepper motors and 128 DC motors. 

Before doing any hardware connections, configure and install software in the RPi.

+ Enable I2C on your Pi by starting a terminal and running:
```
sudo apt-get update
sudo apt-get install python-smbus
sudo apt-get install i2c-tools
```
+ Then run
```
sudo raspi-config
```
+ Now, go to *Interfacing Options* and enable I2C.

+ Install python-dev:
```
sudo apt-get install python-dev
```
+ Go to an appropriate location (ex. /home/pi/lab5), and run the following:
```
git clone https://github.com/adafruit/Adafruit-Motor-HAT-Python-Library.git
cd Adafruit-Motor-HAT-Python-Library
sudo python3 setup.py install
```

Now turn off your RPi, and place the MotorHAT on top. For this you'll need to take the RPi out of its case. Make sure that all the MotorHAT connections are secure. Connect the MotorHAT's power supply, and **after** that turn on your RPi.

Test the motor by running the script:
```
cd /home/pi/lab5/Adafruit-Motor-HAT-Python-Library/examples
sudo python3 StepperTest.py
```

Read and understand the above example's script to get a notion of how the motor is controlled. Write a script that makes the motor tick like an analog clock, no need for great precision.

I2C troubleshoot:
https://learn.adafruit.com/adafruits-raspberry-pi-lesson-4-gpio-setup/configuring-i2c

References:
https://learn.adafruit.com/adafruit-dc-and-stepper-motor-hat-for-raspberry-pi/overview

## Voice recognition

Connect the PlayStation Eye webcam and the speakers.

### Set up the audio and mic:

========== VERBATIM according to [Google](https://developers.google.com/assistant/sdk/guides/service/python/embed/audio) ============


1. Find your recording and playback devices.

a. Locate your USB microphone in the list of capture hardware devices. Write down the card number and device number.

```
arecord -l
```

b. Locate your speaker in the list of playback hardware devices. Write down the card number and device number. Note that the 3.5mm-jack is typically labeled Analog or bcm2835 ALSA (not bcm2835 IEC958/HDMI).
```
aplay -l
```

2. Create a new file named .asoundrc in the home directory (/home/pi). Make sure it has the right slave definitions for microphone and speaker; use the configuration below but replace <card number> and <device number> with the numbers you wrote down in the previous step. Do this for both pcm.mic and pcm.speaker.

```
cd
nano .asoundrc
```

```
pcm.!default {
  type asym
  capture.pcm "mic"
  playback.pcm "speaker"
}
pcm.mic {
  type plug
  slave {
    pcm "hw:1,0"
  }
}
pcm.speaker {
  type plug
  slave {
    pcm "hw:2,0"
  }
}
```

3. Verify that recording and playback work:

a. Adjust the playback volume.
```
alsamixer
```
Press the up arrow key to set the playback volume level to around 70.

b. Play a test sound (this will be a person speaking). Press Ctrl+C when done. If you don't hear anything when you run this, check your speaker connection.
```
speaker-test -t wav
```

c. Record a short audio clip.
```
arecord --format=S16_LE --duration=5 --rate=16000 --file-type=raw out.raw
```

d. Check the recording by replaying it. If you don't hear anything, you may need to check the recording volume in alsamixer.
```
aplay --format=S16_LE --rate=16000 out.raw
```
If recording and playback are working, then you are done configuring audio. If not, check that the microphone and speaker are properly connected. If this is not the issue, then try a different microphone or speaker.

========== END VERBATIM ==========

### Sign up for Watson

On your personal computer sign up to use the free version of [IBM Watson](https://console.bluemix.net/).

Verify your email account. Log in, and when on the [dashboard](https://console.bluemix.net/dashboard/apps/) click on *Create resource*. In the filter box, type "speech", click on the result "Speech To Text", give the service a name, and keep all default options. This will give you *100 minutes* per month of free speech recognition. On the left menu bar click on *Service credentials*, click on *New Credential*, give any name to it, click on *Add*, on the table of *Service credentials* look for your newly created credential and click on *View credentials*. Note down *username* and *password*.

On your RPi we now install a module that helps access many speech recognition services from within Python.

```
sudo pip install SpeechRecognition
pip install pyaudio
```

To test the voice recognition system, first edit the script `/lab5/test_watson.py`. In the fields <your username> and <your password>, put yours. Save and execute the script from within the terminal: `python3 test_watson.py`.

## Abracadabra

Finally run the script `abracadabra.py` to voice-control the motor by uttering either 'left' or 'right' following the prompts given by the script.


![Stepper.png](https://github.com/engn1931z/lab5/blob/master/IMG_2155.JPG?raw=true)
