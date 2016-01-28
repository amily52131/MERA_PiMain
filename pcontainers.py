"""
Created by Anahi Garnelo (https://github.com/agarnelo)
modified by Ying Fang Lee
original function name is POSTContainers.py

methods:
pContainer(postData)
	Takes a json string and post update to web server
"""

import json
import urllib2

def pContainer(postData):
	try:
		req = urllib2.Request("https://thawing-ravine-9396.herokuapp.com/containers")
		req.add_header('Content-Type', 'application/json')
		print json.dumps(postData)
		response = urllib2.urlopen(req, json.dumps(postData))
		print "Post container response = ",response.getcode()
		return response.getcode()
	except:
		print "HTTP Post Error"
		raise