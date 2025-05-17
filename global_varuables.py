import disnake
from disnake.ext import commands, tasks
from datetime import datetime, date
from TOKEN import *


table_flag = False
log_flag = True
setup_flag = True
old_table_id = [0, 0, 0, 0, 0, 0]
new_table_id = [0, 0, 0, 0, 0, 0]
symbols = ['.', '!', '!', '/']
Tir_users = []
emojies = ['🇦🇮', '🇦🇺', '🇧🇲', '🇮🇴', '🇻🇬', '🇰🇾', '🇨🇰', '🇫🇰', '🇫🇯', '🇲🇸', '🇳🇿', '🇳🇺', '🇵🇳', '🇬🇧', '🏴󠁧󠁢󠁥󠁮󠁧󠁿', '🏴󠁧󠁢󠁳󠁣󠁴󠁿', '🏴󠁧󠁢󠁷󠁬󠁳󠁿', '🇬🇸', '🇸🇭', '🇹🇨']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

now_playing_squad = [[], []]
squad_flag = [False, False]
squad_inter_id = [0, 0]

url = "https://warthunder.com/en/community/claninfo/Guard%20Orion"
scores_before = 0
scores_after = 0
game_count = [False, 0, 0, 0] # flag, wins countm, fals count, games
loup_count = 0
played_games_id = 0
squadron_battle_date = 0
starting_scores = 0

current_datetime = datetime.now()


Tir_buttons = [
            disnake.ui.Button(label="пн", style=disnake.ButtonStyle.success, custom_id="mon1"),
            disnake.ui.Button(label="пн", style=disnake.ButtonStyle.danger, custom_id="mon0"),

            disnake.ui.Button(label="вт", style=disnake.ButtonStyle.success, custom_id="tue1"),
            disnake.ui.Button(label="вт", style=disnake.ButtonStyle.danger, custom_id="tue0"),

            disnake.ui.Button(label="ср", style=disnake.ButtonStyle.success, custom_id="wed1"),
            disnake.ui.Button(label="ср", style=disnake.ButtonStyle.danger, custom_id="wed0"),

            disnake.ui.Button(label="чт", style=disnake.ButtonStyle.success, custom_id="thu1"),
            disnake.ui.Button(label="чт", style=disnake.ButtonStyle.danger, custom_id="thu0"),

            disnake.ui.Button(label="пт", style=disnake.ButtonStyle.success, custom_id="fri1"),
            disnake.ui.Button(label="пт", style=disnake.ButtonStyle.danger, custom_id="fri0"),

            disnake.ui.Button(label="сб", style=disnake.ButtonStyle.success, custom_id="sat1"),
            disnake.ui.Button(label="сб", style=disnake.ButtonStyle.danger, custom_id="sat0"),

            disnake.ui.Button(label="вс", style=disnake.ButtonStyle.success, custom_id="sun1"),
            disnake.ui.Button(label="вс", style=disnake.ButtonStyle.danger, custom_id="sun0"),]





class TirUsr():
    def __init__(self, id):
        self.id = id
        self.nick = "Чел, поменяй ник!"
        self.active_status = True
        self.online_status = False
        self.user_status = False
        self.in_voice_channel = False
        self.active_time = [12, 12, 2000, 12, 0] #day month year hour utc
        self.schedule = [True, True, True, True, True, True, True]
        self.reason = '-'
        self.played_time = 0 #minutes
        
    def check_activity(self):
        
        self.active_status = False
        
        if self.schedule[date.today().weekday()]:
            if current_datetime.year > self.active_time[2]:
                self.active_status = True
            elif current_datetime.year == self.active_time[2]:
                if current_datetime.month > self.active_time[1]:
                    self.active_status = True
                elif current_datetime.month == self.active_time[1]:
                    if current_datetime.day > self.active_time[0]:
                        self.active_status = True





def make_table():

    string = "  список неактивных: \n \n"

    for users in Tir_users:
        if users.user_status:
            if current_datetime.year < users.active_time[2]:
                string = string + users.nick + " неактивен до " + str(users.active_time[0]) + "." + str(users.active_time[1]) + "." + str(users.active_time[2]) +  "\n" + "причина: " + users.reason + "\n" + "\n"
            elif current_datetime.year == users.active_time[2]:
                if current_datetime.month < users.active_time[1]:
                    string = string + users.nick + " неактивен до " + str(users.active_time[0]) + "." + str(users.active_time[1]) + "." + str(users.active_time[2]) + "   причина: " + users.reason + "\n" + "\n"
                elif current_datetime.month == users.active_time[1]:
                    if current_datetime.day <= users.active_time[0]:
                        string = string + users.nick + " неактивен до " + str(users.active_time[0]) + "." + str(users.active_time[1]) + "." + str(users.active_time[2]) + "    причина: " + users.reason + "\n" + "\n"

    string = string + "\n" + "\n" + "\n"
        
    for users in Tir_users:
        if users.user_status:

            flag = False
            days = ['пн', 'вт', 'ср', 'чт', 'пт', 'сб', 'вс']

            for i in range(7):
     
                if not users.schedule[i]:
                   flag = True 

            if flag:
                string = string + users.nick + " не играет по: "
                for i in range(7):
                    if not users.schedule[i]:
                        string = string + days[i] + ' '
                string = string + "\n"

    return string





def save_logs():
    
    with open('logs.dat', mode = 'w', ) as file:
            for users in Tir_users:

                string = str(users.id) + ' ' + str(users.user_status) + ' ' + str(users.active_time[0]) + ' ' + str(users.active_time[1]) + ' ' + str(users.active_time[2]) +  ' '
                
                for i in range(7):
                    string = string + str(users.schedule[i]) + ' '

                string = string + str(users.played_time) + ' '
                string = string + ' ' + str(users.reason) + ' ' + '\n'
                
                file.write(string)





def make_embed():

    embeds = [0, 0, 0, 0, 0, 0, 0, 0]
    embed_quantity=0
    embeds_fields=0

    embeds[embed_quantity] = embed = disnake.Embed(title=f"список неактивных {embed_quantity + 1}", colour=0xF0C43F,) #description="Embed Description",


    for users in Tir_users:
        flag = False
        if users.user_status:
            if current_datetime.year < users.active_time[2]:
                flag = True
            elif current_datetime.year == users.active_time[2]:
                if current_datetime.month < users.active_time[1]:
                    flag = True
                elif current_datetime.month == users.active_time[1]:
                    if current_datetime.day <= users.active_time[0]:
                        flag = True


        if flag and embeds_fields == 24:
            embeds_fields = 0
            embed_quantity = embed_quantity + 1
            embeds[embed_quantity] = disnake.Embed(title=f"список неактивных {embed_quantity + 1}", colour=0xF0C43F,) #description="Embed Description",

        if flag:

            if users.active_time[0] == current_datetime.day and users.active_time[1] == current_datetime.month and users.active_time[2] == current_datetime.year:
                name = "```" + str(users.nick) + "```" + " неактивен ```" + "сегодня" + "```"

            elif (users.active_time[0] == current_datetime.day + 1) and (users.active_time[1] == current_datetime.month) and (users.active_time[2] == current_datetime.year):
                name = "```" + str(users.nick) + "```" + " неактивен ```" + "сегодня и завтра" + "```"

            else:
                name = "```" + str(users.nick) + "```" + " неактивен до ```" + str(users.active_time[0]) + "." + str(users.active_time[1]) + "." + str(users.active_time[2]) + "```"
            
            value = str(users.reason) + "\n."
            embeds[embed_quantity].add_field(name=name, value=value, inline=False)
            embeds_fields = embeds_fields + 1



    embed_quantity=3
    embeds_fields=0

    embeds[embed_quantity] = embed = disnake.Embed(title=f"расписание игроков {embed_quantity - 2}", colour=0xF0C43F,) #description="Embed Description",


    for users in Tir_users:
        if users.user_status:

            flag = False
            days = ['пн', 'вт', 'ср', 'чт', 'пт', 'сб', 'вс']
            string = "не играет по: "

            for i in range(7):
         
                if not users.schedule[i]:
                    flag = True 


            if flag and embeds_fields == 24:
                embeds_fields = 0
                embed_quantity = embed_quantity + 1
                embeds[embed_quantity] = disnake.Embed(title=f"расписание игроков {embed_quantity - 2}", colour=0xF0C43F,) #description="Embed Description",

            if flag:
                for i in range(7):
                    if not users.schedule[i]:
                        string = string + days[i] + ' '

                name = "```" + str(users.nick) + "```"
                value = string
                embeds[embed_quantity].add_field(name=name, value=value, inline=False)
                print(users.nick, users.schedule, flag)
                embeds_fields = embeds_fields + 1

    return embeds






def check_format(day, month, year):

    for symbols in day:
        if not (symbols in numbers):
            return [True]

    for symbols in month:
        if not (symbols in numbers):
            return [True]

    day = int(day)
    month = int(month)
    year = int(year)

    if day > 31 or day < 0 or month > 12 or month < 0:
            return [True]

    if (year < 99 and year >= 0):
        year = year + current_datetime.year - current_datetime.year%100

    return [False, day, month, year]
