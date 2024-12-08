from flask import Flask, render_template, request, jsonify
from pymodbus.client import ModbusTcpClient, ModbusSerialClient

app = Flask(__name__)

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


def getCurrentGear():
    try:
        if client.connect():
            response = client.read_holding_registers(address=ADDRESS, count=1, slave=SLAVE_ID)
            if not response.isError():
                return response.registers[0]
            else:
                return {"error": "Error reading current gear"}
        else:
            return {"error": "Failed to connect to the e-shifter"}
    finally:
        client.close()


def shiftGear(gear):
    try:
        if client.connect():
            response = client.write_register(address=ADDRESS, value=gear, slave=SLAVE_ID)
            if not response.isError():
                return {"success": f"Gear shifted to {gear}"}
            else:
                return {"error": "Error shifting gear"}
        else:
            return {"error": "Failed to connect to the e-shifter"}
    finally:
        client.close()


def testGearSequence():
    sequence = [1, 2, 3, 2, 1]
    results = []

    try:
        if client.connect():
            for gear in sequence:
                response = client.write_register(address=ADDRESS, value=gear, slave=SLAVE_ID)
                if response.isError():
                    results.append({"gear": gear, "status": "Error", "message": "Failed to shift gear"})
                else:
                    check_response = client.read_holding_registers(address=ADDRESS, count=1, slave=SLAVE_ID)
                    if not check_response.isError() and check_response.registers[0] == gear:
                        results.append({"gear": gear, "status": "Success"})
                    else:
                        results.append({"gear": gear, "status": "Error", "message": "Gear mismatch"})
        else:
            return {"error": "Failed to connect to the e-shifter"}
    finally:
        client.close()

    return results


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/get_gear', methods=['GET'])
def getGear():
    result = getCurrentGear()
    if isinstance(result, dict) and 'error' in result:
        return jsonify(result), 500
    return jsonify({"current_gear": result}), 200


@app.route('/shift_gear', methods=['POST'])
def shift():
    gear = request.json.get('gear')
    if gear is None or not (0 <= gear <= 3):
        return jsonify({"error": "Invalid gear value"}), 400
    result = shiftGear(gear)
    return jsonify(result), (200 if "success" in result else 500)


@app.route('/test_sequence', methods=['POST'])
def test_sequence():
    results = testGearSequence()
    if isinstance(results, dict) and "error" in results:
        return jsonify(results), 500
    return jsonify({"results": results}), 200


if __name__ == '__main__':
    app.run(debug=True)
