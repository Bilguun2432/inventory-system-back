import math


id = 999

print(str(id))


progress = list(reversed(["K", "M", "B", "T"]))
lastIndex = len(progress) - 1

step = 1000
currentStep = 1
for name in progress:
    currentStep = math.floor(currentStep * step)

remain = id

print(str(currentStep))

for name in progress:
    range = math.floor(remain/currentStep)

    rangeName = str(range) + name
    rangeName = f"{range:0{3}}{name}"
    remain = remain % currentStep
    currentStep = currentStep / step

    print(rangeName)
