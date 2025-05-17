import disnake
from disnake.ext import commands, tasks
from datetime import datetime, date
from TOKEN import *
import os
import global_varuables





class tracking_commands(commands.Cog):



    def __init__(self, bot):
        self.bot=bot




    @commands.slash_command(name = "начать_полковые", description = "начать отсчёт")
    async def start2(self, inter: disnake.ApplicationCommandInteraction, squad: int):

        if global_varuables.log_flag:
            await inter.response.send_message(f"WARNING logs not loaded <@{MY_id}> upload logs before using the command. Удалить сообщение вручную")
            return

        access_flag = True
    
        for roles in inter.author.roles:
            if ( (inter.author.id == MY_id) or (roles.id in admin_roles) ):
                access_flag = False
                break
                    
        if access_flag:
            await inter.response.send_message(f"Недостаточно прав", delete_after=15)
            return

        if squad != 1 and squad != 2:
            await inter.response.send_message(f"ошмбка ввода данных", delete_after=15)
            return

        squad = squad - 1



        if global_varuables.squad_flag[squad]:
            await inter.response.send_message("отсчёт уже идёт!")
            return

        squad_channel = self.bot.get_channel(VOICE_CHANNEL_id[squad + 1])

        global_varuables.now_playing_squad[squad] = []
        user_components = []

        for members in squad_channel.members:

            global_varuables.now_playing_squad[squad].append([members.id, members.nick, 1])

            label=members.nick
            custom_id = str(members.id)+ '_1'

            Button = disnake.ui.Button(label=label, 
                                       style=disnake.ButtonStyle.success, 
                                       custom_id=custom_id)

            user_components.append(Button)

        global_varuables.squad_flag[squad] = True

        await inter.response.send_message(f"squad {squad + 1} now playing:", components=user_components)
        msg = await inter.original_response()
        global_varuables.squad_inter_id[squad] = msg.id






    @commands.slash_command(name = "оставновить_полковые", description = "остановить отсчёт")
    async def stop2(self, inter: disnake.ApplicationCommandInteraction, squad: int):

        if global_varuables.log_flag:
            await inter.response.send_message(f"WARNING logs not loaded <@{MY_id}> upload logs before using the command. Удалить сообщение вручную")
            return

        access_flag = True
        for roles in inter.author.roles:
            if ( (inter.author.id == MY_id) or (roles.id in admin_roles) ):
                access_flag = False
                break
                
        if access_flag:
            await inter.response.send_message(f"Недостаточно прав", delete_after=15)
            return

        if squad != 1 and squad != 2:
            await inter.response.send_message(f"ошмбка ввода данных", delete_after=15)
            return

        squad = squad - 1


        if not global_varuables.squad_flag[squad]:
            await inter.response.send_message("отсчёт уже остановлен!", delete_after=15)
            return


        msg = self.bot.get_message(global_varuables.squad_inter_id[squad])
        await msg.delete()

        global_varuables.squad_flag[squad] = False
        global_varuables.now_playing_squad[squad] = []
        global_varuables.squad_inter_id[squad] = 0
            
        await inter.response.send_message("отсчёт остановлен!", delete_after=15)
        





    @commands.Cog.listener(name = "on_button_click")
    async def squad_playing(self, inter: disnake.MessageInteraction):

        flag = True

        for rows in global_varuables.now_playing_squad[0]:

            if int(inter.component.custom_id[:-2]) == rows[0]:
                flag = False
                squad = 0
                break

        for rows in global_varuables.now_playing_squad[1]:

            if int(inter.component.custom_id[:-2]) == rows[0]:
                flag = False
                squad = 1
                break
        
        if flag:
            return


        user_components=[]
        index = 0

        now_playing_squad = global_varuables.now_playing_squad[squad]
        squad_channel = self.bot.get_channel(VOICE_CHANNEL_id[squad+1])


        for members in now_playing_squad:

            if members[0] == int(inter.component.custom_id[:-2]):

                if members[2] == 0 or members[2] == 2:
                    now_playing_squad[index][2] = 1
                    custom_id = str(members[0]) + '_1'
                    style = disnake.ButtonStyle.success

                elif members[2] == 1:
                    now_playing_squad[index][2] = 0
                    custom_id = str(members[0]) + '_0'
                    style = disnake.ButtonStyle.danger

            else:

                custom_id = str(members[0]) + '_' + str(members[2])

                if members[2] == 1:
                    style = disnake.ButtonStyle.success

                elif members[2] == 0:
                    style = disnake.ButtonStyle.danger

                elif members[2] == 2:
                    style = disnake.ButtonStyle.secondary


            label = str(members[1])

            Button = disnake.ui.Button(label=label, 
                                       style=style, 
                                       custom_id=custom_id)

            user_components.append(Button)
            index = index + 1

        global_varuables.now_playing_squad[squad] = now_playing_squad
        await inter.response.edit_message(components=user_components)



def setup(bot):
    bot.add_cog(tracking_commands(bot))