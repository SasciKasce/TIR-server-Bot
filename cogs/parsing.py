import disnake
from disnake.ext import commands, tasks
from datetime import datetime, date
from TOKEN import *
import os
import global_varuables
import requests
from bs4 import BeautifulSoup




class parsing(commands.Cog):



    def __init__(self, bot):
        self.bot=bot



    @commands.command()
    async def sb_stop(self, ctx):

        if global_varuables.log_flag or global_varuables.setup_flag:
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

        if not global_varuables.game_count[0]:
            await ctx.send(f"Отсчёт ещё не идёт", delete_after=15)
            await ctx.message.delete()
            return

        string = str(global_varuables.squadron_battle_date.day) + '-' + str(global_varuables.squadron_battle_date.month) + '-' + str(global_varuables.squadron_battle_date.year)
        msg = self.bot.get_message(global_varuables.played_games_id)

        if msg == None:
            msg = await channel.send(f"## Полковые {string} итог \n \n### очки \n   начальные: {global_varuables.starting_scores} \n   конченые: {global_varuables.scores_after}\n   разница: {global_varuables.scores_after - global_varuables.starting_scores}")

        else:
            await msg.edit(f"## Полковые {string} итог \n \n### очки \n   начальные: {global_varuables.starting_scores} \n   конченые: {global_varuables.scores_after}\n   разница: {global_varuables.scores_after - global_varuables.starting_scores}")

        global_varuables.game_count[0] = False
        global_varuables.game_count[1] = 0
        global_varuables.game_count[2] = 0
        global_varuables.game_count[3] = 0
                
        global_varuables.played_games_id = 0
                
        global_varuables.loup_count = 0

        global_varuables.starting_scores = -1

        await ctx.send(f"Отсчёт остановлен", delete_after=15)
        await ctx.message.delete()
        


def setup(bot):
    bot.add_cog(parsing(bot))