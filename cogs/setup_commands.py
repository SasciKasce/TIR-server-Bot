import disnake
from disnake.ext import commands, tasks
from datetime import datetime, date
from TOKEN import *
import os
import global_varuables


print(global_varuables.symbols)



class setup_commands(commands.Cog):

    def __init__(self, bot):
        self.bot=bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Bot {self.bot.user} is ready")





    @commands.command()
    async def setup1(self, ctx):

        access_flag = True
        for roles in ctx.author.roles:
            if ( (ctx.author.id == MY_id) or (roles.id in admin_roles) ):
                access_flag = False
                break
                
        if access_flag:
            await ctx.send(f"Недостаточно прав", delete_after=15)
            await ctx.message.delete()
            return

        for users in ctx.author.guild.members:
            global_varuables.Tir_users.append(global_varuables.TirUsr(users.id))
            if isinstance(users.nick, str):
                global_varuables.Tir_users[-1].nick = users.nick
            for roles in users.roles:
                if roles.id in global_varuables.active_roles:
                    global_varuables.Tir_users[-1].user_status = True

        await ctx.send(f"setup complete", delete_after=15)

        global_varuables.setup_flag = False
        
        await ctx.message.delete()
        
        for users in ctx.author.guild.members:
            print(users.nick)





    @commands.command()
    async def load_logs(self, ctx):
        
        access_flag = True
        for roles in ctx.author.roles:
            if ( (ctx.author.id == MY_id) or (roles.id in admin_roles) ):
                access_flag = False
                break
                
        if access_flag:
            await ctx.send(f"Недостаточно прав", delete_after=15)
            await ctx.message.delete()
            return

        if global_varuables.setup_flag:
            await ctx.send(f"WARNING setup has not been conpleted <@{MY_id}> complete setup before using this command. Удалить сообщение вручную")
            return
        
        with open('logs.dat', mode = 'r', ) as file:
            for lines in file:
                data = lines.split()

                for users in global_varuables.Tir_users:

                    if users.id == int(data[0]):

                        users.active_time[0] = int(data[2])
                        users.active_time[1] = int(data[3])
                        users.active_time[2] = int(data[4])

                        for i in range(7):

                            if data[5+i] == "True":
                                users.schedule[i] = True
                            else:
                                users.schedule[i] = False
                        
                        i=0
                        users.played_time = int(data[12])

                        users.reason = ''
                        for words in data:
                            if i > 12 and i < len(data):
                                users.reason = users.reason + str(data[i]) + ' '
                            i=i+1

        global_varuables.log_flag = False
        await ctx.send(f"loading complete", delete_after=15)
        
        await self.bot.get_command('print_table').__call__(ctx, 'setup')

        await ctx.message.delete()





    @commands.command()
    async def ping_all(self, ctx):
        
        access_flag = True
        for roles in ctx.author.roles:
            if ( (ctx.author.id == MY_id) or (roles.id in admin_roles) ):
                access_flag = False
                break
                
        if access_flag:
            await ctx.send(f"Недостаточно прав", delete_after=15)
            await ctx.message.delete()
            return

        awaiting_channel = self.bot.get_channel(VOICE_CHANNEL_id[0])
        squad_1_channel = self.bot.get_channel(VOICE_CHANNEL_id[1])
        squad_2_channel = self.bot.get_channel(VOICE_CHANNEL_id[2])

        for users1 in ctx.author.guild.members:
            for users2 in global_varuables.Tir_users:
                if users1.id == users2.id:
                    
                    if users1.status.value != 'offline':
                        users2.online_status = True
                    else:
                        users2.online_status = False

                    users2.in_voice_channel = False

                    if (users1 in awaiting_channel.members) or (users1 in squad_1_channel.members) or (users1 in squad_2_channel.members):
                        users2.in_voice_channel = False
                    else:
                        users2.in_voice_channel = True


                
        await ctx.send(f"Срочно на ПБ!")
        for users in global_varuables.Tir_users:
            if (users.user_status and users.online_status):
           
                users.check_activity()

                if (users.active_status and users.in_voice_channel):
                    
                    await ctx.send(f"<@{users.id}>")
                    #await ctx.send(f"{users.nick}")

        await ctx.message.delete()



def setup(bot):
    bot.add_cog(setup_commands(bot))