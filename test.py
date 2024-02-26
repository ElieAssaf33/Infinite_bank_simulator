from datetime import date,datetime
import time

timestamp = time.mktime(datetime.now().timetuple())
print(timestamp)

date4 = datetime.fromtimestamp(timestamp)


date1 = date(date4)
date2 = date(date4)
date3 = date1 - date2

print(date3)