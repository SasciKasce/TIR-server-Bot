import disnake
from disnake.ext import commands, tasks
from datetime import datetime, date
from TOKEN import *
import os
import global_varuables




class activity_commands(commands.Cog):



    def __init__(self, bot):
        self.bot=bot



    @commands.slash_command(name = "неактивен", description = "Укажите время до (включительно) которого вы не сможете играть")
    async def act(self, ctx, day: str, month: str, year: int, reason = "отсутсвует"):

        if global_varuables.log_flag:
            await ctx.send(f"WARNING logs not loaded <@{MY_id}> upload logs before using the command. Удалить сообщение вручную")
            return

        input_date = global_varuables.check_format(day, month, year)

        if input_date[0]:
            await ctx.send(f"ошибка ввода данных", delete_after=15)
            return

        day = input_date[1]
        month = input_date[2]
        year = input_date[3]
        
        for users in global_varuables.Tir_users:
            if users.id == ctx.author.id:

                users.active_time[0] = day
                users.active_time[1] = month
                users.active_time[2] = year
                users.reason = reason


                users.check_activity()

                if users.active_status:
                    await ctx.send(f"{ctx.author.nick} теперь активен", delete_after=15)
                else:
                    await ctx.send(f"{ctx.author.nick} неактивен до {day}.{month}.{year}   причина: {users.reason}", delete_after=15)
                
                await self.bot.get_command('print_table').__call__(ctx, 'activity')


        global_varuables.save_logs()
        




    @commands.slash_command(name = "активен", description = "снять статус неактивен")
    async def clearmy(self, ctx):

        if global_varuables.log_flag:
            await ctx.send(f"WARNING logs not loaded <@{MY_id}> upload logs before using the command. Удалить сообщение вручную")
            return

        for users in global_varuables.Tir_users:
            if users.id == ctx.author.id:
                
                users.active_time[0] = global_varuables.current_datetime.day-1
                users.active_time[1] = global_varuables.current_datetime.month
                users.active_time[2] = global_varuables.current_datetime.year
                users.reason = '-'
                

        global_varuables.save_logs()

        
        await self.bot.get_command('print_table').__call__(ctx, 'activity')

        await ctx.send(f"{ctx.author.nick} теперь активен", delete_after=15)





    @commands.slash_command(name = "добавить_неактивен", description = "Добавить статус неактивен другому пользователю")
    async def act_add(self, ctx, member: str, day: str, month: str, year: int, reason = "неактив добавил другой участник"):

        access_flag = True
        for roles in ctx.author.roles:
            if ( (ctx.author.id == MY_id) or (roles.id in admin_roles) ):
                access_flag = False
                break
                
        if access_flag:
            await ctx.send(f"Недостаточно прав", delete_after=15)
            return

        if global_varuables.log_flag:
            await ctx.send(f"WARMING logs not loaded <@{MY_id}> upload logs before using the command. Удалить сообщение вручную")
            return

        input_date = global_varuables.check_format(day, month, year)

        if input_date[0]:
            await ctx.send(f"ошибка ввода данных", delete_after=15)
            return

        day = input_date[1]
        month = input_date[2]
        year = input_date[3]

        flag = True

        for users in global_varuables.Tir_users:
            
            if member == '<@' + str(users.id)+'>':
                
                users.active_time[0] = day
                users.active_time[1] = month
                users.active_time[2] = year
                users.reason = reason

                users.check_activity()
                if users.active_status:
                    await ctx.send(f"{users.nick} теперь активен", delete_after=15)
                else:
                    await ctx.send(f"{users.nick} неактивен до {day}.{month}.{year}   причина: {users.reason}", delete_after=15)

                flag = False

                await self.bot.get_command('print_table').__call__(ctx, 'activity')

        if flag:
            await ctx.send(f"игрок не найден", delete_after=15)

        global_varuables.save_logs()





    @commands.slash_command(name = "убрать_неактивен", description = "Убрать статус неактивен у другого пользователя")
    async def act_rem(self, ctx, member: str):
        
        access_flag = True
        for roles in ctx.author.roles:
            if ( (ctx.author.id == MY_id) or (roles.id in admin_roles) ):
                access_flag = False
                break
                
        if access_flag:
            await ctx.send(f"Недостаточно прав", delete_after=15)
            return

        if global_varuables.log_flag:
            await ctx.send(f"WARNING logs not loaded <@{MY_id}> upload logs before using the command. Удалить сообщение вручную")
            return

        flag = True
        
        for users in global_varuables.Tir_users:
            
            if member == '<@' + str(users.id)+'>':

                users.active_time[0] = global_varuables.current_datetime.day-1
                users.active_time[1] = global_varuables.current_datetime.month
                users.active_time[2] = global_varuables.current_datetime.year
                users.reason = '-'
                await ctx.send(f"{users.nick} теперь активен", delete_after=15)
                flag = False

                await self.bot.get_command('print_table').__call__(ctx, 'activity')

        if flag:
            await ctx.send(f"игрок не найден", delete_after=15)

        global_varuables.save_logs()





    @commands.slash_command(name = "неактивен_сегодня", description = "вы неактивны сегодня")
    async def act_td(self, ctx, reason = "отсутсвует"):

        if global_varuables.log_flag:
            await ctx.send(f"WARNING logs not loaded <@{MY_id}> upload logs before using the command. Удалить сообщение вручную")
            return

        day = global_varuables.current_datetime.day
        month = global_varuables.current_datetime.month
        year = global_varuables.current_datetime.year


        for users in global_varuables.Tir_users:
            if users.id == ctx.author.id:

                users.active_time[0] = day
                users.active_time[1] = month
                users.active_time[2] = year
                users.reason = reason


                users.check_activity()

                await ctx.send(f"{ctx.author.nick} сегодня не играет   причина: {users.reason}", delete_after=15)
                
                await self.bot.get_command('print_table').__call__(ctx, 'activity')


        global_varuables.save_logs()





    @commands.slash_command(name = "неактивен_завтра", description = "вы неактивны сегодня и завтра")
    async def act_tm(self, ctx, reason = "отсутсвует"):

        if global_varuables.log_flag:
            await ctx.send(f"WARNING logs not loaded <@{MY_id}> upload logs before using the command. Удалить сообщение вручную")
            return

        day = global_varuables.current_datetime.day
        month = global_varuables.current_datetime.month
        year = global_varuables.current_datetime.year


        for users in global_varuables.Tir_users:
            if users.id == ctx.author.id:

                users.active_time[0] = day+1
                users.active_time[1] = month
                users.active_time[2] = year
                users.reason = reason


                users.check_activity()

                await ctx.send(f"{ctx.author.nick} не играет сегодня и завтра   причина: {users.reason}", delete_after=15)
                
                await self.bot.get_command('print_table').__call__(ctx, 'activity')


        global_varuables.save_logs()





    @commands.slash_command(name = "добавить_неактивен_сегодня", description = "вы неактивны сегодня")
    async def add_act_td(self, ctx, member: str, reason = "отсутсвует"):

        access_flag = True
        for roles in ctx.author.roles:
            if ( (ctx.author.id == MY_id) or (roles.id in admin_roles) ):
                access_flag = False
                break
                
        if access_flag:
            await ctx.send(f"Недостаточно прав", delete_after=15)
            return

        if global_varuables.log_flag:
            await ctx.send(f"WARNING logs not loaded <@{MY_id}> upload logs before using the command. Удалить сообщение вручную")
            return

        day = global_varuables.current_datetime.day
        month = global_varuables.current_datetime.month
        year = global_varuables.current_datetime.year


        for users in global_varuables.Tir_users:

            if member == '<@' + str(users.id)+'>':

                users.active_time[0] = day
                users.active_time[1] = month
                users.active_time[2] = year
                users.reason = reason


                users.check_activity()

                await ctx.send(f"{ctx.author.nick} сегодня не играет   причина: {users.reason}", delete_after=15)
                
                await self.bot.get_command('print_table').__call__(ctx, 'activity')


        global_varuables.save_logs()





    @commands.slash_command(name = "добавить_неактивен_завтра", description = "вы неактивны сегодня и завтра")
    async def add_act_tm(self, ctx, member: str, reason = "отсутсвует"):

        access_flag = True
        for roles in ctx.author.roles:
            if ( (ctx.author.id == MY_id) or (roles.id in admin_roles) ):
                access_flag = False
                break
                
        if access_flag:
            await ctx.send(f"Недостаточно прав", delete_after=15)
            return

        if global_varuables.log_flag:
            await ctx.send(f"WARNING logs not loaded <@{MY_id}> upload logs before using the command. Удалить сообщение вручную")
            return

        day = global_varuables.current_datetime.day
        month = global_varuables.current_datetime.month
        year = global_varuables.current_datetime.year


        for users in global_varuables.Tir_users:
            
            if member == '<@' + str(users.id)+'>':

                users.active_time[0] = day+1
                users.active_time[1] = month
                users.active_time[2] = year
                users.reason = reason


                users.check_activity()

                await ctx.send(f"{ctx.author.nick} не играет сегодня и завтра   причина: {users.reason}", delete_after=15)
                
                await self.bot.get_command('print_table').__call__(ctx, 'activity')


        global_varuables.save_logs()





    @commands.slash_command(name = "расписание", description = "изменить своё расписание p.s менюшка активна 15 секунд")
    async def set_schedule(self, inter: disnake.ApplicationCommandInteraction):

        if global_varuables.log_flag:
            await ctx.send(f"WARNING logs not loaded <@{MY_id}> upload logs before using the command. Удалить сообщение вручную")
            return

        user_components = []

        for users in global_varuables.Tir_users:
            if users.id == inter.user.id:
                for i in range(7):
                    if users.schedule[i]:
                        user_components.append(global_varuables.Tir_buttons[i*2])
                    else:
                        user_components.append(global_varuables.Tir_buttons[2*i+1])

        await inter.response.send_message("ваше расписание", components=user_components, delete_after = 15.0)





    @commands.slash_command(name = "очистить_расписание", description = "Очистить расписание другого пользователя")
    async def clr_schedule(self, ctx, member: str):
        
        access_flag = True
        for roles in ctx.author.roles:
            if ( (ctx.author.id == MY_id) or (roles.id in admin_roles) ):
                access_flag = False
                break
                
        if access_flag:
            await ctx.send(f"Недостаточно прав", delete_after=15)
            return

        if global_varuables.log_flag:
            await ctx.send(f"WARMING logs not loaded <@{MY_id}> upload logs before using the command. Удалить сообщение вручную")
            return

        flag = True
        
        for users in global_varuables.Tir_users:
            
            if member == '<@' + str(users.id)+'>':
                
                for i in range(7):
                    users.schedule[i] = True

                flag = False

                await self.bot.get_command('print_table').__call__(ctx, 'schedule')

        if flag:
            await ctx.send(f"игрок не найден", delete_after=15)

        global_varuables.save_logs()





    @commands.Cog.listener(name = "on_button_click")
    async def schedule(self, inter: disnake.MessageInteraction):

        days = ["mon1", "tue1", "wed1", "thu1", "fri1", "sat1", "sun1",
                "mon0", "tue0", "wed0", "thu0", "fri0", "sat0", "sun0"]

        if inter.component.custom_id not in days:
            return

        for users in global_varuables.Tir_users:
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
                user_components.append(global_varuables.Tir_buttons[i*2])
            else:
                user_components.append(global_varuables.Tir_buttons[2*i+1])

        await inter.response.edit_message(components=user_components, delete_after = 10.0)

        #await inter.send(f"{users.nick} расписание обновлено", delete_after=10)

        await self.bot.get_command('print_table').__call__(inter.context, 'schedule')

        global_varuables.save_logs()

        


def setup(bot):
    bot.add_cog(activity_commands(bot))