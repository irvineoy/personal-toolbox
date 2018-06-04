import os

path = "./"
for root, dirs, files in os.walk("."):
	for file in files:
		if file[-4:] == '.png':
			nameBefore = file
			nameAfter = file[:-4] + '.eps'
			os.system('convert ' + nameBefore + ' ' + nameAfter)