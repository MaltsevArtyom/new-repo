import RPi.GPIO as GPIO 


dac_bits = [22, 27, 17, 26, 25, 21, 20, 16]


dynamic_range = 3.18


GPIO.setmode(GPIO.BCM)
GPIO.setup(dac_bits, GPIO.OUT)


def voltage_to_number(voltage):
    if not (0.0 <= voltage <= dynamic_range):
        print(f"Напряжение выходит за динамический диапазон ЦАП (0.00 - {dynamic_range:.2f} B)")
        print("Устанавливаем 0.0 В")
        return 0
    
    
    return int(voltage / dynamic_range * 255)

def number_to_dac(value):
    binary_str = bin(value)[2:].zfill(8)
    bits = [int(bit) for bit in binary_str[::-1]]
    
    
    for i in range(8):
        GPIO.output(dac_bits[i], bits[i])


try:
    while True:
        try:
            line = input("Введите напряжение в Вольтах (например, 1.5): ")
            voltage = float(line)
            
            number = voltage_to_number(voltage)
            
            number_to_dac(number)
            print(f"На ЦАП подано значение: {number}")
            
        except ValueError:
            print("Вы ввели не число. Попробуйте ещё раз\n")

finally:
    GPIO.output(dac_bits, 0)
    GPIO.cleanup()