
import RPi.GPIO as GPIO
import time
import dht11


from iota import Iota
from iota import ProposedTransaction
from iota import Address
from iota import Tag
from iota import TryteString

# define GPIO 14 as DHT11 data pin
Temp_sensor = 4

M_pin = 18  # select the pin for motionsensor
B_pin = 13  # select the pin for buzzer

SPICLK = 11
SPIMISO = 9
SPIMOSI = 10
SPICS = 8
mq2_dpin = 26
mq2_apin = 0

DO_pin = 17
AO_pin = 0  # flame sensor AO connected to ADC chanannel 0
# change these as desired - they're the pins connected from the
# SPI port on the ADC to the Cobbler

temp = int()
humi = int()
smoke = ""
flame = ""
motion = ""
arr = []


def main():
    # Main program block
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)

    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(M_pin, GPIO.IN)
    GPIO.setup(B_pin, GPIO.OUT)

    GPIO.setup(SPIMOSI, GPIO.OUT)
    GPIO.setup(SPIMISO, GPIO.IN)
    GPIO.setup(SPICLK, GPIO.OUT)

    GPIO.setup(SPICS, GPIO.OUT)
    GPIO.setup(mq2_dpin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    GPIO.setup(DO_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    pass


def buzzer(sensor):
    GPIO.output(B_pin, GPIO.LOW)
    time.sleep(0.5)
    GPIO.output(B_pin, GPIO.HIGH)
    time.sleep(0.5)
    GPIO.output(B_pin, GPIO.LOW)
    time.sleep(0.5)
    GPIO.output(B_pin, GPIO.HIGH)
    time.sleep(0.5)
    GPIO.output(B_pin, GPIO.LOW)
    time.sleep(0.5)
    GPIO.output(B_pin, GPIO.HIGH)
    time.sleep(0.5)


def dt11():
    instance = dht11.DHT11(pin=Temp_sensor)

    result = instance.read()
    temp = result.temperature
    humi = result.humidity
    #print("Temp = ", str(temp)+"\xb0C"," Humi = ",str(humi)+"%",time.sleep(1))
    return temp, humi


def smoke():
    if GPIO.input(mq2_dpin):
        smoke = 'Gas not Leak'
        # time.sleep(.5)
        #print("Gas not leak", time.sleep(.5))

    else:
        smoke = 'Gas Leakage'
        # time.sleep(.5)
        #print("Gas leakage", time.sleep(.5))
        # buzzer(mq2_dpin)
    return smoke


def flame():
    if GPIO.input(DO_pin) == False:
        flame = 'No Flame'
        #print("* Saft! *")
        # time.sleep(0.5)
    else:
        flame = 'Fire! Fire!!'
        #print("* Fire! *")
        # buzzer(DO_pin)
        # time.sleep(0.5)
    return flame


def detct():
    # for i in range(101):
    if GPIO.input(M_pin):
        motion = 'Someone is closing'
        #print ("Someone is closing!")
        # buzzer(M_pin)
    else:

        GPIO.output(B_pin, GPIO.HIGH)
        motion = 'Nobody Here'
        #print ("Nobody!")
        # time.sleep(2)

    t, h = dt11()

    s = smoke()
    f = flame()

    #data = 'Temp: ' + str(t) + '\xb0 | Humi: ' + str(h)+'% | Gas: ' + s+' | Flame: '+ f +' | Motion: ' + motion
    data = 'Temp: ' + str(t) + '  | Humi: ' + str(h) + '  | Gas: ' + \
        s + '  | Flame: ' + f + '  | Motion: ' + motion
    #data = 'abcd'

    api = Iota('https://nodes.devnet.iota.org:443', testnet=True)

#address = Address.random(81)
    address = Address(
        'YEQFOMPOTSQXIDGVULITXSXHQOSRLJIUZB9LKTXRHUM9IHYLWYXZTBMLBZRATRFPUVRVRMSYZPDRMWNMQCTGMTRGSZ')

######
######

    my_data = TryteString.from_unicode(data)


# Define a zero-value transaction object
# that sends the message to the address
    tx = ProposedTransaction(
        address=address,
        message=my_data,
        value=0
    )

    print('Attaching to IOTA')

    result = api.send_transfer(transfers=[tx])
    txn_hash = result['bundle'].tail_transaction.hash

    print('Attached')

    print('Transaction Hash:', txn_hash)
    # time.sleep(.5)

    print('Retriving from IOTA')

    bundle = api.get_bundles(txn_hash)
    message = bundle['bundles'][0].tail_transaction.signature_message_fragment

    output = message.decode()

    print('Message:', output)
    print('https://explorer.iota.org/devnet/address/'+str(address))
    exp = output.split(' ')

    if s == 'Gas Leakage' or f == 'Fire! Fire!!' or motion == 'Someone is closing':
        buzzer(True)
    #print('Temp:', t, (2 - len(str(t)))*' '+"\xb0C", '  Humi:', h, (2 - len(str(h)))*' '+"%", '  Smoke:', s, '  Flame:', f, '  Motion:', motion, time.sleep(.5))

# time.sleep(3)


def func(self):
    main()
    detct()
    GPIO.cleanup()
