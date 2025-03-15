import socket
import uuid
import platform


class SystemInfo:
    @staticmethod
    def get_mac_address():
        mac = uuid.getnode()
        mac_address = ':'.join(("%012X" % mac)[i:i+2] for i in range(0, 12, 2))
        return mac_address
    
    @staticmethod
    def get_ip_address():
        try:
            hostname = socket.gethostname()
            ip_address = socket.gethostbyname(hostname)
            return ip_address
        except Exception as e:
            return f"Error: {e}"
        
    @staticmethod
    def get_pc_name():
        return platform.node()