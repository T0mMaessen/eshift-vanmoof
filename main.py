from pymodbus.client import ModbusTcpClient, ModbusSerialClient

SLAVE_ID = 0x20
ADDRESS = 0x02

# SERVER_HOST = 'localhost'
# SERVER_PORT = 5020
# UNIT_ID = 6
#
# client = ModbusTcpClient(
#     host=SERVER_HOST,
#     port=SERVER_PORT,
#     timeout=1
# )


SERIAL_PORT = '/dev/serial0'  # GPIO seriële poort
BAUDRATE = 9600

client = ModbusSerialClient(
    port=SERIAL_PORT,       # Bijvoorbeeld: "/dev/ttyUSB0" of "COM3"
    baudrate=BAUDRATE,      # Typisch: 9600, 19200, etc.
    parity='N',             # 'N' voor geen pariteit, 'E' voor even, 'O' voor oneven
    stopbits=1,             # Typisch 1 of 2
    bytesize=8,             # Meestal 8
    timeout=1               # Timeout in seconden
)

def getCurrentGear():
    try:
        print("Verbinden met de e-shifter...")

        if client.connect():
            print("Verbonden")
            response = client.read_holding_registers(address=ADDRESS, count=1, slave=SLAVE_ID)
            if not response.isError():
                current_gear = response.registers[0]
                print("Huidige versnelling:", current_gear)
            else:
                print("Fout bij het lezen van de huidige versnelling:", response)
        else:
            print("Fout bij het verbinden met de e-shifter")
    finally:
        client.close()
        print("Verbinding verbroken")


def shiftGear(gear):
    try:
        print("Verbinden met de e-shifter...")

        if client.connect():
            print("Verbonden")
            response = client.write_register(address=ADDRESS, value=gear, slave=ADDRESS)
            if not response.isError():
                print("Versnelling gewijzigd naar:", gear)
            else:
                print("Fout bij het schakelen van de versnelling:", response)
        else:
            print("Fout bij het verbinden met de e-shifter")
    finally:
        client.close()
        print("Verbinding verbroken")


def main():
    while True:
        print("1. Huidige versnelling")
        print("2. Versnelling wijzigen")
        print("3. Stoppen")

        choice = input("Keuze: ")

        if choice == '1':
            getCurrentGear()
        elif choice == '2':
            gear = int(input("Nieuwe versnelling: "))
            shiftGear(gear)
        elif choice == '3':
            break
        else:
            print("Ongeldige keuze")


if __name__ == '__main__':
    main()
