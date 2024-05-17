# Batch-execute-huawei-vrp
Automate command execution on all managed huawei devices using python

1- Before running the script, insure that these modules are installed:
   - pip install paramiko
   - pip install netmiko
   - pip install openpyxl
   - pip install textfsm

2- Use the devices.xlsx template as a reference for your devices credentials

3- Run the python script **Batch Execute - Netmiko.py**
    - Paste devices credentials that you copied from the excel template, then hit CTRL+Z and Enter
    - Paste or write the commands to be executed on the devices, then hit CTRL+Z and Enter
    - The commands outputs and session logs are saved in **scripts_Outputs**
