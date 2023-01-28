from pyclick import HumanClicker
import time
# initialize HumanClicker object
hc = HumanClicker()

# move the mouse to position (100,100) on the screen in approximately 2 seconds
q = time.time()
hc.move((500,500),1)
x = time.time()
print(x-q)
# mouse click(left button)
