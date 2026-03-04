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

    def sequential_counting_adc(self):
        for value in range(256):
            self.number_to_dac(value)
            time.sleep(self.compare_time) 
            
            if GPIO.input(self.comp_gpio) == 1:
                return value
        return 255

    def get_voltage(self):
        code = self.sequential_counting_adc()
        # Формула: V = (Code / 2^N) * Range
        return (code / 256.0) * self.dynamic_range


def plot_data(time_vals, volt_vals, sampling_periods, max_v):
    """Строит два графика: вольтаж/время и гистограмму периодов."""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10))
    plt.subplots_adjust(hspace=0.4)

   
    ax1.plot(time_vals, volt_vals, color='tab:blue', linewidth=1)
    ax1.set_title("Зависимость напряжения на входе АЦП от времени")
    ax1.set_xlabel("Время, с")
    ax1.set_ylabel("Напряжение, В")
    ax1.set_ylim(0, max_v * 1.1)
    ax1.grid(True)

    ax2.hist(sampling_periods, bins=50, color='tab:orange', edgecolor='black')
    ax2.set_title("Распределение периодов дискретизации")
    ax2.set_xlabel("Период измерения, с")
    ax2.set_ylabel("Количество измерений")
    ax2.set_xlim(0, 0.06) 
    ax2.grid(True)

    plt.show()

if __name__ == "__main__":
    V_REF = 3.3      
    DURATION = 5.0   
    
    adc = R2R_ADC(dynamic_range=V_REF, compare_time=0.0001)
    
    voltage_values = []
    time_values = []
    
    try:
        print(f"Сбор данных запущен на {DURATION} сек...")
        start_time = time.time()
        
        while (time.time() - start_time) < DURATION:
            current_t = time.time() - start_time
            v = adc.get_voltage()
            
            voltage_values.append(v)
            time_values.append(current_t)
        
        
        sampling_periods = [time_values[i] - time_values[i-1] for i in range(1, len(time_values))]
        
        print(f"Сбор завершен. Сделано измерений: {len(voltage_values)}")
        plot_data(time_values, voltage_values, sampling_periods, V_REF)

    finally:
        
        GPIO.output([26, 20, 19, 16, 13, 12, 25, 11], 0)
        GPIO.cleanup()
        print("GPIO очищены.")