from typing import Optional

import disnake
from disnake.ext import commands, tasks
from datetime import datetime, date
from user_class import *
from TOKEN import *



bot = commands.Bot(command_prefix='.', help_command=None, intents=disnake.Intents.all(), test_guilds=[1359580722494705694])


log_flag = True
setup_flag = True
old_table = 0
old_table_id = 0
symbols = ['.', '!', '!', '/']
active_roles = [1359607682306281683]
Tir_users = []

current_datetime = datetime.now()

Tir_buttons = [
            disnake.ui.Button(label="mon", style=disnake.ButtonStyle.success, custom_id="mon1"),
            disnake.ui.Button(label="mon", style=disnake.ButtonStyle.danger, custom_id="mon0"),

            disnake.ui.Button(label="tue", style=disnake.ButtonStyle.success, custom_id="tue1"),
            disnake.ui.Button(label="tue", style=disnake.ButtonStyle.danger, custom_id="tue0"),

            disnake.ui.Button(label="wed", style=disnake.ButtonStyle.success, custom_id="wed1"),
            disnake.ui.Button(label="wed", style=disnake.ButtonStyle.danger, custom_id="wed0"),

            disnake.ui.Button(label="thu", style=disnake.ButtonStyle.success, custom_id="thu1"),
            disnake.ui.Button(label="thu", style=disnake.ButtonStyle.danger, custom_id="thu0"),

            disnake.ui.Button(label="fri", style=disnake.ButtonStyle.success, custom_id="fri1"),
            disnake.ui.Button(label="fri", style=disnake.ButtonStyle.danger, custom_id="fri0"),

            disnake.ui.Button(label="sat", style=disnake.ButtonStyle.success, custom_id="sat1"),
            disnake.ui.Button(label="sat", style=disnake.ButtonStyle.danger, custom_id="sat0"),

            disnake.ui.Button(label="sun", style=disnake.ButtonStyle.success, custom_id="sun1"),
            disnake.ui.Button(label="sun", style=disnake.ButtonStyle.danger, custom_id="sun0"),]




def make_table():

    string = "  список неактивных: \n"

    for users in Tir_users:
        if users.user_status:
            if current_datetime.year < users.active_time[2]:
                string = string + users.nick + " неактивен до " + str(users.active_time[0]) + "." + str(users.active_time[1]) + "." + str(users.active_time[2]) +  "   причина: " + users.reason + "\n"
            elif current_datetime.year == users.active_time[2]:
                if current_datetime.month < users.active_time[1]:
                    string = string + users.nick + " неактивен до " + str(users.active_time[0]) + "." + str(users.active_time[1]) + "." + str(users.active_time[2]) + "   причина: " + users.reason + "\n"
                elif current_datetime.month == users.active_time[1]:
                    if current_datetime.day < users.active_time[0]:
                        string = string + users.nick + " неактивен до " + str(users.active_time[0]) + "." + str(users.active_time[1]) + "." + str(users.active_time[2]) + "    причина: " + users.reason + "\n"

    string = string + "\n"
    
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





@bot.event
async def on_ready():
    print(f"Bot {bot.user} ready")
    return





@bot.command()
@commands.has_permissions(administrator=True)
async def setup(ctx):

    global setup_flag

    for users in ctx.author.guild.members:
        Tir_users.append(TirUsr(users.id))
        if isinstance(users.nick, str):
            Tir_users[-1].nick = users.nick
        for roles in users.roles:
            if roles.id in active_roles:
                Tir_users[-1].user_status = True

    await ctx.send(f"setup complete", delete_after=15)
    setup_flag = False
    await ctx.message.delete()
    
    for users in ctx.author.guild.members:
        print(users.nick)





@bot.command()
async def ping_all(ctx):

    for users1 in ctx.author.guild.members:
        for users2 in Tir_users:
            if users1.id == users2.id:
                if users1.status.value == 'online':
                    users2.online_status = True
                else:
                    users2.online_status = False
            
    
    for users in Tir_users:    
        if users.user_status and users.online_status:
       
            users.check_activity()
            if users.active_status:
                await ctx.send(f"<@{users.id}>")

    await ctx.message.delete()





@bot.command()
@commands.has_permissions(administrator=True)
async def load_logs(ctx):


    if setup_flag:
        await ctx.send(f"WARNING setup has not been conpleted <@320931039252054016> complete setup before using this command. Удалить сообщение вручную")
        return

    with open('logs.dat', mode = 'r', ) as file:
        for lines in file:
            if len(lines)<8:
                break
            data = lines.split()

            for users in Tir_users:

                if users.id == int(data[0]):

                    users.active_time[0] = int(data[2])
                    users.active_time[1] = int(data[3])
                    users.active_time[2] = int(data[4])

                    for i in range(7):

                        if data[5+i] == "True":
                            users.schedule[i] = True
                        else:
                            users.schedule[i] = False

                    print()
                    
                    i=0
                    users.reason = ''
                    for words in data:
                        if i > 11 and i < (len(data) - 1):
                            users.reason = users.reason + str(data[i]) + ' '

    global log_flag
    log_flag = False
    await ctx.send(f"loading complete", delete_after=15)
    
    channel = bot.get_channel(1360163404903485623)
    
    global old_table_id
    tmp = await channel.send(f"{make_table()}")
    old_table_id = tmp.id

    await ctx.message.delete()
    await update_status()
    




@bot.slash_command(name = "неактивен", description = "Укажите время до (не включительно) которого вы не сможете играть")
async def act(ctx, day: int, month: int, year: int, reason = "отсутсвует"):

    if log_flag:
        await ctx.send(f"WARNING logs not loaded <@320931039252054016> upload logs before using the command. Удалить сообщение вручную")
        return

    if day > 31 or day < 0 or month > 12 or month < 0:
        await ctx.send(f"ошибка ввода данных")
        return
    
    for users in Tir_users:
        if users.id == ctx.author.id:

            users.active_time[0] = day
            users.active_time[1] = month
            users.active_time[2] = year
            users.reason = reason
            

            users.check_activity()
            
            global old_table_id
            tmp = await bot.get_context(bot.get_message(old_table_id))
            await tmp.message.delete()
            
            await print_table(ctx)
            
            if users.active_status:
                await ctx.send(f"{ctx.author.nick} теперь активен", delete_after=15)
            else:
                await ctx.send(f"{ctx.author.nick} неактивен до {day}.{month}.{year}   причина: {users.reason}", delete_after=15)


    with open('logs.dat', mode = 'w', ) as file:
        for users in Tir_users:
            string = str(users.id) + ' ' + str(users.user_status) + ' ' + str(users.active_time[0]) + ' ' + str(users.active_time[1]) + ' ' + str(users.active_time[2]) +  ' '
            for i in range(7):
                string = string + str(users.schedule[i]) + ' '
            string = string + ' ' + str(users.reason) + ' ' + '\n'
            file.write(string)
    




@bot.slash_command(name = "активен", description = "снять статус неактивен")
async def clearmy(ctx):

    if log_flag:
        await ctx.send(f"WARNING logs not loaded <@320931039252054016> upload logs before using the command. Удалить сообщение вручную")
        return

    for users in Tir_users:
        if users.id == ctx.author.id:
            
            users.active_time[0] = current_datetime.day
            users.active_time[1] = current_datetime.month
            users.active_time[2] = current_datetime.year
            users.reason = '-'

            global old_table_id
            tmp = await bot.get_context(bot.get_message(old_table_id))
            await tmp.message.delete()
            
            await print_table(ctx)

    with open('logs.dat', mode = 'w', ) as file:
        for users in Tir_users:
            string = str(users.id) + ' ' + str(users.user_status) + ' ' + str(users.active_time[0]) + ' ' + str(users.active_time[1]) + ' ' + str(users.active_time[2]) +  ' '
            for i in range(7):
                string = string + str(users.schedule[i]) + ' '
            string = string + ' ' + str(users.reason) + ' ' + '\n'
            file.write(string)

    await ctx.send(f"{ctx.author.nick} теперь активен", delete_after=15)





@bot.slash_command(name = "добавить_неактивен", description = "Добавить статус неактивен другому пользователю")
@commands.has_permissions(administrator=True)
async def act_add(ctx, member: str, day: int, month: int, year: int, reason = "неактив добавил другой участник"):

    if log_flag:
        await ctx.send(f"WARMING logs not loaded <@320931039252054016> upload logs before using the command. Удалить сообщение вручную")
        return

    if day > 31 or day < 0 or month > 12 or month < 0:
        await ctx.send(f"ошибка ввода данных", delete_after=15)
        return

    flag = True

    for users in Tir_users:
        
        if member == '<@' + str(users.id)+'>':
            users.active_time[0] = day
            users.active_time[1] = month
            users.active_time[2] = year
            users.reason = reason

            users.check_activity()
            if users.active_status:
                await ctx.send(f"{ctx.author.nick} теперь активен", delete_after=15)
            else:
                await ctx.send(f"{ctx.author.nick} неактивен до {day}.{month}.{year}   причина: {users.reason}", delete_after=15)

            flag = False

            global old_table_id
            tmp = await bot.get_context(bot.get_message(old_table_id))
            await tmp.message.delete()
            
            await print_table(ctx)

    if flag:
        await ctx.send(f"игрок не найден", delete_after=15)


    with open('logs.dat', mode = 'w', ) as file:
        for users in Tir_users:
            string = str(users.id) + ' ' + str(users.user_status) + ' ' + str(users.active_time[0]) + ' ' + str(users.active_time[1]) + ' ' + str(users.active_time[2]) +  ' '
            for i in range(7):
                string = string + str(users.schedule[i]) + ' '
            string = string + ' ' + str(users.reason) + ' ' + '\n'
            file.write(string)
    
    #await ctx.send(f"<@{Tir_users[0].id}>")
    #await ctx.send(f"{Guild.id}")





@bot.slash_command(name = "убрать_неактивен", description = "Убрать статус неактивен у другого пользователя")
@commands.has_permissions(administrator=True)
async def act_rem(ctx, member: str):

    if log_flag:
        await ctx.send(f"WARNING logs not loaded <@320931039252054016> upload logs before using the command. Удалить сообщение вручную")
        return

    flag = True
    
    for users in Tir_users:
        
        if member == '<@' + str(users.id)+'>':
            users.active_time[0] = current_datetime.day
            users.active_time[1] = current_datetime.month
            users.active_time[2] = current_datetime.year
            users.reason = '-'
            await ctx.send(f"{users.nick} теперь активен", delete_after=15)
            flag = False

            global old_table_id
            tmp = await bot.get_context(bot.get_message(old_table_id))
            await tmp.message.delete()
            
            await print_table(ctx)

    if flag:
        await ctx.send(f"игрок не найден", delete_after=15)

    with open('logs.dat', mode = 'w', ) as file:
        for users in Tir_users:
            string = str(users.id) + ' ' + str(users.user_status) + ' ' + str(users.active_time[0]) + ' ' + str(users.active_time[1]) + ' ' + str(users.active_time[2]) +  ' '
            for i in range(7):
                string = string + str(users.schedule[i]) + ' '
            string = string + ' ' + str(users.reason) + ' ' + '\n'
            file.write(string)




@bot.slash_command(name = "расписание", description = "изменить своё расписание p.s менюшка активна 15 секунд")
async def schedule(inter: disnake.ApplicationCommandInteraction):

    user_components = []

    for users in Tir_users:
        if users.id == inter.user.id:
            for i in range(7):
                if users.schedule[i]:
                    user_components.append(Tir_buttons[i*2])
                else:
                    user_components.append(Tir_buttons[2*i+1])




    await inter.response.send_message("schedule", components=user_components, delete_after = 15.0)





@bot.slash_command(name = "очистить_расписание", description = "Очистить расписание другого пользователя")
@commands.has_permissions(administrator=True)
async def clr_schedule(ctx, member: str):

    if log_flag:
        await ctx.send(f"WARMING logs not loaded <@320931039252054016> upload logs before using the command. Удалить сообщение вручную")
        return

    flag = True
    
    for users in Tir_users:
        
        if member == '<@' + str(users.id)+'>':
            
            for i in range(7):
                users.schedule[i] = True

            flag = False

            global old_table_id
            tmp = await bot.get_context(bot.get_message(old_table_id))
            await tmp.message.delete()
            
            await print_table(ctx)

    if flag:
        await ctx.send(f"игрок не найден", delete_after=15)

    with open('logs.dat', mode = 'w', ) as file:
        for users in Tir_users:
            string = str(users.id) + ' ' + str(users.user_status) + ' ' + str(users.active_time[0]) + ' ' + str(users.active_time[1]) + ' ' + str(users.active_time[2]) +  ' '
            for i in range(7):
                string = string + str(users.schedule[i]) + ' '
            string = string + ' ' + str(users.reason) + ' ' + '\n'
            file.write(string)





@bot.command()
@commands.has_permissions(administrator=True)
async def print_table(ctx):
    
    channel = bot.get_channel(1360163404903485623)
    
    global old_table_id
    tmp = await channel.send(f"{make_table()}")
    old_table_id = tmp.id


           



@tasks.loop(seconds=15)
async def update_status():
    
    print(12344321)

    if log_flag or setup_flag:
        return


    for users1 in message.author.guild.members:
        flag = True
        for users2 in Tir_users:
            if users1.id == users2.id:
                    
                if isinstance(users1.nick, str):
                    users2.nick = users1.nick
                for roles in users1.roles:
                    if roles.id in active_roles:
                        users2.user_status = True
                    else:
                        users2.user_status = False
            
                flag = False
                break
        if flag:
            Tir_users.append(TirUsr(users1.id))
            break

    for users in Tir_users:
        print(users.nick, users.user_status)






@bot.listen("on_button_click")
async def help_listener(inter: disnake.MessageInteraction):

    days = ["mon1", "tue1", "wed1", "thu1", "fri1", "sat1", "sun1",
            "mon0", "tue0", "wed0", "thu0", "fri0", "sat0", "sun0"]

    if inter.component.custom_id not in days:
        return

    for users in Tir_users:
        if inter.user.id == users.id:
            break

    user_components=[]

    a = days.index(inter.component.custom_id)

    if a > 6:
        users.schedule[a-7] = True
    else:
        users.schedule[a] = False

    for i in range(7):
        if users.schedule[i]:
            user_components.append(Tir_buttons[i*2])
        else:
            user_components.append(Tir_buttons[2*i+1])

    await inter.response.edit_message(components=user_components, delete_after = 10.0)

    await inter.send(f"{users.nick} расписание обновлено", delete_after=10)

    global old_table_id
    tmp = await bot.get_context(bot.get_message(old_table_id))
    await tmp.message.delete()
          
    await print_table(tmp)

    with open('logs.dat', mode = 'w', ) as file:
        for users in Tir_users:
            string = str(users.id) + ' ' + str(users.user_status) + ' ' + str(users.active_time[0]) + ' ' + str(users.active_time[1]) + ' ' + str(users.active_time[2]) +  ' '
            for i in range(7):
                string = string + str(users.schedule[i]) + ' '
            string = string + ' ' + str(users.reason) + ' ' + '\n'
            file.write(string)




bot.run(TOKEN)