import RPi.GPIO as GPIO
import time

class R2R_ADC:
    def __init__(self, dynamic_range, compare_time=0.001):
        self.dynamic_range = dynamic_range
        self.compare_time = compare_time
        
        
        self.bits_gpio = [26, 20, 19, 16, 13, 12, 25, 11]
        self.comp_gpio = 21
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.bits_gpio, GPIO.OUT, initial=0)
        GPIO.setup(self.comp_gpio, GPIO.IN)

    def number_to_dac(self, number):
        
        bits = [int(bit) for bit in bin(number)[2:].zfill(8)]
        GPIO.output(self.bits_gpio, bits)

    def successive_approximation_adc(self):
        result_code = 0
        
        for bit in range(7, -1, -1):
          
            test_code = result_code | (1 << bit)
            self.number_to_dac(test_code)
            time.sleep(self.compare_time)
            
            
            if GPIO.input(self.comp_gpio) == 0:
                result_code = test_code
                
        return result_code

    def get_sar_voltage(self):
        code = self.successive_approximation_adc()
        return (code / 256.0) * self.dynamic_range


if __name__ == "__main__":
    
    adc = R2R_ADC(dynamic_range=3.3)
    
    try:
        print("Чтение напряжения методом SAR (бинарный поиск)...")
        while True:
            voltage = adc.get_sar_voltage()
            print(f"Напряжение: {voltage:.3f} В")
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        print("\nПрограмма остановлена пользователем.")
    finally:
        
        GPIO.output([26, 20, 19, 16, 13, 12, 25, 11], 0)
        GPIO.cleanup()