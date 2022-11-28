from enum import Enum
import socket


class NetOption(Enum):
    HOSTNAME = 0
    IP = 1
    HOSTNAME_IP = 2


class SectionManager:
    HEADER = 'NET'
    option_id = 0
    
    @staticmethod
    def next_option():
        SectionManager.option_id += 1
        if SectionManager.option_id == 3:
            SectionManager.option_id = 0
            
    @staticmethod
    def prev_option():
        SectionManager.option_id -= 1
        if SectionManager.option_id == -1:
            SectionManager.option_id = 2
    
    
    @staticmethod
    def get_option_header():
        return f'{NetOption(SectionManager.option_id).value + 1}: {NetOption(SectionManager.option_id).name}'
    
    
    @staticmethod
    def get_option_output():
        if SectionManager.option_id == NetOption.HOSTNAME.value:
            output = SectionManager._get_hostname()
            
        elif SectionManager.option_id == NetOption.IP.value:
            output = SectionManager._get_ip_addr()
            
        elif SectionManager.option_id == NetOption.HOSTNAME_IP.value:
            output = f'{SectionManager._get_hostname()} : {SectionManager._get_ip_addr()}'
            
        return output.center(24)
            
    
    @staticmethod
    def _get_hostname():
        return socket.gethostname()


    @staticmethod
    def _get_ip_addr():
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0)
        try:
            s.connect(('10.254.254.254', 1))
            IP = s.getsockname()[0]
        except Exception:
            IP = '127.0.0.1'
        finally:
            s.close()
        return IP
    
