"""
Created on Mon Jul 30 2018
Updated on Fri Jun 19 2020
@author:PMB 

NetLog0.8

"""

import os
import csv
import sys
import time
import numpy as np
import datetime as dt
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

system = os.uname()
print(system[1])

standard_time = int(time.strftime('%y%m%d%H%M'))
tme = time.strftime("%H:%M", time.localtime())
date = time.strftime("%b-%d", time.localtime())
unix_time = time.time()

def SpeedTester():
    try:
        import speedtest as sp
        res = sp.shell()
        dwn = round((res.download / 1000.0 / 1000.0), 2)
        up = round((res.upload / 1000.0 / 1000.0), 2)
        png = round(res.ping, 2)
        data = [unix_time, dwn, up, png, standard_time]
        return data
    except:
        data = [0,0,0,0,0]
        return data

def Writer(data,csv_path):
    if os.path.exists(csv_path):
        with open(csv_path,'a') as csv_path:
            csv_writer = csv.writer(csv_path, delimiter=',')
            csv_writer.writerow([data])
    else:
        with open(csv_path,'w') as csv_path:
            csv_writer = csv.writer(csv_path, delimiter=',')
            csv_writer.writerow([data])


def PasswordReader(password_file):
    try:
        with open(password_file,'r') as f:
            password = f.readline()
    except:
        password = "Not the password"
    return password


def Emailer(table_line):
    try:
        download = table_line[2]
        upload = table_line[3]
        ping = table_line[4]
        results_tuple = (download, upload, ping)

        email_sender = 'paulmcbrien99@gmail.com'
        email_receiver = 'paulmcbrien99@gmail.com'
        subject = "NetLog Warning"
        password = PasswordReader('password.txt')

        msg = MIMEMultipart()
        msg['From'] = email_sender
        msg['To'] = email_receiver
        msg['Subject'] = subject
        msg.attach
        body = ("Could not log to GSheets.\nDownload: {}\nUpload: {}".format(download,upload))
        msg.attach(MIMEText(body,'plain'))
        text = msg.as_string()

        server = smtplib.SMTP('smtp.gmail.com:587')
        server.starttls()
        server.login(email_sender,password)
        server.sendmail(email_sender,email_receiver,text)
        server.quit()
    except:
        print("Could not send email")


def GoogleSheetsLogger(data,json_path):
    '''Logs results to google sheets document'''
    #try:
    scope = ["https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(json_path,scope)
    client = gspread.authorize(creds)
    sheet = client.open('NetLog').sheet1
    sheet.append_row(data)
    print("Logged to Gsheet")
    print(data)
    #except:
    #    Emailer(data)


def main():

    if system[1] == 'paul-hplaptop15bw0xx':
        #directory for json gspread file
        json_path= '/home/pmcb99/Documents/Python/NetLog/creds.json'
        #directory to write xlsx info to csv
        csv_path = '/home/pmcb99/Documents/Python/NetLog/log.csv'
    else:
        #directory for json gspread file
        json_path= '/NetLog/creds.json'
        csv_path = '/NetLog/log.csv'
    currentResults = SpeedTester()
    Writer(currentResults,csv_path)
    GoogleSheetsLogger(currentResults,json_path)

main()
