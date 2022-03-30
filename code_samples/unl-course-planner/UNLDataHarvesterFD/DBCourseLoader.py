"""
    This is a collection of functions to load a database
    with course data, collected from the UNL API

    **IMPORTANT**

    1. Make sure you've run the DB creation
    script before using this - the table already needs to
    exist in your DB.

    2. Make sure you fill in your DB info in DBCredentials.py
"""

import mysql.connector
from sys import exit

import CourseDataHarvester
import DBCredentials

def main():
    if DBCredentials.USER == '' or DBCredentials.HOST == '' or DBCredentials.DATABASE == '':
        exit("ERROR: PLEASE ENTER YOUR DB INFORMATION IN DBCredentials\n" \
        + "***\nAdditionally, be sure you've run tableCreationScript.sql\n" \
        + "on your DB before using this\n***")

    courses = CourseDataHarvester.getCourses()
    exportCoursesToDB(courses)
    return

def exportCoursesToDB(courses):
    cnx = getDBConnection()
    cursor = cnx.cursor()

    sql = getStatement()

    for course in courses:
        print("Exporting: " + course.get('title'))
        values = getValues(course)
        cursor.execute(sql, values)

    cnx.commit()

    cursor.close()
    cnx.close()

    return

def exportCourseToDB(course):
    cnx = getDBConnection()
    cursor = cnx.cursor()

    sql = getStatement()
    values = getValues(course)

    cursor.execute(sql, values)
    cnx.commit()

    cursor.close()
    cnx.close()
    return

def getStatement():
    return "insert into Course " \
    + "(title, courseCodes, gradingType, dfRemoval, effectiveSemester, " \
    + "prerequisites, description, campuses, deliveryMethods, " \
    + "termsOffered, activities, credits, aceOutcomes) " \
    + "values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

def getValues(course):
    return (
    course.get('title'),
    stringifyCourseCodes(course.get('courseCodes')),
    course.get('gradingType'),
    int(course.get('dfRemoval')),
    course.get('effectiveSemester'),
    course.get('prerequisite'),
    course.get('description'),
    stringifyList(course.get('campuses')),
    stringifyList(course.get('deliveryMethods')),
    stringifyList(course.get('termsOffered')),
    stringifyActivities(course.get('activities')),
    stringifyCredits(course.get('credits')),
    stringifyACEOutcomes(course)
    )

def getDBConnection():
	cnx = mysql.connector.connect()

	try:
		cnx = mysql.connector.connect(
        user=DBCredentials.USER, password=DBCredentials.PASSWORD,
		host=DBCredentials.HOST, database=DBCredentials.DATABASE)

	except mysql.connector.Error as err:
		if err.errno == mysql.connector.errorcode.ER_ACCESS_DENIED_ERROR:
			exit("Something is wrong with your user name or password")
		elif err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
			exit("Database does not exist")
		else:
			exit(err)

	return cnx

def stringifyACEOutcomes(course):
	if 'aceOutcomes' in course.keys():
		return stringifyList(course.get('aceOutcomes'))

	return ""

def stringifyCredits(credits):
	s = ""
	count = 1
	for credit in credits:
		for value in credit.values():

			if count % 2 == 0:
				s += str(value) + ", "
			else:
				s += str(value) + ": "
			count += 1

	return s[0 : len(s)-2]

def stringifyActivities(activities):
	s = ""
	for activity in activities:
		s += activity.get('type') + " " + str(activity.get('hours')) + ", "

	return s[0 : len(s)-2]

def stringifyCourseCodes(courseCodes):
	s = ""
	for courseCode in courseCodes:
		s += courseCode.get('subject') + " " + courseCode.get('courseNumber') + ", "

	return s[0 : len(s)-2]

def stringifyList(l):
	return str(l).replace('\'', '').replace('[', '').replace(']', '')

if __name__ == '__main__':
	main()
