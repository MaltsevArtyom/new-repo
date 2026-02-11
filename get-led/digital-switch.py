botton = 13
GPIO.setup(botton, GPIO.IN)

while True:
    if GPIO.input(botton):
        state = not state
        GPIO.output(led, state)
        time.sleep(0.2)