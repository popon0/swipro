""" 
This script make easier to execute the python script, to get wifi information on windows
Just run, and get saved_wifi.txt file, that contain wifi, and password information that saved on windows
We imported all needed package just re, stand for Regular Expression and subprocess, to run our python script on windows environment
"""

# for making regular expression searching we use "re", this make python script can search specified information (regex) and details
import re
# Make script can interact with windows command process
import subprocess

# This allow script to run subproccess command, capture all command showing output
output_capture = subprocess.run(["netsh", "wlan", "show", "profiles"], capture_output=True).stdout.decode()
# We find all profile data, use regex to find "All User Profile" syntax and we needed details output capture as writed in line 15
profile_name = (re.findall("All User Profile     : (.*)\r", output_capture))

# Created new variable to make list of wifi that showing on .txt after program is executed line 49
wifi_list = list()

# if we didnt find any profile name, it will give output 0, then no action needed and program just terminated (end), if return to 1, then it get proccessing
if len(profile_name) != 0:
    
    for name in profile_name:
        
        # It will make wifi profile showing at dictionary
        wifi_profile = dict()
            
        # We run for getting more specific information processing, whether checking the Security key showing aren't absent we possibly can get the SSID password 
        profile_info = subprocess.run(["netsh", "wlan", "show", "profile", name], capture_output=True).stdout.decode()
        
        # We use Regex to ignore "absent" profile security key
        if re.search("Security key           : Absent", profile_info):
                continue
        else:
            # Assign the SSID of the wifi profile to the dictionary
            wifi_profile["ssid"] = name
            # We continue our process to make the password, cause in this case security key not showing absent, and we get the password written in plain format using "key=clear" command
            profile_info_pass = subprocess.run(["netsh", "wlan", "show", "profile", name, "key=clear"], capture_output=True).stdout.decode()
            # Again run the regular expressions to capture the group after the : which is the password saved
            password = re.search("Key Content            : (.*)\r", profile_info_pass)
            
            # Checking for wifi profile that dont have password, will be printed as None
            if password == None:
                wifi_profile["password"] = None
            else:
                # And if there a password that showing cause we did "key=clear" on line 35, the password will be printed and will append to dictionary that created on line 25
                wifi_profile["password"] = password[1]
                # Append all wifi_profile information variable in wifi_list dictionary
                wifi_list.append(wifi_profile)

# Finally the output will writed as saved_wifi.txt file, that contain list SSID and Password in plain text
with open('saved_wifi.txt', 'w+') as ro:
        # wifi_list variable that created on line 15, make information showing that appended at line 45
        for x in wifi_list:
            ro.write(f"SSID : {x['ssid']}\nPassword : {x['password']}\n\n")
