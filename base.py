from pymodbus.client import ModbusTcpClient, ModbusSerialClient

SLAVE_ID = 0x20
ADDRESS = 0x02

# FOR THE TCP VERSION (server simulation)
SERVER_HOST = 'localhost'
SERVER_PORT = 5020

client = ModbusTcpClient(
    host=SERVER_HOST,
    port=SERVER_PORT,
    timeout=1
)


# FOR THE SERIAL VERSION
# SERIAL_PORT = '/dev/cu.usbserial-14420'
# BAUDRATE = 9600
#
# client = ModbusSerialClient(
#     port=SERIAL_PORT,
#     baudrate=BAUDRATE,
#     parity='N',
#     stopbits=1,
#     bytesize=8,
# )

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
            response = client.write_register(address=ADDRESS, value=gear, slave=SLAVE_ID)
            if not response.isError():
                print("Versnelling gewijzigd naar:" + str(gear))
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

            if gear > 3:
                print("Ongeldige versnelling")
                continue

            shiftGear(gear)
        elif choice == '3':
            break
        else:
            print("Ongeldige keuze")


if __name__ == '__main__':
    main()
