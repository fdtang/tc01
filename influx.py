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

  def send(self, sound_level) : 
    '''
      Author: F. Tang
      Last Revision: July 7th, 2020
      Description: Send sound level data over to InfluxDB
    '''  
    p = Point("ambient").tag("location", "door").field("sound", sound_level)
              
    try:      
      self.write_api.write(bucket="production", record=p)
    except : 
      pass


    
    temperature_body = []
    if temperatures[0] is not None :
      temperature_body = [
        {"measurement": "temperature",
        "tags": {"host": "ambient"},
          "fields": {"value": round(temperatures[0], 2)}
        }]
    
    
    for tempIndex in range(1, 4):
      if temperatures[tempIndex] is not None :
        temperature_body.append({"measurement": "temperature_0" + str(tempIndex),
        "tags": {"host": "furnace"},
          "fields": {"value": round(temperatures[tempIndex], 2)}
        })
          
    try:  
      if temperature_body:      
        self.influxClient.write_points(temperature_body, retention_policy='develop')
    except : 
      pass