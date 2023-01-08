import pyshark
import socket
from datetime import datetime
from packet import Packet


def chatClientMultiMessage(tx_paquet):
    # InstanceID
    instance_id = tx_paquet.readUnsignedInt()
    # packet length
    packet_length = tx_paquet.readLength()
    # Contenu du message chat
    content = tx_paquet.readUTF()
    # Channel ID
    channel_id = tx_paquet.readByte()
    
    #   public static const CHANNEL_GLOBAL:uint = 0;
    #   public static const CHANNEL_TEAM:uint = 1;
    #   public static const CHANNEL_GUILD:uint = 2;
    #   public static const CHANNEL_ALLIANCE:uint = 3;
    #   public static const CHANNEL_PARTY:uint = 4;
    #   public static const CHANNEL_SALES:uint = 5;
    #   public static const CHANNEL_SEEK:uint = 6;
    #   public static const CHANNEL_NOOB:uint = 7;
    #   public static const CHANNEL_ADMIN:uint = 8;
    #   public static const CHANNEL_ADS:uint = 12;
    #   public static const CHANNEL_ARENA:uint = 13;
    #   public static const CHANNEL_COMMUNITY:uint = 14;
    
    print(f"{datetime.now().strftime('%H:%M:%S')} [DEBUG] TX: ChatClientMultiMessage | InstanceID: {instance_id} | Channel ID: {channel_id} | Packet Length: {packet_length} | Content: {content}")

def chatServerMessage(rx_paquet):
    # packet length
    packet_length = rx_paquet.readLength()
    # channel ID
    channel_id = rx_paquet.readByte()
    # content
    content = rx_paquet.readUTF()
    # timestamp
    timestamp = rx_paquet.readInt()
    # finger print
    fingerprint = rx_paquet.readUTF()
    # sender id
    sender_id = rx_paquet.readDouble()
    # sender name
    sender_name = rx_paquet.readUTF()
    # prefix
    prefix = rx_paquet.readUTF()
    # account id
    account_id = rx_paquet.readInt()
    
    # print(f"{datetime.now().strftime('%H:%M:%S')} [DEBUG] RX: ChatServerMessage | Packet Length: {packet_length} | Channel ID: {channel_id} | Content: {content} | Timestamp: {timestamp} | Fingerprint: \
    #     {fingerprint} | Sender ID: {sender_id} | Sender Name: {sender_name} | Prefix: {prefix} | Account ID: {account_id}")
    if channel_id == 0:
        print(f"(Général) {sender_name}: {content}")
    elif channel_id == 1:
        print(f"(Equipe) {sender_name}: {content}")    
    elif channel_id == 5:
        print(f"(Commerce) {sender_name}: {content}")        
    elif channel_id == 6:
        print(f"(Recrutement) {sender_name}: {content}")    
        
        
def sniffer_parsed():
    capture = pyshark.LiveCapture(bpf_filter='tcp port 5555 and len > 66')
    # Version continu
    for packet in capture.sniff_continuously():
                if packet.ip.src == socket.gethostbyname(socket.gethostname()):         
                    tx_paquet = Packet(bytes.fromhex(packet.tcp.payload.raw_value))
                    
                    if tx_paquet.packet_id == 4757:
                        chatClientMultiMessage(tx_paquet)
                    

                else:
                    rx_paquet = Packet(bytes.fromhex(packet.tcp.payload.raw_value))
                    
                    if rx_paquet.packet_id == 6743:
                        chatServerMessage(rx_paquet)
                        
                    elif rx_paquet.packet_id == 3522:
                        pass    # ChatServerWithObjectMessage
                    
                    else:
                        print(packet.tcp.payload)    
 
def sniffer_raw():            
    capture = pyshark.LiveCapture(bpf_filter='tcp port 5555 and len > 66')
    # Version continu
    for packet in capture.sniff_continuously():
                if packet.ip.src == socket.gethostbyname(socket.gethostname()):         
                    print(f"[DEBUG] Paquet Dofus Envoyé: {packet.tcp.payload}")
                else:
                    print(f"[DEBUG] Paquet Dofus Reçu: {packet.tcp.payload}")            
     

def from_client(origin):
    return origin.getpeername()[0] == "127.0.0.1"     
     
def direction(origin):
    if from_client(origin):
        return "TX: "
    else:
        return "RX: "  
     

                
                
        for c in conns:
            c.close()     

        
