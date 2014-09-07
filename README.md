# AMRUSB-1 Logging from Raspberry Pi

This Python script will log readings received from a [Grid Insight AMRUSB-1 ](http://www.gridinsight.com/products/amrusb-1/)to [Amazon AWS Dynamo DB](http://aws.amazon.com/dynamodb/).

I have no affiliation with Grid Insight; this is code I created for my own purposes.

## Dependencies

	sudo apt-get install python-setuptools
	sudo easy_install pyserial 
	sudo easy_install pip
	sudo pip install boto

## Amazon Dynamo DB Setup

In Amazon Dyanmo DB, create a new table called **readings** with the following settings:

	Table Name: 	readings
	Primary Hash Key: serialnumber (Number)
	Primary Range Key: datestamp (Number) 
	Provisioned Read Capacity Units: 1
	Provisioned Write Capacity Units: 	1

## Installation
  
Put the amrusb.py Python script into **/home/pi/amrusb** and then:
  
	sudo mkdir /var/log/amrusb

In the file **/etc/boto.cfg** put Amazon AWS credentials with privileges sufficient to create Dynamo DB items in the table you created above:

	[Credentials]
	aws_access_key_id = ACCESS_KEY_GOES_HERE
	aws_secret_access_key = SECRET_ACCESS_KEY_GOES_HERE

Copy the amrusb shell script into /etc/init.d and then:

	sudo chmod +x /etc/init.d/amrusb
	sudo update-rc.d amrusb defaults

This will ensure that the logging script starts as a daemon on boot.

## Test

First, make sure that the script works when run from the command line:

	sudo /home/pi/amrusb/amrusb.py
	
Leave this running, and watch the log:

	tail -f /var/log/amrusb/amrusb.log
	
Where you should see something like this:

	2014-09-07 19:49:04,678 - DaemonLog - INFO - Starting amrusb daemon
	2014-09-07 19:49:04,682 - DaemonLog - INFO - Opening device /dev/ttyACM0
	2014-09-07 19:49:04,684 - DaemonLog - INFO - Connected to Amazon Dynamo DB
	2014-09-07 19:49:36,408 - DaemonLog - INFO - $UMSCM,24543136,7,1764501*6E
	2014-09-07 19:50:00,033 - DaemonLog - INFO - $UMSCM,26080514,8,31849*6A

For any SCM line -- those starting with **$UMSCM** -- you should see data in the Amazon Dynamo DB table you created.

# Launching on Boot

If all of the above works properly, then:

	sudo /etc/init.d/amrusb start
	
And you should see similar log items.

If you got this far, then you should be able to reboot, and you should find that, on reboot, the amrusb.py script is running:

	# ps ax | grep amrusb.py
	 2941 ?        S      0:02 python /home/pi/amrusb/amrusb.py
