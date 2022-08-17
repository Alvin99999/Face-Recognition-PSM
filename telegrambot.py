import telepot
from time import *
from PIL import Image 
import RPi.GPIO as GPIO

RELAY = 17
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(RELAY, GPIO.OUT) #set up GPIO output channel
GPIO.output(RELAY,GPIO.LOW)

def opendoor(RELAY):
        GPIO.output(RELAY,GPIO.HIGH)
        print("Door Unlocked! Enter within 5 seconds!")
        sleep(5)
        GPIO.output(RELAY,GPIO.LOW)
        return 


def handle(msg):
    chat_id = msg['chat']['id']
    command = msg['text']

    print ('Command ' + command + ' from chat id' + str(id))

    if command == 'open' or 'Open':
       bot.sendMessage(chat_id, opendoor(RELAY))
    

bot = telepot.Bot('YOUR TOKEN')
bot.message_loop(handle)
print ('I am listening...')

#while 1:
    #sleep(5)
