#!/usr/bin/python

import threading
from datetime import datetime
from time import sleep

def thread_job():
	while True:
		print(str(datetime.now()) + " - Thread output")
		sleep(2)


nums = int(input("How many threads to run?"))
print("Start %s threads." % (nums))
for i in range(0, nums):
        print("Start a new thread!")
        new_thread = threading.Thread(target=thread_job)
        new_thread.start()

