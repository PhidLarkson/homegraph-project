import time
import json
import socket

esp_ip = '192.168.238.181'  # Replace with your ESP32 IP address
esp_port = 10000            # Replace with the port you used

def connect_to_esp():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((esp_ip, esp_port))
    print("Connected to ESP32")
    return sock

def send_to_esp(sock, data):
    sock.sendall(data.encode())
    response = sock.recv(1024)
    print("Received", repr(response))
    return response

def handle_led_control(state):
    sock = connect_to_esp()
    
    # Access the LED status from the nested JSON structure
    led_status = state.get("utility", {}).get("led_status", "A")
    
    if led_status == "A":
        send_to_esp(sock, "A")
    elif led_status == "B":
        send_to_esp(sock, "B")

    elif led_status == "X":
        send_to_esp(sock, "X")
    
    sock.close()

def load_json(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

def monitor_json(file_path, check_interval=1):
    last_state = load_json(file_path)
    while True:
        time.sleep(check_interval)
        current_state = load_json(file_path)
        if current_state != last_state:
            print("Change detected")
            handle_led_control(current_state)
            last_state = current_state

if __name__ == "__main__":
    monitor_json("/home/pnlarbi/Documents/2024-a/ETHACCRA/SmartHome/smart_home/client/detect.json")
