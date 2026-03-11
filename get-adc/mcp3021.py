import smbus
import time

class MCP3021:
    def __init__(self, dynamic_range, verbose=False):
        self.bus = smbus.SMBus(1)
        self.dynamic_range = dynamic_range
        self.address = 0x4D 
        self.verbose = verbose

    def deinit(self):
        self.bus.close()

    def get_number(self):
        data = self.bus.read_word_data(self.address, 0)
        
        lower_data_byte = data >> 8
        upper_data_byte = data & 0xFF
        
        number = (upper_data_byte << 6) | (lower_data_byte >> 2)
        
        if self.verbose:
            print(f"Принятые данные: {data}, Старший: {upper_data_byte:x}, Младший: {lower_data_byte:x}, Число: {number}")
            
        return number

    def get_voltage(self):
        number = self.get_number()
        return (number / 1024.0) * self.dynamic_range

if __name__ == "__main__":
    V_REF = 5.0 
    
    adc = MCP3021(dynamic_range=V_REF)
    
    try:
        print("Чтение напряжения с MCP3021 (10-bit I2C)...")
        while True:
            voltage = adc.get_voltage()
            print(f"Напряжение: {voltage:.3f} В")
            time.sleep(1) # Пауза 1с, чтобы не перегружать терминал
            
    except KeyboardInterrupt:
        print("\nОстановка...")
    finally:
       
        adc.deinit()