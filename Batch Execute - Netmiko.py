import time, re, os, multiprocessing, concurrent.futures, sys
from netmiko import Netmiko
from netmiko.exceptions import NetmikoAuthenticationException
from getInputs import getInputs

try: os.mkdir("scripts_Outputs")
except FileExistsError: pass

credentials = getInputs(f'{os.getcwd()}\\scripts_Outputs\\', os.path.basename(__file__)[:-3])
print("Please Enter commands to be executed line by line: (then hit CTRL+Z and Enter when finished)")
print("PS: (each line is considered a command and will be executed on the device)")
commands = re.split(r'[\r\n]+', sys.stdin.read().strip().strip())


start_time = time.time()

counter = 0
def mainCode(remote, counter):
	if remote["host"] == "" or remote["username"] == "" or remote["password"] == "": return
	try: 
		host = {
		"host": remote["host"],
		"username": remote["username"],
		"password": remote["password"],
		"device_type": "huawei_vrp",
		"session_log": f'Logs/{remote["host"]}_session.log',
		}#, "global_delay_factor": 2}
		shell = Netmiko(**host)
	except NetmikoAuthenticationException as e:
	# Handle authentication errors
		print(f'Authentication error for: {remote["host"]}, Password is not {remote["password"]}')
		return 0
	except Exception as e:
		# Handle unexpected exceptions
		print(f"An unexpected error occurred while trying to connect to {remote['NE_Name']}: {str(e)}")
		return 0
	#print(f"Device name: {device_sysname}")
	try:
		output = ''
		for command in commands:
			output += shell.send_command_timing(command, strip_prompt=False, strip_command=False, read_timeout=0)
			time.sleep(1)
		device_Sysname = shell.find_prompt().split('<')[-1].strip('>')
		print(f"Device name: {device_Sysname} {remote['host']}, Success")
		counter += 1
	except Exception as e:
		# Handle unexpected exceptions
		print(f"An unexpected error occurred while executing commands on {remote['NE_Name']}: {str(e)}")
		return 0
	shell.disconnect()
	os.rename(f'Logs/{remote["host"]}_session.log', f'Logs/{device_Sysname}_session.log')


	filename = device_Sysname+'.txt'
	with open(remote['Foldername'] + '/' + filename, 'w') as f:
		f.write(output)
	return counter



num_threads = 100#min(int(multiprocessing.cpu_count() * (3/4)), len(credentials))

# Create a thread pool executor with the desired number of threads
with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
	# Submit the slow function to the thread pool executor for each piece of data
	futures = [executor.submit(mainCode, remote, counter) for remote in credentials]
	# Wait for all the threads to complete
	results = [f.result() for f in futures]
	sum_counter = sum(results)


end_time = time.time()
print(f"success rate = {sum_counter}/{len(credentials)}")
# Calculate and print the elapsed time
execution_time = end_time - start_time
print(f"Execution time: {execution_time:.6f} seconds")