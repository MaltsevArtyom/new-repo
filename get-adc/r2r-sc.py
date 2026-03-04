import RPi.GPIO as GPIO
import time
import matplotlib.pyplot as plt


class R2R_ADC:
    def __init__(self, dynamic_range, compare_time=0.01, verbose=False):
        self.dynamic_range = dynamic_range
        self.verbose = verbose
        self.compare_time = compare_time
      
        self.bits_gpio = [26, 20, 19, 16, 13, 12, 25, 11]
        self.comp_gpio = 21
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.bits_gpio, GPIO.OUT, initial=0)
        GPIO.setup(self.comp_gpio, GPIO.IN)

    def number_to_dac(self, number):
        bits = [int(bit) for bit in bin(number)[2:].zfill(8)]
        GPIO.output(self.bits_gpio, bits)

    def sequential_counting_adc(self):
        for value in range(256):
            self.number_to_dac(value)
            time.sleep(self.compare_time)
            if GPIO.input(self.comp_gpio) == 1:
                return value
        return 255

    def get_sc_voltage(self):
        code = self.sequential_counting_adc()
        return (code / 256.0) * self.dynamic_range


def plot_voltage_vs_time(time_list, voltage_list, max_v):
    plt.figure(figsize=(10, 6))
    plt.plot(time_list, voltage_list)
    plt.title("График зависимости напряжения на входе АЦП от времени")
    plt.xlabel("Время, с")
    plt.ylabel("Напряжение, В")
    plt.xlim(0, max(time_list) if time_list else 1)
    plt.ylim(0, max_v * 1.1)
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    voltage_range = 3.3  
    duration = 5.0       
    
    voltage_values = []
    time_values = []

    
    adc = R2R_ADC(dynamic_range=voltage_range, compare_time=0.0001)

    try:
        print(f"Начало измерения ({duration} сек)...")
        start_time = time.time()
        
        while (time.time() - start_time) < duration:
            v = adc.get_sc_voltage()
            voltage_values.append(v)
            time_values.append(time.time() - start_time)
            
        print("Измерение окончено. Рисую график...")
        plot_voltage_vs_time(time_values, voltage_values, voltage_range)

    finally:
        
        GPIO.output([26, 20, 19, 16, 13, 12, 25, 11], 0)
        GPIO.cleanup()
        print("Программа завершена.")