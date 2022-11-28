#!/usr/bin/python
# -- KeyPad_Client/modules/clock: clock.py --

from datetime import date, datetime

from enum import Enum


class ClockOption(Enum):
    TIME = 0
    DATE = 1
    DATETIME = 2


class SectionManager:
    HEADER = 'CLOCK'
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
        return f'{ClockOption(SectionManager.option_id).value + 1}: {ClockOption(SectionManager.option_id).name}'
    
    @staticmethod
    def get_option_output():
        if SectionManager.option_id == ClockOption.TIME.value:
            output = SectionManager._get_current_time()
            
        elif SectionManager.option_id == ClockOption.DATE.value:
            output = SectionManager._get_current_date()
            
        elif SectionManager.option_id == ClockOption.DATETIME.value:
            output = f'{SectionManager._get_current_date()}      {SectionManager._get_current_time()}'
            
        return output.center(24)
    


    def _get_current_date():
        today = date.today().strftime("%d/%m/%Y")
        return today


    def _get_current_time():
        now = datetime.now().strftime("%H:%M:%S")
        return now