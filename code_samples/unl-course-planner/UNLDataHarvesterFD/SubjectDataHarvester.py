"""
	This is a collection of functions to retrieve
	subject data from the UNL API
"""

import requests
import json

def getSubjects():
	majorsURL = "https://bulletin.unl.edu/undergraduate/majors.json"
	return _getJSONFromLink(majorsURL)

def getTestSubject():
    return getSubjects()[0]

def getSubjectPrefixes(url):
	prefixData = _getJSONFromLink(url + "/courses.json")

	prefixes = list()
	for key in prefixData.keys():
		prefixes.append(prefixData[key])

	return prefixes
	
def getSubjectData():
	subjectsURL = "https://bulletin.unl.edu/undergraduate/courses.json"
	print("Getting subjectData from: " + subjectsURL)
	return _getJSONFromLink(subjectsURL)

def _getJSONFromLink(url):
	r = requests.get(url)
	return r.json()
