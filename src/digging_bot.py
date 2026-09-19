import os
from flask import Flask, request, jsonify, render_template

# Handle production hardware serial vs local PC emulation mode
try:
    import serial
    HAS_SERIAL = True
except ImportError:
    print("[WARNING] pyserial not found. Running in EMULATION mode.")
    HAS_SERIAL = False

app = Flask(__name__)

# --- UART Serial Port Configuration ---
# On the BeagleY-AI or BBB, look to /dev/ttyS2 or /dev/bone/UART/4 and etc...
SERIAL_PORT = "/dev/bone/uart/4" 
BAUD_RATE = 115200

# Initialize the serial connection interface context handle safely
if HAS_SERIAL and os.path.exists(SERIAL_PORT):
    try:
        ser = serial.Serial(
            port=SERIAL_PORT,
            baudrate=BAUD_RATE,
            timeout=0.1,
            write_timeout=0.1
        )
        print(f"[UART] Serial port opened successfully on {SERIAL_PORT} at {BAUD_RATE} baud.")
    except Exception as e:
        print(f"[ERROR] Could not open serial port {SERIAL_PORT}: {e}")
        ser = None
else:
    ser = None
    if HAS_SERIAL:
        print(f"[WARNING] {SERIAL_PORT} path not found. Defaulting to Emulation console outputs.")

# --- UART Data Transmission Engine ---
def write_to_motors(left_speed, right_speed):
    """
    Formats speeds (-1.0 to 1.0) into a reliable telemetry packet string frame:
    Example String: "M:0.85,-0.40\n"
    """
    if not ser:
        print(f"[EMU UART] Outbound Frame -> L: {left_speed:5.2f} | R: {right_speed:5.2f}")
        return

    try:
        # Construct a standardized structural string frame packet. 
        # Restricting decimals to 2 places minimizes the packet length on the serial bus.
        packet = f"M:{left_speed:.2f},{right_speed:.2f}\n"
        
        # Convert the Python string payload into bytes and transmit across UART
        ser.write(packet.encode('utf-8'))
        ser.flush() # Flush OS buffers to ensure real-time command delivery
        
    except Exception as e:
        print(f"[UART TX ERROR] Failed to stream command packet frame: {e}")

# --- Flask Server Routes ---
@app.route('/')
def index():
    return render_template('dig_em_bot.html')

@app.route('/control', methods=['POST'])
def control_rover():
    try:
        data = request.get_json()
        vector = data.get('action', {})
        
        # Read the telemetry variables generated from your index.html gamepad canvas logic
        left_speed = float(vector.get('left_motor', 0.0))
        right_speed = float(vector.get('right_motor', 0.0))
        
        write_to_motors(left_speed, right_speed)
        return jsonify({"status": "Active"}), 200

    except (TypeError, ValueError) as e:
        return jsonify({"status": "Malformed Command"}), 400
    except Exception as e:
        write_to_motors(0.0, 0.0)
        return jsonify({"status": f"Server Fault: {str(e)}"}), 500

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=5000, debug=False)
    finally:
        print("\n[SHUTDOWN] Sending safety halt command over UART...")
        write_to_motors(0.0, 0.0)
        if ser and ser.is_open:
            ser.close()
