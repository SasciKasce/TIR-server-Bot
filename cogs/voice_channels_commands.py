import disnake
from disnake.ext import commands, tasks
from datetime import datetime, date
from TOKEN import *
import os
import global_varuables





class voice_channels_commands(commands.Cog):



    def __init__(self, bot):
        self.bot=bot



    @commands.command()
    async def move1(self, ctx):
    
        access_flag = True
        for roles in ctx.author.roles:
            if ( (ctx.author.id == MY_id) or (roles.id in admin_roles) ):
                access_flag = False
                break
                
        if access_flag:
            await ctx.send(f"Недостаточно прав", delete_after=15)
            await ctx.message.delete()
            return

        flag = False
        user_quantity = 0

        awaiting_channel = self.bot.get_channel(VOICE_CHANNEL_id[0])
        squad_1_channel = self.bot.get_channel(VOICE_CHANNEL_id[1])

        for members in awaiting_channel.members:
            await members.move_to(channel = squad_1_channel)
            flag = True



        if flag:

            user_quantity = 0
            for members in squad_1_channel.members:
                user_quantity = user_quantity + 1
                

            await ctx.send(f"команда 1 готова! \n{user_quantity}/8 игроков", delete_after=15)
        else:
            await ctx.send(f"в ожидающих никого нет!", delete_after=15)

        await ctx.message.delete()





    @commands.command()
    async def move2(self, ctx):
    
        access_flag = True
        for roles in ctx.author.roles:
            if ( (ctx.author.id == MY_id) or (roles.id in admin_roles) ):
                access_flag = False
                break
                
        if access_flag:
            await ctx.send(f"Недостаточно прав", delete_after=15)
            await ctx.message.delete()
            return

        flag = False
        user_quantity = 0

        awaiting_channel = self.bot.get_channel(VOICE_CHANNEL_id[0])
        squad_2_channel = self.bot.get_channel(VOICE_CHANNEL_id[2])

        for members in awaiting_channel.members:
            await members.move_to(channel = squad_2_channel)
            flag = True



        if flag:

            for members in squad_2_channel.members:
                user_quantity = user_quantity + 1
                

            await ctx.send(f"команда 2 готова! \n{user_quantity}/8 игроков", delete_after=15)
        else:
            await ctx.send(f"в ожидающих никого нет!", delete_after=15)

        await ctx.message.delete()





#    @commands.command()
#    async def Rains_Of_Castamere(self, ctx):
#
#        file_name = 'The_Rains_of_Castamere_(Red_Wedding_Version)'
#        voice_channel = ctx.message.author.voice.channel
#
#        if not voice_channel:
#            await ctx.send("Вы не находитесь в голосовом канале!")
#            return
#
#        vc = await voice_channel.connect()
#
#        audio_file = f'sounds/{file_name}.mp3'
#
#        if not os.path.isfile(audio_file):
#            await ctx.send(f"Файл {file_name}.mp3 не найден.")
#            return
#
#        source = discord.FFmpegPCMAudio(audio_file)
#
#        vc.play(source)
            



def setup(bot):
    bot.add_cog(voice_channels_commands(bot))