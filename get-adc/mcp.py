import smbus
import time
import matplotlib.pyplot as plt

class MCP3021_Plotter:
    def init(self, v_ref=5.0):
        # Инициализация I2C шины (номер 1 для Raspberry Pi)
        self.bus = smbus.SMBus(1)
        self.address = 0x4D # Стандартный адрес устройства
        self.v_ref = v_ref
        
    def read_voltage(self):
        """Чтение 10-битного значения и перевод в Вольты."""
        # Читаем 2 байта данных
        data = self.bus.read_word_data(self.address, 0)
        
        # Переставляем байты (SMBus читает их в обратном порядке для этой микросхемы)
        lower_byte = (data >> 8) & 0xFF
        upper_byte = data & 0xFF
        
        # Сборка 10 бит: [D9 D8 D7 D6 D5 D4 D3 D2] [D1 D0 X X X X X X]
        # Результат = (Upper << 2) | (Lower >> 6) - стандарт для MCP3021
        raw_value = ((upper_byte << 2) | (lower_byte >> 6)) & 0x3FF
        
        # Перевод в напряжение: (Число / 1024) * V_ref
        return (raw_value / 1024.0) * self.v_ref

# --- Основной цикл программы ---
if name == "main":
    # Укажи здесь точное напряжение питания, измеренное мультиметром!
    REAL_VREF = 5.0 
    DURATION = 5.0 # Время сбора данных в секундах
    
    adc = MCP3021_Plotter(v_ref=REAL_VREF)
    
    voltages = []
    timestamps = []
    
    try:
        print(f"Начинаю сбор данных (10-бит) на {DURATION} сек...")
        start_time = time.time()
        
        while (time.time() - start_time) < DURATION:
            current_time = time.time() - start_time
            v = adc.read_voltage()
            
            voltages.append(v)
            timestamps.append(current_time)
            
            # Небольшая пауза, чтобы не перегружать шину I2C
            time.sleep(0.01)
            
        print(f"Готово! Собрано {len(voltages)} точек.")
        
        # Построение графика
        plt.figure(figsize=(10, 6))
        plt.plot(timestamps, voltages, label='Входной сигнал', color='blue')
        plt.title(f"График напряжения (10-битный АЦП MCP3021)\n$V_{{ref}}$ = {REAL_VREF}В")
        plt.xlabel("Время (сек)")
        plt.ylabel("Напряжение (В)")
        plt.ylim(0, REAL_VREF + 0.1)
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.legend()
        plt.show()

    except Exception as e:
        print(f"Произошла ошибка: {e}")
    finally:
        print("Программа завершена.")