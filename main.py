#!/usr/bin/python
# -- KeyPad_Client: main.py --

import sys
import configparser as cfgp

from tcp_client import TCP_Client
from menu import Menu
from buttons_handler import Buttons_Handler


APP_DIR = '/home/pi/.Private/RPi0_KeyPad_Client'
CONFIG_FILE = f'{APP_DIR}/config.ini'


def config_init():
    try:
        config = cfgp.ConfigParser()

        config.read(CONFIG_FILE)

        # TCP Server
        global HOST, PORT, FORMAT, BUFFER_SIZE
        
        HOST = config['TCP Server']['host']
        PORT = int(config['TCP Server']['port'])
        FORMAT = config['TCP Server']['format']
        BUFFER_SIZE = int(config['TCP Server']['buffer_size'])
        
        # RPi KeyPad
        global BUTTON_NEXT_PIN, BUTTON_PREV_PIN, BUTTON_BACK_PIN, BUTTON_SELECT_PIN
        
        BUTTON_NEXT_PIN = int(config['RPi KeyPad']['pin_button_next'])
        BUTTON_PREV_PIN = int(config['RPi KeyPad']['pin_button_prev'])
        BUTTON_BACK_PIN = int(config['RPi KeyPad']['pin_button_back'])
        BUTTON_SELECT_PIN = int(config['RPi KeyPad']['pin_button_select'])
        
        # RPi LED
        global PIN_PWMLED
        
        PIN_PWMLED = int(config['RPi LED']['pin_pwmled'])
    
    except KeyError as e:
        sys.stderr.write('-- Config Key Error --')
        sys.stderr.write(str(e))
        sys.exit(1)
    
    except Exception as e:
        sys.stderr.write('-- Unexpected Error Config --')
        sys.stderr.write(str(type(e)))
        sys.stderr.write(str(e))
        sys.exit(1)


def main():
    # -- Config
    print('Reading config... ', end='')
    config_init()
    print('Done.')
    
    # -- TCP Client
    print('Setting up the TCP Client... ', end='')
    client = TCP_Client(HOST, PORT, BUFFER_SIZE, FORMAT)
    print('Done.')
    
    # -- Menu
    print('Setting up the Menu manager... ', end='')
    menu = Menu(client)
    print('Done.')
    
    # -- KeyPad
    print('Setting up the KeyPad... ', end='')
    btn_handler = Buttons_Handler(BUTTON_NEXT_PIN, BUTTON_PREV_PIN, BUTTON_BACK_PIN, BUTTON_SELECT_PIN, PIN_PWMLED, menu)
    print('Done.\n')
    
    try:
        btn_handler.run()
        
    except KeyboardInterrupt:
        btn_handler.led.value = 1
        print('-- Manually Interrupt --')
    
    except Exception as e:
        sys.stderr.write('-- Unexpected Error Client --')
        sys.stderr.write(str(type(e)))
        sys.stderr.write(str(e))
        sys.exit(1)
        

if __name__ == '__main__':
    main()
    sys.exit(0)