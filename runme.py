#Importts area
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import numpy as np
from datetime import datetime
import os
import glob
import time
import tkinter as tk
import csv
import mysql.connector

############################################

#Tempature reading
 
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

########################################################
    
#Database connections
mydb=mysql.connector.connect(
    host="#",
    user="#",
    password="#",
    database="#"
)     
    
mycursor=mydb.cursor()




print(' rom: '+ read_rom())
while True:
    
    time.sleep(3600)#writes temp every 3600 seconds ( 1hour )
        
    #sql statment
    sql="INSERT INTO `Fridgetemp` (`Tempature`,`date and time`) VALUES(%s,%s);"
    L=datetime.now()#inserts current datetime into database ( databsase value needs to be set to datetime)
    val=(x,L)
    
    
 

     
    if(x<30000):#This is the threshhold to which the tempature should be 
        print(' C=%3.3f  F=%3.3f'% read_temp())
        p=str(x)

        mycursor.execute(sql,val)
        mydb.commit()
    else:
        
        print("Warning tempature to high !!!!!!")
        break



#https://github.com/AidanThomas1234
