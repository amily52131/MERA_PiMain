"""
Created by Anahi Garnelo (https://github.com/agarnelo)
modified by Ying Fang Lee
original function name is JSONHTTPRequest.py

methods:
jRequest(dID)
	Takes dispenser id to retrieve update from server
	returns a JSON string of updates
	
SQLUpdate
	takes a json string and updates it into database

update the sqliteDB to the path 
"""

import json
import datetime
import requests
import string
import sqlite3
import os

def jRequest(dID):
	#VARIABLES TO BE CHANGED (FIRST 3 LINES)
	#Hard Code these lines based on the Raspberry Pi Data
	#Might need to make a change or two
	sqliteDB = '/home/pi/Desktop/MERA/PiDatabase' #Path where DB is stored
	url = "http://thawing-ravine-9396.herokuapp.com/dispenser?id="
	dispenserID = dID
	
	#Dispenser Request URL
	dispenserRequest = url + repr(dispenserID)

	#HTTP Request to the website
	r = requests.get(dispenserRequest)
	
#Only accounted for a successful HTTP Request
	if (r.status_code==200):
		data = r.json()
		print "Successful HTTP Request to MERA Website"
		return data

def SQLUpdate(data):
	if os.path.isfile(sqliteDB):
		print "Database Exists"
		conn = sqlite3.connect(sqliteDB) #Connect to the existing Database
		c = conn.cursor()
		
		#We are assuming since the DB is already setup, we have the dispenser set up too
		#We need to update the data stored in the DB
		c.execute(''' INSERT OR REPLACE INTO dispenser(startTime, endTime) VALUES(?,?) WHERE dispenserID = ? ''',
				 (data['Operation Start Time'],data['Operation End Time'],data['Dispenser ID']))
		for eachContainer in data['Containers']:
			c.execute(''' INSERT OR REPLACE INTO container(containerID, pillCount, attachedTo) VALUES(?,?,?) ''',
					 (eachContainer['Container ID'],eachContainer['Pill Count'],data['Dispenser ID']))
			c.execute(''' INSERT OR REPLACE INTO medication(dose, scheduledTime, dailyTime, frequency, storedIn) VALUES(?,?,?,?,?) ''',
					 (eachContainer['Medication']['Dose'],
						eachContainer['Medication']['Scheduled Time'], 
						eachContainer['Medication']['Daily Time'],
						eachContainer['Medication']['Frequency'],
						eachContainer['Container ID']
					))
		conn.commit()
		conn.close()
	
	else:
		print "Doesn't exist"
		conn = sqlite3.connect(sqliteDB)
		c = conn.cursor()
		#Create Tables Dispenser, Container & Medication
		c.execute('''CREATE TABLE dispenser(dispenserID bigserial primary key not null, startTime time, endTime time, CONSTRAINT dispenserIDUnique UNIQUE(dispenserID)) ''')
		c.execute('''CREATE TABLE container(containerID bigserial primary key not null, pillCount bigint, attachedTo bigserial, foreign key(attachedTo) References dispenser(dispenserID),
					 CONSTRAINT containerIDUnique UNIQUE(containerID))''')
		c.execute('''CREATE TABLE medication(dose bigint, scheduledTime time, dailyTime time, frequency bigint, storedIn bigserial, foreign key(storedIn) References container(containerID),
					 CONSTRAINT medicationIDUnique UNIQUE(storedIn))''')
		
		#Save to the Database the HTTP Request Information
		c.execute(''' INSERT INTO dispenser(dispenserID, startTime, endTime) VALUES(?,?,?) ''',
				 	(data['Dispenser ID'],
					data['Operation Start Time'],
					data['Operation End Time']
				))
		for eachContainer in data['Containers']:
			c.execute(''' INSERT INTO container(containerID, pillCount, attachedTo) VALUES(?,?,?) ''',
					 (eachContainer['Container ID'],
					eachContainer['Pill Count'],
					data['Dispenser ID']
				))
			c.execute(''' INSERT INTO medication(dose, scheduledTime, dailyTime, frequency, storedIn) VALUES(?,?,?,?,?) ''',
					 (eachContainer['Medication']['Dose'],
					 eachContainer['Medication']['Scheduled Time'],
					 eachContainer['Medication']['Daily Time'],
					 eachContainer['Medication']['Frequency'],
					 eachContainer['Container ID']
					))
		conn.commit()
		conn.close()
