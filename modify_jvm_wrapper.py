#!/usr/bin/python
"""
Script made by Vignesh GJ (CECID : vgopalja)
Language : Python 3.x
Purpose : Add params to Wrapper settings of JVM instance for specific application
"""

import sys
import os
import re
import logging

# USAGE:  <life_cycle> <string_to_be_added>

cwd = os.getcwd()
logging.basicConfig(filename=cwd + '/newfile.log',
                    format='%(levelname)s:%(asctime)s:%(message)s',
                    filemode='a')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# Path Assignment to variables

life_cycles = ['dev', 'stage', 'lt', 'prod']
base_path = '/opt/infra/apm-local/'
if sys.argv[1] in life_cycles and len(sys.argv)==3:
        life_cycle = sys.argv[1]
        string_to_be_appended_3 = sys.argv[2]
else:
        print "Please use this format: <script> <life_cycle> <string_to_be_appened>"
        sys.exit()
last_path = '/conf/nocli_wrapper.conf'

# Gets list of Jvm in given lifecycle

def fetch_jvm(base_path, life_cycle):
	""" This function will fetch the list of JVM under specified life cycle """
	print 'fetching the Jvm ......'
	logger.info('fetching the Jvm ......')
	try:
		a = [dI for dI in os.listdir(base_path + life_cycle + '/apps/')
			if os.path.isdir(os.path.join(base_path + life_cycle
				+ '/apps/', dI)) and 'mm' in dI[:2]]
		return a
	except OSError:
		print 'Error: Path not exist' + base_path + life_cycle
		logger.error('Error: Path doesnot exist' + base_path
                     + life_cycle)


jvm_list = fetch_jvm(base_path, life_cycle)


def master():
	if jvm_list != None:
		for app_id in jvm_list:
			path = base_path + life_cycle + '/apps/' + app_id + last_path
			string_to_be_appended_1 = "wrapper.java.additional."

			def find_num():
				""" This function will get already existing number in wrapper.conf and will generate non existing number """
				try:
					filename = path
					f = open(filename, 'r')
					text = f.read()
					s = re.findall(r"\.\d+|\d+", text)
					f.close()
					final = []
					for string in s:
						if "." in string:
							final.append(int(string[1:]))
					return final[-1]
				except IOError:
					# print(os.error) will <class 'OSError'>
					print 'Problem reading: ' + filename
					logger.error("Problem reading: "+ filename)

			string_to_be_appended_2 = str(find_num()+1) + "=-D"
			string_to_be_appended = string_to_be_appended_1+string_to_be_appended_2+string_to_be_appended_3


			def check_add():
				"""This function is used to check, weather the string to be added is alreday there or not"""
				try:
				# If the file does not exist,
					check = 0
					filename = path
					file = open(filename, 'r')
					text = file.read()
					s = re.findall(string_to_be_appended_3.strip(), text)
					file.close()
					check = len(s)
					if check == 0:
						add_line(string_to_be_appended)
					else:
						print "The line " + string_to_be_appended_3.strip() +" Already Exist in " + path
						logger.error("The line " + string_to_be_appended_3.strip() +" Already Exist in " + path)
				except IOError:
                    # print(os.error) will <class 'OSError'>
					print 'Problem reading: ' + filename
					logger.error("Problem reading: "+ filename)



			def add_line(string_to_be_appended):
				"""This function will open the file and add the Expected line to end of the file"""
				try:
					filename = path
					file = open(filename, 'a')
					file.write("\n")
					file.write(string_to_be_appended.strip())
					file.close()
					print "Sucessfully added"
					logger.info("Life_cycle: "+ life_cycle)
					logger.info("app_id: "+ app_id)
					logger.info("string_to_be_appended: "+ string_to_be_appended_3)
					logger.info("The line: "+ string_to_be_appended + " Sucessfully added to the path: "+ filename)
				except IOError:
					print 'Problem writing: ' + filename
					logger.error("Problem reading: "+ filename)
			if life_cycle in life_cycles and "mm" in app_id[:2] and len(app_id) == 8:
				check_add()
			else:
				print "check lifecyle"
				print "Use the below format:  <life_cycle> <string_to_be_added>"
				logger.error(" Check the lifecycle")
				logger.error(" Use the below format:  <life_cycle> <string_to_be_added>")



# calling the master function
master()
