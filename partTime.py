import json
import time
import os
from pprint import pprint

def check(item):
	if item.isdigit():return 0
	else:
		print("Input wrong")
		exit(0)
	

def checkFloat(item):
	try:
		floatNum = float(item)
	except:
		print('Input wrong')
		exit(0)
	return 0


def inputTime():
	if os.path.isfile('./partTimeJob.json')==False:
		with open('partTimeJob.json', 'w') as file:
			file.write('[]')
	with open('partTimeJob.json', 'r') as file:
		dictList = json.load(file)
	print("Please input the 'q' to return homepage.")
	month = input("Input the month(12):  ")
	if month == 'q':
		run()
		exit(0)
	check(month)
	day = input("Input the day(12):  ")
	check(day)
	beginTime = input("Input the beginTime(15.5):  ")
	endTime = input("Input the endTime(21.5):  ")
	timeLength = float(endTime) - float(beginTime)
	dictInfor = {'month':int(month), 'day':int(day), 'beginTime':float(beginTime), 'endTime':float(endTime), 'timeLength':timeLength}
	dictList.append(dictInfor)
	with open('partTimeJob.json', 'w') as file:
		json.dump(dictList, file)


def calculMoney():
	with open('partTimeJob.json', 'r') as file:
		dictList = json.load(file)
	localtime = time.localtime(time.time())
	if localtime.tm_mday > 15:
		monthBefore = localtime.tm_mon
		if monthBefore == 12:
			monthAfter = 1
		else: monthAfter = monthBefore + 1
	if localtime.tm_mday <= 15:
		monthAfter = localtime.tm_mon
		if monthAfter == 1:
			monthBefore = 12
		else: monthBefore = monthAfter - 1
	
	sum = 0.0
	for i in range(len(dictList)):
		if dictList[i]['month'] == monthBefore:
			if dictList[i]['day'] > 15:
				sum += dictList[i]['timeLength']
		elif dictList[i]['month'] == monthAfter:
			if dictList[i]['day'] <= 15:
				sum += dictList[i]['timeLength']

	print('The sum of hours are %0.1f' % (sum))
	print('The total money is %0.0f' % (sum*880))

	# print(localtime.tm_mday)

def showTime():
	with open('partTimeJob.json', 'r') as file:
		dictList = json.load(file)
	for oneDay in dictList:
		print("Data:%d.%d Time:%0.1f~%0.1f Length:%0.1f Money:%d " % \
			(oneDay['month'], oneDay['day'], oneDay['beginTime'], oneDay['endTime'], oneDay['timeLength'], oneDay['timeLength']*880))		


def run():
	print("1.Calculate the time length and money")
	print("2.Show all the time of part-time job")
	a = input()
	if a == '1':
		calculMoney()
	if a == '2':
		showTime()


if __name__ == "__main__":
	inputTime()