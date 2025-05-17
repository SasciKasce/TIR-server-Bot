import disnake
from disnake.ext import commands, tasks
from datetime import datetime, date
from TOKEN import *
import os
import global_varuables





class configs(commands.Cog):



    def __init__(self, bot):
        self.bot=bot



    @commands.slash_command()
    async def config1(self, ctx, channel_id: str, message_id: str):
    
        access_flag = True
        for roles in ctx.author.roles:
            if ( (ctx.author.id == MY_id) or (roles.id in admin_roles) ):
                access_flag = False
                break
                
        if access_flag:
            await ctx.send(f"Недостаточно прав", delete_after=15)
            return

        channel_id = int(channel_id)
        message_id = int(message_id)

        channel = self.bot.get_channel(channel_id) # Channel ID
        msg = await channel.fetch_message(message_id) # Message ID
        await msg.delete()
        await ctx.send(f"message deleted", delete_after=15)
        
        return





    @commands.slash_command()
    async def config2(self, ctx, channel_id: str, message_id: str):
    
        access_flag = True
        for roles in ctx.author.roles:
            if ( (ctx.author.id == MY_id) or (roles.id in admin_roles) ):
                access_flag = False
                break
                
        if access_flag:
            await ctx.send(f"Недостаточно прав", delete_after=15)
            return

        channel_id = int(channel_id)
        message_id = int(message_id)

        channel = self.bot.get_channel(channel_id)
        msg = await channel.fetch_message(message_id)
        await msg.pin()
        await ctx.send(f"message pinned", delete_after=15)
        
        return





    @commands.slash_command()
    async def config3(self, ctx, channel_id: str, message_id: str):
    
        access_flag = True
        for roles in ctx.author.roles:
            if ( (ctx.author.id == MY_id) or (roles.id in admin_roles) ):
                access_flag = False
                break
                
        if access_flag:
            await ctx.send(f"Недостаточно прав", delete_after=15)
            return

        channel_id = int(channel_id)
        message_id = int(message_id)

        channel = self.bot.get_channel(channel_id)
        msg = await channel.fetch_message(message_id)

        for emojies in global_varuables.emojies:
            await msg.add_reaction(emojies)





    #@commands.slash_command(name = "config4", description = "снять статус неактивен")
    #async def config4(self, ctx, loop_num: int):






    @commands.command()
    async def stop_Tir_Bot(self, ctx):
    
        access_flag = True
        for roles in ctx.author.roles:
            if ( (ctx.author.id == MY_id) or (roles.id in admin_roles) ):
                access_flag = False
                break
                
        if access_flag:
            await ctx.send(f"Недостаточно прав", delete_after=15)
            return
    
        await ctx.message.delete()

        await ctx.send(f"bot stoped", delete_after=15)
    
        exit()





def setup(bot):
    bot.add_cog(configs(bot))