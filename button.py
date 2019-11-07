#!/usr/bin/env python
#
# This script sends a live stream to my youtube account
#
import RPi.GPIO as GPIO
import time
import subprocess
import os
import signal

GPIO.setmode(GPIO.BOARD)

led=35
button=33
GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Button
GPIO.setup(led, GPIO.OUT)        # LED

state=0

while True:
      # Wait for the button to be pushed without maxing out the CPU
      GPIO.wait_for_edge(button, GPIO.FALLING) 

      input_state=GPIO.input(button)
      if (state == 0 and input_state == False):
         print('Record')
         GPIO.output(led, GPIO.HIGH)
         time.sleep(1)
         p=subprocess.Popen(['sh', "/home/pi/code/lugstreamer/stream_low"], close_fds=True, preexec_fn=os.setsid)
         print(p.pid)
         state = 1
         
      elif (state == 1 and input_state == False):
         print('Cancel')
         GPIO.output(led, GPIO.LOW)
         time.sleep(1)
         print(p.pid)
         os.killpg(p.pid, signal.SIGUSR1)
         state = 0
      
