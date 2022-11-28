#!/usr/bin/python
# -- KeyPad_Client: buttons_handler.py --

from gpiozero import Button, PWMLED
from signal import pause

from menu import Menu

class Buttons_Handler:
    def __init__(self, pin_btn_next : int, pin_btn_prev : int, pin_btn_back : int, pin_btn_select : int, menu : Menu) -> None:
        self.menu = menu

        self.btn_next = Button(pin_btn_next)
        self.btn_prev = Button(pin_btn_prev)
        self.btn_back = Button(pin_btn_back)
        self.btn_select = Button(pin_btn_select)
        
        self.led = PWMLED(13)
        self.led.pulse()
        
        self.btn_next.when_pressed = self._press_next
        self.btn_prev.when_pressed = self._press_prev
        self.btn_back.when_pressed = self._press_back
        self.btn_select.when_pressed = self._press_select
        
        self.menu.update_output()
        
    # ----------------------------------------------------------
    
        
    def _press_next(self):
        print('Button NEXT')
        
        self.menu.next()
    
    
    def _press_prev(self):
        print('Button PREV')
        
        self.menu.prev()
    
    
    def _press_back(self):
        print('Button BACK')
        
        self.menu.back()
    
    
    def _press_select(self):
        print('Button SELECT')
        
        self.menu.select()
    
    
    # ----------------------------------------------------------
    
    def run(self):
        print('KeyPad is ready.\n')
        pause()
        