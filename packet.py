# Simple Network Packet Analyzer by SurajInCode
import threading
import keyboard  # For detecting the Esc key press
from scapy.all import sniff, IP, TCP, UDP, Raw

# Create a stop event
stop_sniffing_event = threading.Event()

def analyze_packet(packet):
    if packet.haslayer(IP):
        src_ip = packet[IP].src
        dst_ip = packet[IP].dst
        protocol = packet[IP].proto

        print(f"=== Packet Information ===")
        print(f"Source IP: {src_ip} | Destination IP: {dst_ip} | Protocol: {protocol}")

        # Check for TCP packets
        if packet.haslayer(TCP):
            try:
                payload = packet[Raw].load
                decoded_payload = payload.decode('utf-8', 'ignore')
                print("TCP Payload: ", decoded_payload)
            except (IndexError, UnicodeDecodeError):
                print("Unable to decode TCP payload.")

        # Check for UDP packets
        elif packet.haslayer(UDP):
            try:
                payload = packet[Raw].load
                decoded_payload = payload.decode('utf-8', 'ignore')
                print("UDP Payload: ", decoded_payload)
            except (IndexError, UnicodeDecodeError):
                print("Unable to decode UDP payload.")

        print("==========================\n")

def stop_sniffing(pkt):
    """Check if stop event is set to stop sniffing."""
    return stop_sniffing_event.is_set()

def start_sniffing():
    """Start sniffing packets and analyze them."""
    print("Starting packet sniffing... Press 'Esc' to stop.")
    sniff(prn=analyze_packet, store=False, stop_filter=stop_sniffing)

def check_for_esc_key():
    """Monitor for the 'Esc' key press to stop sniffing."""
    keyboard.wait('esc')  # Block until 'Esc' is pressed
    stop_sniffing_event.set()
    print("Esc key pressed. Stopping packet sniffing...")

# Start the sniffing process in a separate thread
sniff_thread = threading.Thread(target=start_sniffing)
sniff_thread.start()

# Monitor for 'Esc' key press in the main thread
check_for_esc_key()

# Wait for the sniffing thread to finish
sniff_thread.join()
