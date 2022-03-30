"""
	This is a collection of functions to retrieve
	course data from the UNL API
"""

import requests
import json

def getCourses():
	subjectPrefixes = getSubjectPrefixes()
	courseData = getAllCourseData(subjectPrefixes)
	return extractCoursesFromCourseData(courseData)

def getTestCourse():
    subjectPrefixes = getSubjectPrefixes()
    courseData = getCourseDataItem(subjectPrefixes[0])
    courses = courseData.get('courses')
    return courses[0]

def extractCoursesFromCourseData(courseData):
	courses = list()

	for courseDataItem in courseData:
		for course in courseDataItem.get('courses'):
			print("Extracting from course data: " + course.get('title'))
			courses.append(course)

	return courses

def getAllCourseData(subjectPrefixes):

	courseData = list()
	for subjectPrefix in subjectPrefixes:
		courseDataItem = getCourseDataItem(subjectPrefix)
		courseData.append(courseDataItem)

	return courseData

def getCourseDataItem(subjectPrefix):
	# The '{0}' corresponds to subject id
	print("Getting course data from subjectPrefix: " + subjectPrefix)
	coursesURL = "https://bulletin.unl.edu/undergraduate/courses/{0:s}.json"
	return _getJSONFromLink(coursesURL.format(subjectPrefix))

def getSubjectPrefixes():
	return list(getSubjectData().keys())

def getSubjectData():
	subjectsURL = "https://bulletin.unl.edu/undergraduate/courses.json"
	print("Getting subjectData from: " + subjectsURL)
	return _getJSONFromLink(subjectsURL)

def _getJSONFromLink(url):
	r = requests.get(url)
	return r.json()
