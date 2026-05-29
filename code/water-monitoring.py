"""
Smart Water Quality Monitoring System

Platform: Raspberry Pi Pico W
Language: MicroPython

Sensors:
- pH Sensor
- TDS Sensor
- DS18B20
- DHT11
"""

from machine import Pin, I2C, ADC
import time
import dht
from ds18x20 import DS18X20
import onewire

# Initialize I2C for LCD
i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=400000)

# Initialize DHT11 sensor for air temperature (GPIO 15)
dht_sensor = dht.DHT11(Pin(15))

# Initialize DS18B20 sensor for water temperature (GPIO 2)
ow = onewire.OneWire(Pin(2))
ds = DS18X20(ow)

# Initialize ADC for pH and TDS sensors
ph_sensor = ADC(Pin(26))   # pH sensor
tds_sensor = ADC(Pin(27))  # TDS sensor


def read_air_temperature():
    dht_sensor.measure()
    return dht_sensor.temperature()


def read_water_temperature():
    roms = ds.scan()

    if not roms:
        return None

    ds.convert_temp()
    time.sleep(1)

    return ds.read_temp(roms[0])


def read_ph_value():
    ph_raw = ph_sensor.read_u16()

    voltage = (ph_raw / 65535) * 3.3

    # Example calibration formula
    ph_value = -5.70 * voltage + 20.0

    return ph_value


def read_tds_value():
    tds_raw = tds_sensor.read_u16()

    voltage = (tds_raw / 65535) * 3.3

    if voltage > 2.3:
        voltage = 2.3

    voltage = voltage * (2.3 / 3.3)

    tds_value = (
        133.42 * voltage**3
        - 255.86 * voltage**2
        + 857.39 * voltage
    )

    return tds_value


while True:

    air_temp = read_air_temperature()
    water_temp = read_water_temperature()
    ph_value = read_ph_value()
    tds_value = read_tds_value()

    print("Air Temperature: {}°C".format(air_temp))

    if water_temp is not None:
        print("Water Temperature: {:.2f}°C".format(water_temp))
    else:
        print("Water Temperature Sensor Not Detected")

    print("pH Value: {:.2f}".format(ph_value))
    print("TDS Value: {:.2f} ppm".format(tds_value))

    # Optional LCD Display
    # lcd.clear()
    # lcd.putstr("Air: {}C".format(air_temp))

    time.sleep(5)
