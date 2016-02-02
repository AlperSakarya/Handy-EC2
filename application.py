import os
import time
import sys

# REPLACE THIS WITH YOUR PRIVATE KEY
ssh_keyPath = "/path/to/your/key.pem"


# Installing required packages if they are not installed
try:
    import boto
except ImportError, e:
    print "BOTO COULD NOT BE FOUND TRYING TO INSTALL IT..."
    time.sleep(2)
    os.system("sudo pip install boto")
    import boto

try:
    from blessings import Terminal
except ImportError, e:
    print "BLESSINGS COULD NOT BE FOUND TRYING TO INSTALL IT..."
    os.system("sudo pip install blessings")
    from blessings import Terminal

ec2 = boto.connect_ec2()
instances = ec2.get_only_instances()
t = Terminal()


def main_function():
    os.system('clear')
    number = 1
    n = len(instances)
    global ssh_keyPath

    def ssh_to_instance():
            ssh_command = "ssh -i {0} {1}@{2}".format(ssh_keyPath, ssh_username, ssh_instance)
            os.system(ssh_command)

    # Coloring of running/stopped/other states
    def color_i_state():
        if instance.state == "running":
            return t.green(instance.state)
        elif instance.state == "stopped":
            return t.red(instance.state)
        else:
            return t.yellow(instance.state)

    # Describe instances the way I want to see
    print t.blue("##########################################################################################")
    print "TOTAL INSTANCES:", n
    for instance in instances:
        color_i_state()
        # looking to see if instance tag exist or not
        if 'Name' in instance.tags:
            print number, t.bold("Instance:"), instance.id, "||", t.bold("State:"), color_i_state(), "||", t.bold("Public IP:"), instance.ip_address, "\n", t.bold("Name:"), instance.tags['Name']
            number = (number + 1)
        else:
            print number, t.bold("Instance:"), instance.id, "||", t.bold("State:"), color_i_state(), "||", t.bold("Public IP:"), instance.ip_address, "\n", t.bold("Name:"), "no tag OR not available now"
            number = (number + 1)

    print t.blue("##########################################################################################")
    print "REFRESH  - Press 0"
    print "START    - Press 1"
    print "STOP     - Press 2"
    print "SSH      - Press 3"
    print "EXIT     - Press 9"

    operation = raw_input()
    if operation == "0":
        main_function()

    elif operation == "1":
        selected_instance = int(raw_input("What is the instance number? e.g 1 or 2 "))
        selected_instance = (selected_instance - 1)
        instances[selected_instance].start()
        print "Instance is starting..."
        time.sleep(3)
        main_function()

    elif operation == "2":
        selected_instance = int(raw_input("What is the instance number? e.g 1 or 2 "))
        selected_instance = (selected_instance - 1)
        instances[selected_instance].stop()
        print "Instance is stopping..."
        time.sleep(3)
        main_function()

    elif operation == "3":
        selected_instance = int(raw_input("What is the instance number? e.g 1 or 2 "))
        selected_instance = (selected_instance - 1)
        ssh_username = (raw_input("What is the SSH user?")).lower()
        ssh_instance = instances[selected_instance].ip_address
        if os.path.exists(ssh_keyPath):
            ssh_to_instance()
        else:
            print "SSH Private Key can't be found..."
            time.sleep(3)
            ssh_keyPath = raw_input("Please enter full path for your private key e.g /home/myuser/mykey.pem")
            ssh_to_instance()

    elif operation == "9":
        print "GOOD BYE..."
        exit()

    else:
        print t.red("Wrong selection")
        time.sleep(3)
        main_function()

# Running the app and capturing SIGINT
try:
    main_function()
except KeyboardInterrupt:
    print "GOOD BYE..."
    sys.exit(0)
