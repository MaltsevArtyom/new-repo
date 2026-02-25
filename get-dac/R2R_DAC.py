import RPi.GPIO as GPIO

class R2R_DAC:
    def __init__(self, gpio_bits, dynamic_range, verbose=False):
        self.gpio_bits = gpio_bits
        self.dynamic_range = dynamic_range
        self.verbose = verbose

        
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpio_bits, GPIO.OUT, initial=0)

    def deinit(self):
        GPIO.output(self.gpio_bits, 0)
        GPIO.cleanup()
        if self.verbose:
            print("GPIO очищены, работа завершена.")

    def set_number(self, number):
        bin_list = [int(bit) for bit in bin(number)[2:].zfill(8)[::-1]]
        GPIO.output(self.gpio_bits, bin_list)
        
        if self.verbose:
            print(f"Число на вход ЦАП: {number}, биты: {bin_list}")

    def set_voltage(self, voltage):
        if not (0.0 <= voltage <= self.dynamic_range):
            print(f"Напряжение выходит за динамический диапазон ЦАП (0.00 - {self.dynamic_range:.2f} B)")
            return
        number = int(voltage / self.dynamic_range * 255)
        self.set_number(number)

if __name__ == "__main__":

    my_pins = [22, 27, 17, 26, 25, 21, 20, 16]
    
    dac = R2R_DAC(my_pins, 3.18, verbose=True)

    try:
        while True:
            try:
                user_val = input("Введите напряжение в Вольтах: ")
                if user_val.lower() == 'q': break
                
                voltage = float(user_val)
                dac.set_voltage(voltage)
                
            except ValueError:
                print("Вы ввели не число. Попробуйте ещё раз\n")
    finally:
    
        dac.deinit()