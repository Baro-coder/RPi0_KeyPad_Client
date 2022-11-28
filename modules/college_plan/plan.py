#!/usr/bin/python
# -- KeyPad_Client/modules/college_plan: plan.py --

from enum import Enum
import datetime
import csv

from modules.college_plan.date import Date
from modules.college_plan.lesson import Lesson, LessonType

class PlanOptions(Enum):
    CURRENT_DAY = 0
    NEXT_DAY = 1


class SectionManager:
    HEADER = 'COLLEGE PLAN'
    option_id = 0
    
    plan = None
    block_id = 0
    
    @staticmethod
    def next_option():
        SectionManager.option_id += 1
        if SectionManager.option_id == 2:
            SectionManager.option_id = 0
            
    @staticmethod
    def prev_option():
        SectionManager.option_id -= 1
        if SectionManager.option_id == -1:
            SectionManager.option_id = 1
    
    
    @staticmethod
    def get_option_header():
        return f'{PlanOptions(SectionManager.option_id).value + 1}: {PlanOptions(SectionManager.option_id).name}'
    
    
    @staticmethod
    def get_option_output():
        if SectionManager.option_id == PlanOptions.CURRENT_DAY.value:
            date, plan = SectionManager._get_plan_for_current_day()
            
        elif SectionManager.option_id == PlanOptions.NEXT_DAY.value:
            date, plan = SectionManager._get_plan_for_next_day()
        
        out1 = f'{SectionManager.HEADER}:{(23 - (len(SectionManager.HEADER) + len(date))) * " "}{date}'
        
        if plan is None:
            out2 = 'WOLNE'.center(24)
        else:
            out2 = str(plan.lessons[SectionManager.block_id])
        
        output = (out1, out2)
        
        return output
    

    @staticmethod
    def next_block():
        SectionManager.block_id += 1
        if SectionManager.block_id == 7:
            SectionManager.block_id = 0
            
    @staticmethod
    def prev_block():
        SectionManager.block_id -= 1
        if SectionManager.block_id == -1:
            SectionManager.block_id = 6
    

    @staticmethod
    def _get_plan_for_current_day():
        year, month, day = datetime.datetime.today().strftime("%Y-%m-%d").split('-')
        
        date = f'{day}/{month}/{year}'
        plan = Plan.get_plan_by_date(int(year), int(month), int(day))

        return date, plan
    
    @staticmethod
    def _get_plan_for_next_day():
        year, month, day = (datetime.datetime.today() + datetime.timedelta(days=1)).strftime("%Y-%m-%d").split('-')
        
        date = f'{day}/{month}/{year}'
        plan = Plan.get_plan_by_date(int(year), int(month), int(day))
        
        return date, plan



# *** Plan ***
class Plan:
    FILE_CSV = '/home/pi/.Private/RPi0_College_Plan/college_plan.csv'
    dates = []
            
    @staticmethod
    def get_plan_by_date(year : int, month : int, day : int):
        Plan._read_data_from_csv_file()
        
        d = Date(day, month, year)
        
        for date in Plan.dates:
            if d.__eq__(date):
                return date
        
        return None
    
    @staticmethod
    def _get_from_list(dates : list, date : Date):
        if len(dates) == 0:
            return None

        for d in dates:
            if d == date:
                return d

        return None

    @staticmethod
    def _read_data_from_csv_file():
        Plan.dates = []
        
        with open(Plan.FILE_CSV, newline='\n', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter=',', quoting=csv.QUOTE_NONE)

            for i, row in enumerate(reader):
                if i == 0: continue

                date = Date(day=int(row[2]),
                            month=int(row[1]), 
                            year=int(row[0]),
                            lessons=[])
                Lesson()
                lesson = Lesson(block_id=int(row[3]),
                                subject=row[4],
                                type=LessonType(row[5]),
                                place=row[6],
                                info=row[7])

                d = Plan._get_from_list(Plan.dates, date)

                if d is None:
                    date.lessons.append(lesson)
                    Plan.dates.append(date)

                else:
                    d.lessons.append(lesson)
