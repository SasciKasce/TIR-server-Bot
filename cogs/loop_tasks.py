import disnake
from disnake.ext import commands, tasks
from datetime import datetime, date
from TOKEN import *
import os
import global_varuables
import requests
from bs4 import BeautifulSoup





class loop_tasks(commands.Cog):



    def __init__(self, bot):
        self.bot=bot
        self.update_status.start()
        self.update_table.start()
        self.save_logs_loop.start()
        self.loop_message_1.start()
        self.check_scores.start()
        self.update_played_time.start()



    @tasks.loop(seconds=15)
    async def update_status(self):

        if global_varuables.log_flag or global_varuables.setup_flag:
            return

        global_varuables.current_datetime = datetime.now()

        for guilds1 in self.bot.guilds:
            if guilds1.id == TIR_id:
                break

        for users1 in guilds1.members:
            flag = True
            for users2 in global_varuables.Tir_users:
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
                global_varuables.Tir_users.append(global_varuables.TirUsr(users1.id))
                break





    @tasks.loop(hours=8)
    async def update_table(self):

        if global_varuables.log_flag or global_varuables.setup_flag:
            return

        for users in global_varuables.Tir_users:
            users.check_activity()
        
        for i in range(6):
                
            if global_varuables.old_table_id[i]:
                
                tmp = await self.bot.get_context(self.bot.get_message(global_varuables.old_table_id[i]))
                await tmp.message.delete()
                        

        channel = self.bot.get_channel(global_varuables.CHANNEL_id)
        embeds = global_varuables.make_embed()
                    
                
        for i in range(6):
            
            if embeds[i]:
                tmp = await channel.send(embed = embeds[i])
                global_varuables.old_table_id[i] = tmp.id
            else:
                global_varuables.old_table_id[i] = 0





    @tasks.loop(hours=1)
    async def save_logs_loop(self):

        if global_varuables.log_flag or global_varuables.setup_flag:
            return

        global_varuables.save_logs()





    @tasks.loop(hours=35)
    async def loop_message_1(self):

        if global_varuables.log_flag or global_varuables.setup_flag:
            return

        channel = self.bot.get_channel(777899864510955523)
        msg = await channel.send(f"## Кто может, кто часто играет, пишите в чаты\n\nПолк Tir набирает игроков для совместной игры и полковых боев. Адекватный коллектив, полковые с 17:00 до 20:00МСК, обучение, связь дискорд. Подробности в лс\n@everyone ")





    #@tasks.loop(minutes=1)
    @tasks.loop(seconds=10)
    async def update_played_time(self):

        if global_varuables.log_flag or global_varuables.setup_flag:
            return

        squad = 0

        for flags in global_varuables.squad_flag:

            if flags:

                edit_flag = False
                user_components = []
                squad_channel = self.bot.get_channel(VOICE_CHANNEL_id[squad + 1])

                for members1 in global_varuables.now_playing_squad[squad]:
                    
                    remove_flag = True

                    for users in global_varuables.Tir_users:

                        if users.id == members1[0] and members1[2] == 1:
                            users.played_time = users.played_time + 1


                    for members2 in squad_channel.members:

                        if members2.id == members1[0]:

                            remove_flag = False

                            label = str(members1[1])
                            custom_id = str(members1[0]) + '_' + str(members1[2])

                            if members1[2] == 1:
                                style = disnake.ButtonStyle.success

                            elif members1[2] == 0:
                                style = disnake.ButtonStyle.danger

                            elif members1[2] == 2:
                                style = disnake.ButtonStyle.secondary

                            Button = disnake.ui.Button(label=label, 
                                                       style=style, 
                                                       custom_id=custom_id)

                            user_components.append(Button)


                    if remove_flag:
                        global_varuables.now_playing_squad[squad].remove(members1)
                        edit_flag = True




                for members2 in squad_channel.members:
                    add_flag = True

                    for members1 in global_varuables.now_playing_squad[squad]:

                        if members2.id == members1[0]:
                            add_flag = False


                    if add_flag:

                        edit_flag = True

                        global_varuables.now_playing_squad[squad].append([members2.id, members2.nick, 2])

                        label=members2.nick
                        custom_id = str(members2.id) + '_2'

                        Button = disnake.ui.Button(label=label, 
                                                   style=disnake.ButtonStyle.secondary, 
                                                   custom_id=custom_id)

                        user_components.append(Button)


                print(global_varuables.squad_inter_id[squad], squad)
                
                if edit_flag:
                    msg = self.bot.get_message(global_varuables.squad_inter_id[squad])
                    await msg.edit(components=user_components)

            squad = squad + 1





    @tasks.loop(minutes=1)
    async def check_scores(self):

        if global_varuables.log_flag or global_varuables.setup_flag:
            return
        
        response = requests.get(global_varuables.url)

        soup = BeautifulSoup(response.text, "lxml")
        data = soup.find("div", class_="squadrons-counter__value").text
        data = int(data)

        #channel_tmp = self.bot.get_channel(CHANNEL_service_id)
        #msg = await channel_tmp.send(f"{global_varuables.game_count[0]} | data {data} | old {global_varuables.scores_before} | new {global_varuables.scores_after} | {global_varuables.loup_count}")

        global_varuables.scores_after = data

        channel = self.bot.get_channel(CHANNEL_SB_id)


        if global_varuables.scores_after != global_varuables.scores_before:

            if not global_varuables.game_count[0]:
                global_varuables.game_count[0] = True
                msg = await channel.send(f"## Полковые \n \n   ### бои\n   побед: {global_varuables.game_count[1]}   \n   поражений: {global_varuables.game_count[2]}   \n   всего игр: {global_varuables.game_count[3]} \n### очки \n   начальные: {global_varuables.scores_before}\n")
                global_varuables.played_games_id = msg.id
                global_varuables.squadron_battle_date = datetime.now()
                global_varuables.starting_scores = global_varuables.scores_before


            if global_varuables.scores_after > global_varuables.scores_before:
                global_varuables.game_count[1] = global_varuables.game_count[1] + 1

            else:
                global_varuables.game_count[2] = global_varuables.game_count[2] + 1


            global_varuables.game_count[3] = global_varuables.game_count[3] + 1
            global_varuables.scores_before = global_varuables.scores_after

            global_varuables.loup_count = 0

            msg = self.bot.get_message(global_varuables.played_games_id)

            if msg == None:
                #msg = await channel.send(f"## Полковые \n \n   ### бои\n   побед: {global_varuables.game_count[1]}   \n   поражений: {global_varuables.game_count[2]}   \n   всего игр: {global_varuables.game_count[3]} \n### очки \n   начальные: {global_varuables.starting_scores} \n   промежуточные: {global_varuables.scores_after}\n   разница: {global_varuables.scores_after - global_varuables.starting_scores}")
                msg = await channel.send(f"## Полковые \n \n### очки \n   начальные: {global_varuables.starting_scores} \n   промежуточные: {global_varuables.scores_after}\n   разница: {global_varuables.scores_after - global_varuables.starting_scores}\n")
                global_varuables.played_games_id = msg.id

            else:

                #await msg.edit(f"## Полковые \n \n   ### бои\n   побед: {global_varuables.game_count[1]}   \n   поражений: {global_varuables.game_count[2]}   \n   всего игр: {global_varuables.game_count[3]} \n### очки \n   начальные: {global_varuables.starting_scores} \n   промежуточные: {global_varuables.scores_after}\n   разница: {global_varuables.scores_after - global_varuables.starting_scores}")
                await msg.edit(f"## Полковые \n \n### очки \n   начальные: {global_varuables.starting_scores} \n   промежуточные: {global_varuables.scores_after}\n   разница: {global_varuables.scores_after - global_varuables.starting_scores}\n")


        if global_varuables.game_count[0]:
            global_varuables.loup_count = global_varuables.loup_count + 1

            if global_varuables.loup_count > 90:

                string = str(global_varuables.squadron_battle_date.day) + '-' + str(global_varuables.squadron_battle_date.month) + '-' + str(global_varuables.squadron_battle_date.year)
                msg = self.bot.get_message(global_varuables.played_games_id)

                if msg == None:
                    #msg = await channel.send(f"## Полковые {string} итог \n \n### бои\n   побед: {global_varuables.game_count[1]}   \n   поражений: {global_varuables.game_count[2]}   \n   всего игр: {global_varuables.game_count[3]} \n### очки \n   начальные: {global_varuables.starting_scores} \n   конченые: {global_varuables.scores_after}\n   разница: {global_varuables.scores_after - global_varuables.starting_scores}")
                    msg = await channel.send(f"## Полковые {string} итог \n \n### очки \n   начальные: {global_varuables.starting_scores} \n   конченые: {global_varuables.scores_after}\n   разница: {global_varuables.scores_after - global_varuables.starting_scores}\n")

                else:
                    #await msg.edit(f"## Полковые {string} итог \n \n### бои\n   побед: {global_varuables.game_count[1]}   \n   поражений: {global_varuables.game_count[2]}   \n   всего игр: {global_varuables.game_count[3]} \n### очки \n   начальные: {global_varuables.starting_scores} \n   конченые: {global_varuables.scores_after}\n   разница: {global_varuables.scores_after - global_varuables.starting_scores}")
                    await msg.edit(f"## Полковые {string} итог \n \n### очки \n   начальные: {global_varuables.starting_scores} \n   конченые: {global_varuables.scores_after}\n   разница: {global_varuables.scores_after - global_varuables.starting_scores}\n")

                global_varuables.game_count[0] = False
                global_varuables.game_count[1] = 0
                global_varuables.game_count[2] = 0
                global_varuables.game_count[3] = 0
                
                global_varuables.played_games_id = 0
                
                global_varuables.loup_count = 0

                global_varuables.starting_scores = -1





    @commands.slash_command(name = "config4")
    async def config4(self, ctx, num: int):


        channel_tmp = self.bot.get_channel(CHANNEL_service_id)

        if num == 0:

            string = ''
            string = string + "1. update_status "      + str(self.update_status.is_running()) + "\n"
            string = string + "2. update_table "       + str(self.update_table.is_running()) + "\n"
            string = string + "3. save_logs_loop "     + str(self.save_logs_loop.is_running()) + "\n"
            string = string + "4. loop_message_1 "     + str(self.loop_message_1.is_running()) + "\n"
            string = string + "5. check_scores "       + str(self.check_scores.is_running()) + "\n"
            string = string + "6. update_played_time " + str(self.update_played_time.is_running()) + "\n"

            msg = await channel_tmp.send(f"{string}")


        elif num == 1:
            if not self.update_status.is_running():
                self.update_status.start()
        
        elif num == 2:
            if not self.update_table.is_running():
                self.update_table.start()

        elif num == 3:
            if not self.save_logs_loop.is_running():
                self.save_logs_loop.start()

        elif num == 4:
            if not self.loop_message_1.is_running():
                self.loop_message_1.start()

        elif num == 5:
            if not self.check_scores.is_running():
                self.check_scores.start()

        elif num == 6:
            if not self.update_played_time.is_running():
                self.update_played_time.start()


        elif num == 10:
            if self.update_status.is_running():
                await self.update_status()
        
        elif num == 20:
            if self.update_table.is_running():
                await self.update_table()

        elif num == 30:
            if self.save_logs_loop.is_running():
                await self.save_logs_loop()

        elif num == 40:
            if self.loop_message_1.is_running():
                await self.loop_message_1()

        elif num == 50:
            if self.check_scores.is_running():
                await self.check_scores()

        elif num == 60:
            if self.update_played_time.is_running():
                await self.update_played_time()



def setup(bot):
    bot.add_cog(loop_tasks(bot))