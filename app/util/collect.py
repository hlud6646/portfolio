from scrapers import bom, smh, wzn
from time import sleep


# In the real world this would take place at arms length from the server
# and be a cronjob or something like that rather than a python loop.
while True:
	try:
		data = '{0},{1},{2}\n'.format(bom(), smh(), wzn())
		with open('/home/ubuntu/portfolio/app/data/temperature.csv', 'a+') as f:
			f.write(data)
	# This is sinful but it's just a demo...
	except Exception as e:
		print(e)
	sleep(60*60)
