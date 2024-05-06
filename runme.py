#Import Area
from datetime import datetime
import os
import glob
import time 
import MySQLdb




 
# These tow lines mount the device:
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
 
base_dir = '/sys/bus/w1/devices/'
# Get all the filenames begin with 28 in the path base_dir.
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'
def read_rom():
    name_file=device_folder+'/name'
    f = open(name_file,'r')
    return f.readline()
 
def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines
 
def read_temp():
    lines = read_temp_raw()
    # Analyze if the last 3 characters are 'YES'.
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    # Find the index of 't=' in a string.
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        # Read the temperature .
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c, temp_f


    






#Database connections
mydb=MySQLdb.connect(
    host="#",
    user="#",
    password="#",
    database="#"
)   
    
mycursor=mydb.cursor()





print(' rom: '+ read_rom())
while True:
    
    
    #This set verible x as the tempature output in c
   #These IDs are unique to probe itself , this will be differant for yours as all are uniqe=. See sys/bus/W1/devices
    Tempature1=int((open('/sys/bus/w1/devices/28-3ce10457cfdd/temperature').read()))
    


    
    #sql statment

    sql="INSERT INTO `Brod` (`ID`,`Tempature`,`date and time`) VALUES(NULL,%s,%s);"
    
    L=datetime.now()
    val=(Tempature1,L)
    print(' C=%3.3f  F=%3.3f'% read_temp())
    p=str(Tempature1)
    mycursor.execute(sql,val)
    mydb.commit()
    time.sleep(3600)

    
    




# close the file
