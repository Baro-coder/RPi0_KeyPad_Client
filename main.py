#!/usr/bin/python
# -- KeyPad_Client: main.py --

import sys
import configparser as cfgp

from tcp_client import TCP_Client
from menu import Menu
from buttons_handler import Buttons_Handler


CONFIG_FILE = './config.ini'


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
    
    except KeyError as e:
        print('-- Config Error --')
        print(e)
    
    except Exception as e:
        print('-- Unexpected Error Config --')
        print(type(e))
        print(e)
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
    btn_handler = Buttons_Handler(BUTTON_NEXT_PIN, BUTTON_PREV_PIN, BUTTON_BACK_PIN, BUTTON_SELECT_PIN, menu)
    print('Done.')
    
    
    try:
        btn_handler.run()
        
    except KeyboardInterrupt:
        print('-- Manually Interrupt --')
    
    except Exception as e:
        print('-- Unexpected Error Server --')
        print(type(e))
        print(e)
        sys.exit(1)
        

if __name__ == '__main__':
    main()
    sys.exit(0)