#!/usr/bin/python

# getIdfSeries.py

import os
import csv

def toStr(num):
	if(num >= 10):
		return str(num)
	else:
		return '0'+str(num)

def main():
	# ----- these need to be set to target the correct day
	fileYear = 2015
	fileMonth = 6
	fileDay = 9

	MIN_HOURS = 0
	MAX_HOURS = 23
	# ----- 

	dayStr_FileStem = toStr(fileYear)+'_'+toStr(fileMonth)+'_'+toStr(fileDay)
	dayStr_DateStem = toStr(fileYear)+'-'+toStr(fileMonth)+'-'+toStr(fileDay)

	startHour = MIN_HOURS
	endHour = startHour+2

	neededHours = [15,16,17,18,20,21]

	while endHour <= MAX_HOURS:

		if startHour in neededHours:
			idfOutFileName = dayStr_FileStem+'_'+toStr(startHour+1)+toStr(endHour)
			startTime = dayStr_DateStem+' '+toStr(startHour)+':00'
			endTime = dayStr_DateStem+' '+toStr(endHour)+':00'


			outFileWriter = open('/Users/internship/Desktop/internship/chandanStuff/twitter-events/scripts/idfComputing/chandanPreproc/python/input20150609','w')
			outFileWriter.write(idfOutFileName)
			outFileWriter.write('\n')		
			outFileWriter.write(startTime)
			outFileWriter.write('\n')
			outFileWriter.write(endTime)
			outFileWriter.write('\n')

			outFileWriter.close()

			print(idfOutFileName)
			print(startTime)
			print(endTime)
			print('\n')

			os.system("time /Users/internship/Desktop/internship/chandanStuff/twitter-events/scripts/idfComputing/chandanPreproc/python/main.py < /Users/internship/Desktop/internship/chandanStuff/twitter-events/scripts/idfComputing/chandanPreproc/python/input20150609")

		startHour += 1
		endHour += 1


if __name__ == '__main__':
	main()

