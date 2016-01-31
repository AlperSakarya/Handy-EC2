import boto, os, time, sys
from blessings import Terminal
from boto.manage.cmdshell import sshclient_from_instance

ec2 = boto.connect_ec2()
instances = ec2.get_only_instances()
t = Terminal()



def main_function():
    os.system('clear')
    number = 1
    n = len(instances)

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
            print number, t.bold("Instance:"), instance.id, "||", t.bold("State:"), color_i_state(), "||", t.bold("Public IP:"), instance.ip_address, "||", t.bold("Name:"), instance.tags['Name']
            number = (number + 1)
        else:
            print number, t.bold("Instance:"), instance.id, "||", t.bold("State:"), color_i_state(), "||", t.bold("Public IP:"), instance.ip_address, "||", t.bold("Name:"), "no tag OR not available now"
            number = (number + 1)

    print t.blue("##########################################################################################")
    print "Refresh instance list  - Press 0"
    print "Start an Instance      - Press 1"
    print "Stop  an Instance      - Press 2"
    print "Connect to an Instance - Press 3"
    print "Ctrl + C to exit or    - Press 9"

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
        ssh_username = raw_input("What is the SSH user?")
        ssh_instance = instances[selected_instance]
        keypath = "/Users/sakaryaa/.ssh/EC2-NEW.pem"
        boto.manage.cmdshell.sshclient_from_instance(ssh_instance,keypath,host_key_file='~/.ssh/known_hosts',user_name=ssh_username, ssh_pwd=None).run("ls")

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
