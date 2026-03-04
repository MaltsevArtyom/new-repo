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


def plot_voltage_vs_time(time_list, voltage_list, max_v):
   
    plt.figure(figsize=(10, 6))
    plt.plot(time_list, voltage_list)
    plt.title("Зависимость напряжения на входе АЦП от времени (SAR)")
    plt.xlabel("Время, с")
    plt.ylabel("Напряжение, В")
    plt.ylim(0, max_v + 0.2) 
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    V_REF = 3.3       
    DURATION = 3.0    
    
    
    adc = R2R_ADC(dynamic_range=V_REF, compare_time=0.0001)
    
    
    voltage_values = []
    time_values = []
    
    try:
        print(f"Начинаем измерение (SAR) на {DURATION} сек...")
        start_t = time.time() 
        
        while (time.time() - start_t) < DURATION:

            v = adc.get_voltage()
            t = time.time() - start_t
            
            
            voltage_values.append(v)
            time_values.append(t)
            
        print(f"Измерение завершено. Сделано {len(voltage_values)} замеров.")
        
        
        plot_voltage_vs_time(time_values, voltage_values, V_REF)
        
    finally:
      
        GPIO.output([26, 20, 19, 16, 13, 12, 25, 11], 0)
        GPIO.cleanup()
        print("GPIO успешно очищены.")