"""
    This is a collection of functions to load a database
    with subject data, collected from the UNL API

    **IMPORTANT**

    1. Make sure you've run the DB creation
    script before using this - the table already needs to
    exist in your DB.

    2. Make sure you fill in your DB info in DBCredentials.py
"""

import mysql.connector
from sys import exit

import SubjectDataHarvester
import DBCredentials

def main():
    if DBCredentials.USER == '' or DBCredentials.HOST == '' or DBCredentials.DATABASE == '':
        exit("ERROR: PLEASE ENTER YOUR DB INFORMATION IN THIS SCRIPT\n" \
        + "***\nAdditionally, be sure you've run tableCreationScript.sql\n" \
        + "on your DB before using this\n***")

    subjects = SubjectDataHarvester.getSubjects()
    exportSubjectsToDB(subjects)
    return

def exportSubjectsToDB(courses):
    cnx = getDBConnection()
    cursor = cnx.cursor()

    sql = getStatement()

    for i in range(len(courses)):
        course = courses[i]
        print(course.get('title'))
        values = getValues(course)
        cursor.execute(sql, values)

    cnx.commit()

    cursor.close()
    cnx.close()

    return

def exportSubjectToDB(subject):
    cnx = getDBConnection()
    cursor = cnx.cursor()

    sql = getStatement()
    values = getValues(subject)

    cursor.execute(sql, values)
    cnx.commit()

    cursor.close()
    cnx.close()
    return

def getStatement():
    return "insert into Subject " \
    + "(title, minorAvailable, minorOnly, colleges, uri, subjectPrefixes) " \
    + "values (%s, %s, %s, %s, %s, %s)"

def getValues(subject):
    return (
    subject.get('title'),
    int(subject.get('minorAvailable')),
    int(subject.get('minorOnly')),
    stringifyList(subject.get('college')),
    subject.get('uri'),
    stringifyList(SubjectDataHarvester.getSubjectPrefixes(subject.get('uri')))
    )

def stringifyList(l):
	return str(l).replace('\'', '').replace('[', '').replace(']', '')

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

if __name__ == '__main__':
    main()
