import time
from sense_hat import SenseHat
sh = SenseHat()
for i in reversed(range(0,10)):
	sh.show_letter(str(i))
	time.sleep(1)

