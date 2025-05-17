import disnake
from disnake.ext import commands, tasks
from datetime import datetime, date
from TOKEN import *
import os
import global_varuables





class other_commands(commands.Cog):



    def __init__(self, bot):
        self.bot=bot



    @commands.command()
    async def print_leaderboard(self, ctx):


        if global_varuables.log_flag:
            await ctx.send(f"WARNING logs not loaded <@{MY_id}> upload logs before using the command. Удалить сообщение вручную")
            return

        access_flag = True
        for roles in ctx.author.roles:
            if ( (ctx.author.id == MY_id) or (roles.id in admin_roles) ):
                access_flag = False
                break
                
        if access_flag:
            await ctx.send(f"Недостаточно прав", delete_after=15)
            await ctx.message.delete()
            return



        string = '## Liderboard of TIR squadron \n'

        for users in global_varuables.Tir_users:

            if users.played_time > 0 and users.user_status:

                string = string + users.nick + '\n' + 'played_time: ' + str(round(float(users.played_time)/60, 2)) + ' hours' + '\n' + '\n'


        await ctx.send(f"{string}")

        await ctx.message.delete()





    @commands.command()
    async def clear_played_time(self, ctx):

        if global_varuables.log_flag:
            await ctx.send(f"WARNING logs not loaded <@{MY_id}> upload logs before using the command. Удалить сообщение вручную")
            return

        access_flag = True
        for roles in ctx.author.roles:
            if ( (ctx.author.id == MY_id) or (roles.id in admin_roles) ):
                access_flag = False
                break
                
        if access_flag:
            await ctx.send(f"Недостаточно прав", delete_after=15)
            await ctx.message.delete()
            return

        for users in global_varuables.Tir_users:

            users.played_time = 0


        await ctx.send(f"played time cleared", delete_after=15)
        await ctx.message.delete()



def setup(bot):
    bot.add_cog(other_commands(bot))