from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

class InfluxDB() : 
  '''
      Author: F. Tang
      Last Revision: August 17th, 2021
      Description: Send sound level
  '''
    
  def __init__(self) :
    
    influxClient = InfluxDBClient(url="http://winston.hiptec.no:8086", 
                                       token="4ScEnBn7HAd-bTb6-Z9lOX7tB_aN04kQiFh59LOLk8ASCBAoC0hjcsd6m4vRSHcOQMZoyh6MuDmlII4zHsUysA==",
                                       org="HIPtec")
    
    self.write_api = influxClient.write_api(write_options=SYNCHRONOUS)

  def send(self, temperature_body) : 
    '''
      Author: F. Tang
      Last Revision: July 7th, 2020
      Description: Send sound level data over to InfluxDB
    '''  
    p = Point("temperature").tag("box_id", "tc01")
              
    
    for temp_index in range(0, 4): 
      try:
        temperature = float(temperature_body[temp_index])):
        if temperature> -9998 :
          p = p.field(f"ch{temp_index}" , temperature)
      except:
        pass
          

    try:  
      if temperature_body:      
        self.write_api.write(bucket="production", record=p)
    except : 
      pass