import time

n = 0
while True:
    f = open("peizhi/pin.txt", "a")
    f.write(str(n) + "\n")
    f.close()
    n += 1
    time.sleep(0.3)
    if n > 1000:
        break
