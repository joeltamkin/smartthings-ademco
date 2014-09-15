#!/usr/bin/env python
/**
 *  Ademco RESTful interface for use with corresponding SmartThings app
 *  Requires AD2USB module for interface to ademco system
 *  Tested with Ademco Safewatch 3000 pro 
 *
 *  Author: Joel Tamkin
 *  Date: 2014-04-16
 */
 
import time
from alarmdecoder import AlarmDecoder
from alarmdecoder.messages import Message
from alarmdecoder.devices import USBDevice
import urllib2

import logging
lgr = logging.getLogger('ademco')
lgr.setLevel(logging.DEBUG)
fh = logging.FileHandler('ademco.log')
fh.setLevel(logging.WARNING)
frmt = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(frmt)
lgr.addHandler(fh)



myDevices = {'0232638' : "Back Door",
	'0039154' : "Media Motion",
        '0019290' : "Family Motion",
        '0218176' : "Front Door",
        '0721918' : "Garage Door",
        '0117882' : "Loft Smoke"}

STBASEURL = 'https://graph.api.smartthings.com/api/smartapps/installations/'
STAPPGUID = 'insert-your-guid-here'
STAPPTOKEN = '?access_token=insert-your-access-token-here'
APIBASEURL = STBASEURL + STAPPGUID

lastmessage = Message()

def main():
    """
    Example application that watches for an event from a specific RF device.

    This feature allows you to watch for events from RF devices if you have
    an RF receiver.  This is useful in the case of internal sensors, which
    don't emit a FAULT if the sensor is tripped and the panel is armed STAY.
    It also will monitor sensors that aren't configured.

    NOTE: You must have an RF receiver installed and enabled in your panel
          for RFX messages to be seen.
    """
    
    try:
        # Retrieve the first USB device
        device = AlarmDecoder(USBDevice.find())

        # Set up an event handler and open the device
        device.on_rfx_message += handle_rfx
	device.on_message += handle_message
        with device.open():
            while True:
                time.sleep(1)

    except Exception, ex:
        lgr.warn('Exception:' + str(ex))


def handle_rfx(sender, message):
    """
    Handles RF message events from the AlarmDecoder.
    """
    try:
    # Check for our target serial number and loop
    #if message.serial_number == RF_DEVICE_SERIAL_NUMBER and message.loop[0] == True:

        global myDevices
        if message.serial_number in myDevices.keys():

	    lgr.warn(str(myDevices[message.serial_number]) + 'triggered value ' + str(message.value))
	
	    url = APIBASEURL + '/rfx/'+ str(message.serial_number) + '/' + str(message.value) + STAPPTOKEN
	    lgr.warn(url)
	
 	    try:
		rsp = urllib2.urlopen(url).read()
		lgr.info("Sent message, response")
	    except:
		rsp = None
		lgr.error(url)
		lgr.error("API error?")
		return 0
        else:
	    lgr.warn("Unknown Sensor" + str(message.serial_number) + 'triggered value' + str(message.value))
    except:
        lgr.error("handle_rfx crashed") 

def handle_message(sender, message):
    """
    Handles message events from the AlarmDecoder.
    """
    pass
    """
    global lastmessage
    try:
      #print "message received:",message.raw
      #if (message.ready != lastmessage.ready) or \
      if (message.armed_away != lastmessage.armed_away) or \
	(message.armed_home != lastmessage.armed_home) or \
	(message.alarm_event_occurred != lastmessage.alarm_event_occurred) or \
	(message.alarm_sounding != lastmessage.alarm_sounding) or \
	(message.fire_alarm != lastmessage.fire_alarm) or \
	(message.ac_power != lastmessage.ac_power) or \
	(message.battery_low != lastmessage.battery_low):

	params = [ message.ready, \
		message.armed_away, \
		message.armed_home, \
		message.alarm_event_occurred, \
		message.alarm_sounding, \
		message.fire_alarm, \
		message.ac_power, \
		message.battery_low ]

	url = APIBASEURL + '/panel/' + ''.join(['1' if x else '0' for x in params]) + STAPPTOKEN
	try:
		rsp = urllib2.urlopen(url).read()
                print "Sent message"
		lgr.info("Sent message, response")
		lastmessage = message
        except:
                lgr.warn(url)
                lgr.warn("API error?")
      else:
	#duplicate state
	pass
    except:
	lgr.error("massive fail")
	return 0
    """
if __name__ == '__main__':
    while 1:
	try:
		main()
		lgr.warn("main returned???")
    	except:
		lgr.error("main() crashed!")
		
