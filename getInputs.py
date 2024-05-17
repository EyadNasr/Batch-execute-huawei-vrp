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
		if len(devices_lst) == 1: Foldername = 'Output'
		else:
			if any(i in str(creds).lower() for i in ['oob','eor','tor','ce']): Foldername = 'Switches'
			elif 'ne' in str(creds).lower(): Foldername = 'Routers'
			elif 'fw' in str(creds).lower(): Foldername = 'Firewalls'
			else: Foldername = 'Output'
		os.mkdir(Foldername)
		credentials += [{'NE_Name': tup[0], 'host': tup[1], "password": tup[2], "username": tup[3], "Foldername": Foldername}  for tup in creds]
	return credentials

# from autom.getInputs import getInputs
# credentials = getInputs('Z:\\Ed\\Portable_python\\scripts_Outputs\\', os.path.basename(__file__)[:-3])