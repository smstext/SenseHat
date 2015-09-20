from sense_hat import SenseHat

sense = SenseHat()

red = (0, 0, 255)
white = (255, 0, 0)

while True:
    pressure = sense.pressure
    pressure_value = 64 * pressure
    print(pressure)

    pixels = [red if i < pressure_value else white for i in range(64)]

