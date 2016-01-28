"""
Created by Anahi Garnelo (https://github.com/agarnelo)
modified by Ying Fang Lee

methods:
pContainer(postData)
	Takes a json string and post update to web server
"""

import json
import datetime
import sqlite3
import os

#Class Container is going to hold information for each Container stored in the device

class Container:
	dispenserID = 0
	pillCount = 0
	scheduledTime = ""
	dailyTime = ""
	frequency = 0
	dose = 0
	OstartTime = ""
	OendTime = ""
	containerID = 0

#Containers Dictionary
#Containers -> Key: the Container ID & the Value: Container Class
Containers = {}

def fetchContainers():
	#VARIABLES TO BE CHANGED (FIRST LINE)
	sqliteDB = 'path to SQLite database'

	#Check if the database Exists
	if os.path.isfile(sqliteDB):
		print "Exists"
		conn = sqlite3.connect(sqliteDB)
		c = conn.cursor()
		
		#DISPENSER INFORMATION
		c.execute('''SELECT * FROM dispenser''')
		for row in c:
			dispenserID = row[0]
			startTime = row[1]
			endTime = row[2]
		print dispenserID
		print startTime
		print endTime


		c.execute('''SELECT * FROM container''')
	#	print "\nContainer"
	#	print "container ID, Pill Count, Dispenser ID"

		for row in c:
			contain = Container()
			Containers[row[0]] = contain
			Containers[row[0]].pillCount = row[1]
			Containers[row[0]].dispenserID = row[2]
			Containers[row[0]].OstartTime = datetime.datetime.strptime(startTime, '%I:%M %p').time()
			Containers[row[0]].OendTime = datetime.datetime.strptime(endTime, '%I:%M %p').time()
		c.execute('''SELECT * FROM medication''')
	#	print "\nMedication"
	#	print "Dose, Scheduled Time, Daily Time, Frequency, Container Stored In"
		for row in c:
			Containers[row[4]].dose = row[0]
			Containers[row[4]].scheduledTime = datetime.datetime.strptime(row[1], '%I:%M %p')
			Containers[row[4]].dailyTime = datetime.datetime.strptime(row[2], '%I:%M %p').time()
			Containers[row[4]].frequency = datetime.timedelta(int(row[3]))
		conn.close()

		#Print out the Containers Information
		for each in Containers:
			print "Dispenser ID", Containers[int(each)].dispenserID
			print "Pill Count in Container", Containers[int(each)].pillCount
			print "Scheduled Time ",Containers[int(each)].scheduledTime
	#		start_time = datetime.datetime.strptime(Containers[int(each)].scheduledTime, '%I:%M %p').time()
	#		print start_time
			print "Operation start time " , Containers[row[0]].OstartTime
			print "Operation start time " , Containers[row[0]].OendTime
			print "Daily Time ", Containers[int(each)].dailyTime
			print "Frequency ",Containers[int(each)].frequency
			print "Dose ",Containers[int(each)].dose
			print "\n"

	else:
		return None
	return Containers



"""
{"Dispenser ID":10,"Operation Start Time":"09:00 AM","Operation End Time":"10:00 PM","Updated":true,"Containers":[{"Container ID":1,"Pill Count":25,"Medication":{"Dose":1,"Frequency":5},"Days":{"Mon":true,  "Tues":true, "Wed":false, "Thur":"" , "Fri": "", "Sat": "", "Sun":"" }}]}

days will be implemented as binary number if im taking this pill everyday: 1111111
binaryString = ""
if Days["Mon"] == true:
	binaryString += "1"
elif Days["Mon"]== false:
	binaryString += "0"

if Days["Tues"] == true:
	binaryString += "1"
elif Days["Tues"]== false:
	binaryString += "0"
	
if Days["Wed"] == true:
	binaryString += "1"
elif Days["Wed"]== false:
	binaryString += "0"

if Days["Tues"] == true:
	binaryString += "1"
elif Days["Tues"]== false:
	binaryString += "0"

if Days["Fri"] == true:
	binaryString += "1"
elif Days["Fri"]== false:
	binaryString += "0"

if Days["Sat"] == true:
	binaryString += "1"
elif Days["Sat"]== false:
	binaryString += "0"

if Days["Sun"] == true:
	binaryString += "1"
elif Days["Sun"]== false:
	binaryString += "0"
	
	
"""

#http://stackoverflow.com/questions/12932607/how-to-check-with-python-and-sqlite3-if-one-sqlite-database-file-exists



