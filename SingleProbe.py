import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Import other necessary libraries
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

# Temperature reading

# These two lines mount the device:
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
# Get all the filenames beginning with 28 in the path base_dir.
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

def read_rom():
    name_file = device_folder + '/name'
    with open(name_file, 'r') as f:
        return f.readline().strip()

def read_temp_raw():
    with open(device_file, 'r') as f:
        lines = f.readlines()
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
        # Read the temperature.
        temp_string = lines[1][equals_pos + 2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c, temp_f

########################################################

# Database connections
mydb = mysql.connector.connect(
    host="plesk.remote.ac",
    user="ws330240_Projects",
    password="M0nday08#",
    database="ws330240_AandR"
)

mycursor = mydb.cursor()

# Function to send email
def send_email(subject, body, to_email):
    from_email = "your-email@example.com"
    from_password = "your-email-password"
    
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, from_password)
        text = msg.as_string()
        server.sendmail(from_email, to_email, text)
        server.quit()
        print("Email sent successfully")
    except Exception as e:
        print(f"Failed to send email: {e}")

print('ROM: ' + read_rom())

# Read and print initial temperature
initial_temp_c, initial_temp_f = read_temp()
print(f'Initial temperature: C={initial_temp_c:.3f}  F={initial_temp_f:.3f}')

while True:
    
    
    temp_c, temp_f = read_temp()
    
    # SQL statement
    sql = "INSERT INTO `Brod` (`ID`,`Tempature`,`date and time`) VALUES(NULL,%s,%s);"
    current_time = datetime.now()  # inserts current datetime into database (database value needs to be set to datetime)
    val = (temp_c, current_time)
    
    if temp_c < -5:  # This is the threshold to which the temperature should be
        print(f'C={temp_c:.3f}  F={temp_f:.3f}')
        mycursor.execute(sql, val)
        mydb.commit()
        print("Temperature successfully appended to the database.")
        time.sleep(3600)  # writes temp every 3600 seconds (1 hour)
    else:
        print("Warning: temperature too high!")
        send_email(
            subject="Temperature Alert",
            body=f"The temperature has exceeded the threshold! Current temperature is {temp_c:.2f}°C.",
            to_email="tech@purnhousefarm.co.uk"
        )
        mycursor.execute(sql, val)
        mydb.commit()
        time.sleep(3600)  # writes temp every 3600 seconds (1 hour)
    
    # Continue logging even if the temperature exceeds the threshold
    print("Continuing to log temperatures...")

