import light
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

# Setup GPIO pins for buttons:
for i in [17, 27, 22, 10]:
    GPIO.setup(i, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Setup light controller:
LC = light.LightController([light.SingleLightController(18),
                            light.SingleLightController(19)])


def toggle_power(channel):
    LC.power_toggle()


def toggle_mode(channel):
    LC.toggle_mode()


def increase_level(channel):
    increment = 5
    LC.level(LC.brightness + increment)


def decrease_level(channel):
    increment = 5
    LC.level(LC.brightness - increment)

bouncetime = 100

GPIO.add_event_detect(
    17, GPIO.FALLING, callback = toggle_power, bouncetime = bouncetime)

GPIO.add_event_detect(
    27, GPIO.FALLING, callback = toggle_mode, bouncetime = bouncetime)

GPIO.add_event_detect(
    22, GPIO.FALLING, callback = increase_level, bouncetime = bouncetime)

GPIO.add_event_detect(
    10, GPIO.FALLING, callback = decrease_level, bouncetime = bouncetime)

input("Press enter to close...q")
