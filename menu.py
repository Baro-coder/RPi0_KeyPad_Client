#!/usr/bin/python
# -- KeyPad_Client: menu.py --

from enum import Enum
from time import sleep
import threading as thr


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
    HEADER = 'MENU'
    
    
    def __init__(self, tcp_client : TCP_Client) -> None:
        self.client = tcp_client
        
        self.section_id = 0
        self.section = MenuSections(self.section_id)
    
        self.in_sections = True
        self.in_options = False
        
        self.child_Thread = None
        
        
        
    def next(self):
        if self.in_sections:
            self.section_id += 1
            if self.section_id == 4:
                self.section_id = 0
            self.section = MenuSections(self.section_id)
            
        elif self.in_options:
            if self.section == MenuSections.CLOCK:
                clock.SectionManager.next_option()
            
            elif self.section == MenuSections.NET:
                net.SectionManager.next_option()
            
            elif self.section == MenuSections.COLLEGE_PLAN:
                plan.SectionManager.next_option()
                
            elif self.section == MenuSections.CRYPTO:
                crypto.SectionManager.next_option()
        
        else:
            # TODO:
            #   Suboptions setter for: college_plan
            return
            
        self.update_output()
            
            
    def prev(self):
        if self.in_sections:
            self.section_id -= 1
            if self.section_id == -1:
                self.section_id = 3
            self.section = MenuSections(self.section_id)
        
        elif self.in_options:
            if self.section == MenuSections.CLOCK:
                clock.SectionManager.prev_option()
            
            elif self.section == MenuSections.NET:
                net.SectionManager.prev_option()
            
            elif self.section == MenuSections.COLLEGE_PLAN:
                plan.SectionManager.prev_option()
                
            elif self.section == MenuSections.CRYPTO:
                crypto.SectionManager.prev_option()
                
        else:
            # TODO:
            #   Suboptions setter for: college_plan
            return
        
        self.update_output()
        
        
    def back(self):
        if self.in_sections:
            self.in_sections = True
            self.in_options = False
            
        elif self.in_options:
            self.in_sections = True
            self.in_options = False
            
        else:
            self.threaded = False # for subprocess
            
            self.in_sections = False
            self.in_options = True
        
        self.update_output()
    
    
    def select(self):
        if self.in_sections:
            self.in_sections = False
            self.in_options = True
            
        elif self.in_options:
            self.threaded = True # for subprocess
            
            self.in_sections = False
            self.in_options = False
            
        else:
            self.in_sections = False
            self.in_options = False
        
        self.update_output()
    
    
    def _thread_task(self):
        while True:
            if not self.threaded:
                print(f'{self.child_Thread.name} : STOP')
                break
            
            if self.section == MenuSections.CLOCK:
                output = (f'{clock.SectionManager.HEADER}:', clock.SectionManager.get_option_output())

            if self.section == MenuSections.NET:
                output = (f'{net.SectionManager.HEADER}:', net.SectionManager.get_option_output())

            if self.section == MenuSections.COLLEGE_PLAN:
                output = (f'{plan.SectionManager.HEADER}:', plan.SectionManager.get_option_output())

            if self.section == MenuSections.CRYPTO:
                output = (f'{crypto.SectionManager.HEADER}:', crypto.SectionManager.get_option_output())

            self.client.send(row=0, text=output[0])
            self.client.send(row=1, text=output[1])
            
            sleep(1)
    
    
    def update_output(self):
        if self.section == MenuSections.CLOCK:
            if self.in_sections:
                output = (f'-- {Menu.HEADER} --', f'{self.section_id + 1}: {clock.SectionManager.HEADER}')
                
            elif self.in_options:
                output = (f'-- {clock.SectionManager.HEADER} --', clock.SectionManager.get_option_header())
                    
            else:
                self.child_Thread = thr.Thread(target=self._thread_task, args=(), daemon=True)
                self.child_Thread.name = f'<ChildThread>CLOCK'
                
                print(f'{self.child_Thread.name} : START')
                
                self.child_Thread.start()
                return
                
        if self.section == MenuSections.NET:
            if self.in_sections:
                output = (f'-- {Menu.HEADER} --', f'{self.section_id + 1}: {net.SectionManager.HEADER}')
                
            elif self.in_options:
                output = (f'-- {net.SectionManager.HEADER} --', net.SectionManager.get_option_header())
                
            else:
                self.child_Thread = thr.Thread(target=self._thread_task, args=(), daemon=True)
                self.child_Thread.name = f'<ChildThread>NET'
                
                print(f'{self.child_Thread.name} : START')
                
                self.child_Thread.start()
                return
            
        if self.section == MenuSections.COLLEGE_PLAN:
            if self.in_sections:
                output = (f'-- {Menu.HEADER} --', f'{self.section_id + 1}: {plan.SectionManager.HEADER}')
                
            elif self.in_options:
                output = (f'-- {plan.SectionManager.HEADER} --', plan.SectionManager.get_option_header())
                    
            else:
                self.child_Thread = thr.Thread(target=self._thread_task, args=(), daemon=True)
                self.child_Thread.name = f'<ChildThread>PLAN'
                
                print(f'{self.child_Thread.name} : START')
                
                self.child_Thread.start()
                return
            
        if self.section == MenuSections.CRYPTO:
            if self.in_sections:
                output = (f'-- {Menu.HEADER} --', f'{self.section_id + 1}: {crypto.SectionManager.HEADER}')
                
            elif self.in_options:
                output = (f'-- {crypto.SectionManager.HEADER} --', crypto.SectionManager.get_option_header())
                    
            else:
                self.child_Thread = thr.Thread(target=self._thread_task, args=(), daemon=True)
                self.child_Thread.name = f'<ChildThread>CRYPTO'
                
                print(f'{self.child_Thread.name} : START')
                
                self.child_Thread.start()
                return
        
        self.client.send(row=0, text=output[0].center(24))
        self.client.send(row=1, text=output[1])
