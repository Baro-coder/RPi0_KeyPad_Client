#!/usr/bin/python
# -- KeyPad_Client: buttons_handler.py --

from gpiozero import Button, PWMLED
from signal import pause

from menu import Menu

class Buttons_Handler:
    def __init__(self, pin_btn_next : int, pin_btn_prev : int, pin_btn_back : int, pin_btn_select : int, pin_pwmled : int, menu : Menu) -> None:
        # -- Menu
        self.menu = menu

        # -- LED
        self.led = PWMLED(pin_pwmled)
        self.led.pulse()

        # -- Buttons
        self.btn_next = Button(pin_btn_next)
        self.btn_prev = Button(pin_btn_prev)
        self.btn_back = Button(pin_btn_back)
        self.btn_select = Button(pin_btn_select)
        
        self.btn_next.when_pressed = self._press_next
        self.btn_prev.when_pressed = self._press_prev
        self.btn_back.when_pressed = self._press_back
        self.btn_select.when_pressed = self._press_select
        
    # ----------------------------------------------------------
    
        
    def _press_next(self):
        print('Button pressed: NEXT')
        self.menu.next()
    
    
    def _press_prev(self):
        print('Button pressed: PREV')
        self.menu.prev()
    
    
    def _press_back(self):
        print('Button pressed: BACK')
        self.menu.back()
    
    
    def _press_select(self):
        print('Button pressed: SELECT')
        self.menu.select()
    
    
    # ----------------------------------------------------------
    
    def run(self):
        print('KeyPad is ready.\n')
        
        self.menu.update_output()
        
        pause()
        