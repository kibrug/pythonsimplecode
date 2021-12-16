# import subprocess so we can use system commands
import subprocess

# import the re module so that we can make use of regular expressions.
import re
# python allows us to run system commands by using a function provided by the subprocess module
# (subprocess.run(<list of command line arguments goes here>, <specify the second argument module
# The script is a parent process and create a child process which runs the system command
# and will only contents once the child process has completed
# To save the contents that gets sent to the standard output stream (the terminal)
# we have specify that we want to capture  the output,
#  so we specify  second argument as output is True

command_output = subprocess.run(["netsh", "wlen", "show", "profiles"], capture_output=True).stdout.decode()
# we import the re module so that we can make use of regular expressions
# we want to find all the wifi names which is always listed after "All user profiles
# in the regular expression we create a group of all characters until the return
profile_names = (re.findall("All User Profile    :(.*)\r", command_output))

# we create an empty list outside of the loop where dictionaris with all the wifi
# username and password will be saved

wifi_list = list()

# if we didn't find profile name we didn't have any wifi connections,
# so we only run the part check for the details of wifi and
# whether we can get their password in this part
if len(profile_names) != 0:
    for name in profile_names:
        # Every wifi connectin will need its owon dictionary which will be appends
        wifi_profile = dict()
        # we now run a more specific command to see the information about the specify
        # and if the security key is not absent we can possibly get the password
        profile_info = subprocess.run(["netsh", "wlen", "show", "profile", name], capture_output=True).stdout.decode()
        # we use a regular expression to only look for the absent cass so we can ignore them
        if re.search("Security key        :Absent", profile_info):
            continue
        else:
            # Assign ssid of the wifi profiles to the dictionary
            wifi_profile["ssid"] = name
            # these cases aren't absent and we shoul we should can run them "kev=class command"
            profile_info_pass = subprocess.run(["netsh", "wlen", "show", "profile", name, "key=clear"], capture_output=True).stdout.decode()
            # again run the regular expression to capture the group after the which is the password
            password = re.search("Key Content       :(.*)\r", profile_info_pass)
            # check if we found a password in the regular expression.All wifi connection will not have
            if password == None:
                wifi_profile["password"] = None
            else:
                # we assign the grouping (wher the password is containd) we are interested to the password
                wifi_profile["password"] =password[1]
            # we append the wifi information to the wifi_list
            wifi_list.append(wifi_profile)

for x in range(len(wifi_list)):
    print(wifi_list[x])
