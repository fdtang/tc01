
from dt8852 import Dt8852
import serial 
import time
import datetime
from influx import InfluxDB


if __name__ == '__main__':
    
    influx = InfluxDB()
    # For Windows, try COM3 or COM4.
    sp=serial.Serial('/dev/ttyUSB0')

    # Instantiate object
    dt8852 = Dt8852(sp)
    # Sets modes: range 30dB - 80dB, slow, dB(C) and start recording.
    modes = [Dt8852.Range_mode.R_30_130_AUTO, 
             Dt8852.Time_weighting.FAST, 
             Dt8852.Frequency_weighting.DBA,\
             Dt8852.Recording_mode.RECORDING]
    dt8852.set_mode(modes)
    
    # Process incoming data from device until all modes have set.
    for _ in dt8852.decode_next_token():
        if len(modes) == 0:
            break
        
    for recordings in dt8852.get_recordings():
        kill = recordings
    
    previous_time = time.time() 
    while True:
        try:            
            for (token_type, sound_level, value_changed) in dt8852.decode_next_token():
                if (token_type == 'current_spl'):                              
                    if (time.time() - previous_time) > 1: 
                        influx.send(sound_level)   
                        previous_time = time.time()  
                        # date_str = datetime.datetime.now().strftime("%H:%M:%S")
                        # print(f"sound_level (dbA): {sound_level}, time: {date_str}")
        except:
            pass
                        
                                                    
                    
            
