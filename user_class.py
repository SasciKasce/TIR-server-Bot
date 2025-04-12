from datetime import datetime
from datetime import date

current_datetime = datetime.now()

class TirUsr():
    def __init__(self, id):
        self.id = id
        self.nick = "Чел, поменяй ник!"
        self.active_status = True
        self.online_status = False
        self.user_status = False
        self.active_time = [12, 12, 2000, 12, 0] #day month year hour utc
        self.schedule = [True, True, True, True, True, True, True]
        self.reason = '-'
        
    def check_activity(self):
        
        self.active_status = False
        
        if self.schedule[date.today().weekday()]:
            if current_datetime.year > self.active_time[2]:
                self.active_status = True
            elif current_datetime.year == self.active_time[2]:
                if current_datetime.month > self.active_time[1]:
                    self.active_status = True
                elif current_datetime.month == self.active_time[1]:
                    if current_datetime.day >= self.active_time[0]:
                        self.active_status = True
