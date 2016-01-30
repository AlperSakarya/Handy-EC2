import boto, os
from blessings import Terminal

ec2 = boto.connect_ec2()
instances = ec2.get_only_instances()
t = Terminal()

# Describe instances the way I want to see
print t.blue("#########################################################")

def color_i_state():
	if instance.state == "running":
		return t.green(instance.state)
	elif instance.state == "stopped":
		return t.red(instance.state)
	else:
		return t.yellow(instance.state)

for instance in instances:
	print "-- ", t.bold("Instance:") ,instance.id, "||", t.bold("State:"), color_i_state(), "||", t.bold("Public IP:"), instance.ip_address, "||", t.bold("Name:") ,instance.tags['Name'] 
print t.blue("#########################################################")
