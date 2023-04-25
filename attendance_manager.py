import pandas as pd
#import openpyxl
#import calendar
import time


class AttManager:
    index = []
    columns = []
    attendance_list = []
    def __init__(self) -> None:
        self.columns = ['Name', 'arrival time', 'exit time']
        curr_time = time.gmtime()
        date = "{}-{}-{}".format(curr_time.tm_mday, curr_time.tm_mon, curr_time.tm_year)
        
        df = pd.DataFrame(self.attendance_list, index=self.index, columns=self.columns)
        df.to_excel('./att_sheet.xlsx', sheet_name=date)


    def addToAttendanceSheet(self, name, timestamp, date, type_of_log):
        found_user = False
        if type_of_log == 'arrival':
            for att in self.attendance_list:
                if name in att:
                    i = att.index(name)
                    self.attendance_list[i][1] = timestamp
                    found_user = True
            if not found_user:
                self.index.append(len(self.index)+1)
                self.attendance_list.append([name, timestamp, ''])

        if type_of_log == 'exit':
            for att in self.attendance_list:
                if name in att:
                    i = att.index(name)
                    self.attendance_list[i][2] = timestamp
                    found_user = True
            if not found_user:
                self.index.append(len(self.index)+1)
                self.attendance_list.append([name, '', timestamp])


        df = pd.DataFrame(self.attendance_list, index=self.index, columns=self.columns)
        df.to_excel('./att_sheet.xlsx', sheet_name=date)
        