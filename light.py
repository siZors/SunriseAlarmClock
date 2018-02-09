import pigpio
import time
import easings


class SingleLightController:
    """A controller for controlling an LED light.

    Input the channel, frequency and mode for a PWM LED controller. The channel
    should be a GPIO channel, the frequency is given in HZ, and the mode should
    either "strong" or "weak", and referers to the type of PWM that is used.

    Strong mode has more stable pulses and a finer selection of duty cycles, but
    is limited to two channels, while the weak mode can be run on all 31 GPIO
    pins.
    """

    def __init__(self, channel, frequency=20000, mode="strong"):
        self.channel = channel
        self.frequency = frequency
        self.brightness = 0
        SingleLightController.pi = pigpio.pi()
        # Set pull down resistor for N-type MOSFET transistor
        SingleLightController.pi.set_pull_up_down(self.channel, pigpio.PUD_DOWN)
        self.set_mode(mode)

    def _intensity_log(func):
        """Modify intensity value.

        Since the human eye does not precieve the input as linear, this
        decorator will modify the function input to a logarithmic scale."""
        def func_wrapper(self, input, *args, **kwargs):
            output = 10**(input / 49.899) - 1
            if input == 100:
                output = 100
            return func(self, output, *args, **kwargs)
        return func_wrapper

    @ _intensity_log
    def _set_level_strong(self, new_level, transition_time=1):
        """Change level of LEDs.

        Time in seconds, frequency in Hz and GPIO channel."""

        # Note that self.brightness refers to the old brightness level until it
        # is redefined at the end of the function.
        new_level = 10000*new_level  # Convert from 1-100 to 1M
        old_level = self.brightness
        change = new_level - old_level

        start_time = time.process_time()
        elapsed_time = 0
        while elapsed_time < transition_time:
            SingleLightController.pi.hardware_PWM(
                self.channel,
                self.frequency,
                int(easings.easeOutQuint(elapsed_time,
                                         old_level,
                                         change,
                                         transition_time)))
            elapsed_time = time.process_time() - start_time
        # Ensure that the final brightness is the given setpoint:
        SingleLightController.pi.hardware_PWM(
            self.channel, self.frequency, int(new_level))
        self.brightness = new_level

    @ _intensity_log
    def _set_level_weak(self, new_level, transition_time=1):
        """Change level of LEDs.

        Time in seconds, frequency in Hz and GPIO channel."""

        # Note that self.brightness refers to the old brightness level until it
        # is redefined at the end of the function.
        new_level = 100*new_level  # Convert from 1-100 to 10000
        old_level = self.brightness/100 # Convert from 1-1M to 10000
        change = new_level - old_level

        start_time = time.process_time()
        elapsed_time = 0
        while elapsed_time < transition_time:
            SingleLightController.pi.set_PWM_dutycycle(
                self.channel,
                int(easings.easeOutQuint(elapsed_time,
                                         old_level,
                                         change,
                                         transition_time)))
            elapsed_time = time.process_time() - start_time
        # Ensure that the final brightness is the given setpoint:
        SingleLightController.pi.set_PWM_dutycycle(
            self.channel, int(new_level))
        self.brightness = new_level*100

    def set_level(self, new_level, transition_time=1):
        if self.mode == "strong":
            self._set_level_strong(new_level, transition_time)
        elif self.mode == "weak":
            self._set_level_weak(new_level, transition_time)

    def set_mode(self, mode):
        """Change between strong mode and weak mode by passing "strong"
        or "weak".

        Strong mode uses hardware PWM, which is very stable and has a high
        degree of tuneability, but is only avalible on two channels on the RPI.

        Weak mode uses software PWM that is worse, but avalible on all GPIO
        pins on the raspberry pi.
        """
        self.mode = mode
        if mode == "strong":
            SingleLightController.pi.hardware_PWM(self.channel,
                                            self.frequency,
                                            self.brightness)
        elif mode == "weak":
            SingleLightController.pi.set_PWM_range(self.channel, 10000)
            SingleLightController.pi.set_PWM_dutycycle(self.channel,
                                                 int(self.brightness/100))
        else:
            raise ValueError

    def set_frequency(self, frequency):
        """Changees the frequency of the PWM signal in Hz."""
        SingleLightController.pi.set_PWM_frequency(self.channel, frequency)
        if self.mode == "strong":
            SingleLightController.pi.hardware_PWM(self.channel,
                                            frequency,
                                            self.brightness)
        self.frequency = frequency

class LightController:
    """"Light controller object.

    This object accepts a list of "SimpleLightController" objects and uses them
    to control the list as a set. As many SimpleLightControllers as you want
    can be fed into this object, but they must be fed as a list.

    The object also accepts a fan_pin, which is the GPIO pin that a bianary
    on/off fan is connected too. When the lights are on, the fan is on. When
    the lights are off, the fan is off.
    """

    def __init__(self, light_objects, fan_pin=4):
        self._fan_pin = fan_pin
        self.light_objects = light_objects
        self.mode_ix = 0
        self.brightness = 0
        self.last_brightness = 0

        self.turn_off()

    def _check_fan(self):
        """"Check to see if light is on/off and turn on/off fan accordingly."""
        if self.brightness == 0:
            self.light_objects[0].pi.write(self._fan_pin, 0)
        else:
            self.light_objects[0].pi.write(self._fan_pin, 1)

    def turn_off(self):
        """Turn off all lights and fan."""
        self.last_brightness = self.brightness
        for x in self.light_objects:
            x.set_level(0, 0)
            self.brightness = 0
        self._check_fan()

    def power_toggle(self):
        """Toggle between off and last brightness setting."""
        if self.brightness == 0:
            self.level(self.last_brightness)
        else:
            self.turn_off()

    def add_light_object(self, light_object):
        """Add another SimpleLightController object."""
        self.light_objects.append(light_object)

    def level(self, level, transition_time=0.2):
        """Set brightness level."""
        self.light_objects[self.mode_ix].set_level(level, transition_time)
        self.brightness = level
        self._check_fan()

    def toggle_mode(self):
        """Toggle between the different avalible light controllers."""
        self.light_objects[self.mode_ix].set_level(0, 0)
        if self.mode_ix == len(self.light_objects) - 1:
            self.mode_ix = 0
        else:
            self.mode_ix += 1
        self.light_objects[self.mode_ix].set_level(self.brightness, 0)
