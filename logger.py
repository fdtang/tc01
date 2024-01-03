#!/usr/bin/env python3

'''
  Author: F. Tang
  Last Revision: May 11th, 2020
  Description:  Logging of ambient temperature and high-temperature K-type thermocouple

	Channel 1 : Ambient k-type temperature
 	Channel 2 : Open k-type thermocouple
	Channel 3 : Open k-type thermocouple
 	Channel 4 : Open k-type thermocouple
'''
import time
import random
from influx import InfluxDB


from daqhats import mcc134, HatIDs, HatError, TcTypes
from daqhats_utils import select_hat_device, tc_type_to_string

if __name__ == '__main__':

    ## You can generate a Token from the "Tokens Tab" in the UI
    starttime=time.time()
    influx = InfluxDB()
    try:
        address = select_hat_device(HatIDs.MCC_134)
        hat = mcc134(address)
        tc_type = TcTypes.TYPE_K   # change this to the desired thermocouple type
        delay_between_reads = 1  # Seconds
        channels = (0, 1, 2, 3)

        for channel in channels:
            hat.tc_type_write(channel, tc_type)

        while True:
            temperatures = {0: None, 1:None, 2: None, 3: None}

            for channel in channels:
                value = hat.t_in_read(channel)
                if value not in [mcc134.OPEN_TC_VALUE, mcc134.OVERRANGE_TC_VALUE,  mcc134.COMMON_MODE_TC_VALUE] :
                    temperatures[channel] = float(value)

            influx.send(temperatures)
            time.sleep(1 - (time.time() - starttime) % 1)

    except (HatError, ValueError) as error:
        print('\n', error)
