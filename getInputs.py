import time, os, sys

def getInputs(outputDir, curfilename):
	outputInstance = f'{curfilename} {time.strftime("%Y-%m-%d")} {time.strftime("%H;%M;%S")}'
	newDir = outputDir + outputInstance
	os.mkdir(newDir)
	os.chdir(newDir)
	os.mkdir('Logs')
	print(f"files will be saved in >> {os.getcwd()}")
	
	print("Paste the nodes Names & IPs & Passwords & Usernames from excel: (then hit CTRL+Z and Enter)")
	paste_ne_IP_Pass = sys.stdin.read()
	devices_lst = paste_ne_IP_Pass.strip().split('\n\n')
	credentials = []
	for info in devices_lst:
		creds = [dev.split('***') for dev in info.split('\n') if dev != '']
		Foldername = 'Output'
		os.mkdir(Foldername)
		credentials += [{'NE_Name': tup[0], 'host': tup[1], "password": tup[2], "username": tup[3], "Foldername": Foldername}  for tup in creds]
	return credentials
