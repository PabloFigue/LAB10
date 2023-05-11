"""
'send_receive.py'
=========================================
Sends incrementing values to feeds and subscribes to them

Author(s): Brent Rubell, Todd Treece for Adafruit Industries
"""
# Import standard python modules
import sys
import time


# Import Adafruit IO REST client and MQTTClient
from Adafruit_IO import Client, Feed, MQTTClient

# Set to your Adafruit IO key and username.
ADAFRUIT_IO_KEY = "aio_rOLs319BUUrMzr87OICWzNTp8Zo1"
ADAFRUIT_IO_USERNAME = "PabloFig"

# Set the ID of the feeds to send and subscribe to for updates.
MOD_FEED_ID = "modificador"
CONT_FEED_ID = "contador"


# Create an instance of the REST client.
aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

# Create feeds if they don't exist
try:
    aio.feeds(MOD_FEED_ID)
except:
    feed = Feed(name=MOD_FEED_ID)
    aio.create_feed(feed)

try:
    aio.feeds(CONT_FEED_ID)
except:
    feed = Feed(name=CONT_FEED_ID)
    aio.create_feed(feed)
    
window = MainWindow()

# Variables to hold the count for the feeds
value_modificador = 0
value_contador = 0

# Define callback functions for the MQTT client.
def connected(client):
    print("Subscribing to Feed {0}".format(MOD_FEED_ID))
    client.subscribe(MOD_FEED_ID)
    print("Subscribing to Feed {0}".format(CONT_FEED_ID))
    client.subscribe(CONT_FEED_ID)
    print("Waiting for feed data...")
    

def disconnected(client):
    sys.exit(1)

def message(client, feed_id, payload):
    print("Feed {0} received new value: {1}".format(feed_id, payload))
    
# Create an MQTT client instance.
mqtt_client = MQTTClient(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

# Setup the callback functions defined above.
mqtt_client.on_connect = connected
mqtt_client.on_disconnect = disconnected
mqtt_client.on_message = message

# Connect to the Adafruit IO server.
mqtt_client.connect()

# Start the MQTT client's background thread to listen for messages.
mqtt_client.loop_background()

#Se toma una captura de valor que tiene el Modificador al iniciar el programa por si ya tenía un valor puesto
VERI_MOD_PREV = int(aio.receive(MOD_FEED_ID).value)

while True:
    
    #Se comprueba si hay algun cambio en el valor del Modificador
    veri_mod_act = int(aio.receive(MOD_FEED_ID).value)
    print("****** value modificador input: ", veri_mod_act)
    
    if veri_mod_act != VERI_MOD_PREV:
        value_modificador = veri_mod_act
        VERI_MOD_PREV = veri_mod_act
    
    value_contador = serial.data
    print("Sending contador status: ", value_contador)
    aio.send_data(CONT_FEED_ID, value_contador)

    # Adafruit IO is rate-limited for publishing,
    # so we'll need a delay for calls to aio.send_data()
    time.sleep(5)
