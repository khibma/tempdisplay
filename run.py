
'''
pip3 install adafruit-circuitpython-dht
sudo apt-get install libgpiod2

sudo apt-get update
sudo apt-get install git build-essential python-dev python-smbus
git clone https://github.com/adafruit/Adafruit_Python_BMP.git
cd Adafruit_Python_BMP
sudo python setup.py install

pip3 install adafruit-circuitpython-ht16k33
'''
import time
import board
import adafruit_dht
import Adafruit_BMP.BMP085 as BMP085
from adafruit_ht16k33.segments import Seg7x4
 
i2c = board.I2C()
display = Seg7x4(i2c)
display.brightness = 0.5
display.blink_rate = 3

def display():
    '''
    to print text to the display, you just use the print function. For the 7-segment display, 
    valid characters are 0-9, letters A-F, a period, and a hyphen. So if we want to print ABCD,
     we would use the following:
    '''    

    display.print(1234)
    display.print("ABCD")

    display[0] = '1'
    display[1] = '2'
    display[2] = 'A'
    display[3] = 'B'


def dht22():
    # Initial the dht device, with data pin connected to:
    dhtDevice = adafruit_dht.DHT22(board.D18)

    # you can pass DHT22 use_pulseio=False if you wouldn't like to use pulseio.
    # This may be necessary on a Linux single board computer like the Raspberry Pi,
    # but it will not work in CircuitPython.
    # dhtDevice = adafruit_dht.DHT22(board.D18, use_pulseio=False)

    while True:
        try:
            # Print the values to the serial port
            temperature_c = dhtDevice.temperature
            temperature_f = temperature_c * (9 / 5) + 32
            humidity = dhtDevice.humidity
            print(
                "Temp: {:.1f} F / {:.1f} C    Humidity: {}% ".format(
                    temperature_f, temperature_c, humidity
                )
            )

        except RuntimeError as error:
            # Errors happen fairly often, DHT's are hard to read, just keep going
            print(error.args[0])
            time.sleep(2.0)
            continue
        except Exception as error:
            dhtDevice.exit()
            raise error

        time.sleep(2.0)


def bmp180():

    # Default constructor will pick a default I2C bus.
    #
    # For the Raspberry Pi this means you should hook up to the only exposed I2C bus
    # from the main GPIO header and the library will figure out the bus number based
    # on the Pi's revision.
    #
    # For the Beaglebone Black the library will assume bus 1 by default, which is
    # exposed with SCL = P9_19 and SDA = P9_20.
    sensor = BMP085.BMP085()

    # Optionally you can override the bus number:
    #sensor = BMP085.BMP085(busnum=2)

    # You can also optionally change the BMP085 mode to one of BMP085_ULTRALOWPOWER, 
    # BMP085_STANDARD, BMP085_HIGHRES, or BMP085_ULTRAHIGHRES.  See the BMP085
    # datasheet for more details on the meanings of each mode (accuracy and power
    # consumption are primarily the differences).  The default mode is STANDARD.
    #sensor = BMP085.BMP085(mode=BMP085.BMP085_ULTRAHIGHRES)

    print ('Temp = {0:0.2f} *C'.format(sensor.read_temperature()))
    print ('Pressure = {0:0.2f} Pa'.format(sensor.read_pressure()))
    print ('Altitude = {0:0.2f} m'.format(sensor.read_altitude()))
    print ('Sealevel Pressure = {0:0.2f} Pa'.format(sensor.read_sealevel_pressure()))


def run():

    bmp = BMP085.BMP085()
    dhtDevice = adafruit_dht.DHT22(board.D18)

    while True:

        tmp = bmp.read_temperature()
        print("bmp tmp: {}".format(tmp))
        display.print(tmp)
        time.sleep(1.5)

        temperature_c = dhtDevice.temperature
        temperature_f = temperature_c * (9 / 5) + 32
        humidity = dhtDevice.humidity
        time.sleep(1.5)
        print("dht humid: {}".format(humidity))
        display.print(humidity)
        time.sleep(1.5)
        print("dht temp: {}".format(temperature_c))
        display.print(temperature_c)
        time.sleep(1.5)

if __name__ == "__main__":
    run()
