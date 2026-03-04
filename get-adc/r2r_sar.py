import RPi.GPIO as GPIO
import time
import matplotlib.pyplot as plt

class R2R_ADC:
    def __init__(self, dynamic_range, compare_time=0.0001):
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

    def get_voltage(self):
        
        code = self.successive_approximation_adc()
        return (code / 256.0) * self.dynamic_range


if __name__ == "__main__":
    V_REF = 3.3
    DURATION = 3.0
    
    adc = R2R_ADC(dynamic_range=V_REF)
    voltage_values = []
    time_values = []
    
    try:
        print(f"Старт замера (SAR) на {DURATION} сек...")
        start_t = time.time()
        
        while (time.time() - start_t) < DURATION:
            voltage_values.append(adc.get_voltage())
            time_values.append(time.time() - start_t)
            
    
        sampling_periods = [time_values[i] - time_values[i-1] for i in range(1, len(time_values))]
        
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10))
        
       
        ax1.plot(time_values, voltage_values)
        ax1.set_title("Напряжение (Алгоритм SAR)")
        ax1.set_ylabel("Вольты")
        ax1.grid(True)
        
        
        ax2.hist(sampling_periods, bins=50, range=(0, 0.01)) 
        ax2.set_title("Гистограмма периодов (SAR)")
        ax2.set_xlabel("Время одного измерения, с")
        ax2.grid(True)
        
        plt.tight_layout()
        plt.show()

    finally:
        GPIO.cleanup()