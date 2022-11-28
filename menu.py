#!/usr/bin/python
# -- KeyPad_Client: menu.py --

from enum import Enum

from tcp_client import TCP_Client

from modules.net import net
from modules.clock import clock
from modules.college_plan import plan
from modules.crypto import crypto


class MenuSections(Enum):
    CLOCK = 0
    NET = 1
    COLLEGE_PLAN = 2
    CRYPTO = 3

class Menu:
    def __init__(self, tcp_client : TCP_Client) -> None:
        self.client = tcp_client
        
        self.section = MenuSections.CLOCK
    
        self.in_sections = True
        
        
    def next(self):
        if self.in_sections:
            self.section_id += 1
            if self.section_id == 4:
                self.section_id = 0
            
        else:
            if self.section == MenuSections.CLOCK:
                clock.SectionManager.next_option()
            
            elif self.section == MenuSections.NET:
                net.SectionManager.next_option()
            
            elif self.section == MenuSections.COLLEGE_PLAN:
                plan.SectionManager.next_option()
                
            elif self.section == MenuSections.CRYPTO:
                crypto.SectionManager.next_option()
            
        self.update_output()
            
            
    def prev(self):
        if self.in_sections:
            self.section_id -= 1
            if self.section_id == -1:
                self.section_id = 3
        
        else:
            if self.section == MenuSections.CLOCK:
                clock.SectionManager.prev_option()
            
            elif self.section == MenuSections.NET:
                net.SectionManager.prev_option()
            
            elif self.section == MenuSections.COLLEGE_PLAN:
                plan.SectionManager.prev_option()
                
            elif self.section == MenuSections.CRYPTO:
                crypto.SectionManager.prev_option()
        
        self.update_output()
        
        
    def back(self):
        self.in_sections = True
        self.update_output()
    
    
    def select(self):
        self.in_sections = False
        self.update_output()
        
    
    
    def update_output(self):
        if self.section == MenuSections.CLOCK:
            if self.in_sections:
                output = (clock.SectionManager.HEADER, clock.SectionManager.get_option_header())
                
            else:
                output = (clock.SectionManager.HEADER, clock.SectionManager.get_output())
                
        if self.section == MenuSections.NET:
            if self.in_sections:
                output = (net.SectionManager.HEADER, net.SectionManager.get_option_header())
                
            else:
                output = (net.SectionManager.HEADER, net.SectionManager.get_option_output())
            
        if self.section == MenuSections.COLLEGE_PLAN:
            if self.in_sections:
                output = (plan.SectionManager.HEADER, plan.SectionManager.get_option_header())
                
            else:
                output = (plan.SectionManager.HEADER, plan.SectionManager.get_option_output())
            
        if self.section == MenuSections.CRYPTO:
            if self.in_sections:
                output = (crypto.SectionManager.HEADER, crypto.SectionManager.get_option_header())
                
            else:
                output = (crypto.SectionManager.HEADER, crypto.SectionManager.get_option_output())
            
        
        print('OUTPUT:')
        print(f'\t{output[0].center(24)}')
        print(f'\t{output[1].center(24)}\n')
        
        self.client.send(row=0, text=output[0].center(24))
        self.client.send(row=1, text=output[1].center(24))
