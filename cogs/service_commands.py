import disnake
from disnake.ext import commands, tasks
from datetime import datetime, date
from TOKEN import *
import os
import global_varuables





class service_commands(commands.Cog):



    def __init__(self, bot):
        self.bot=bot



    @commands.command()
    async def print_table(self, ctx, table_type):

        if table_type == 'activity':
            index_marker = 0
            index_corrector = 0
        elif table_type == 'schedule':
            index_marker = 3
            index_corrector = 0
        elif table_type == 'setup':
            index_marker = 0
            index_corrector = 3
        else:
            return

        for i in range(3 + index_corrector):
                
            if global_varuables.old_table_id[i+index_marker]:
                
                tmp = await self.bot.get_context(self.bot.get_message(global_varuables.old_table_id[i+index_marker]))
                await tmp.message.delete()
                        

        channel = self.bot.get_channel(global_varuables.CHANNEL_id)
        embeds = global_varuables.make_embed()
                    
                
        for i in range(3 + index_corrector):
            
            if embeds[i+index_marker]:
                tmp = await channel.send(embed = embeds[i+index_marker])
                global_varuables.old_table_id[i+index_marker] = tmp.id
            else:
                global_varuables.old_table_id[i+index_marker] = 0



def setup(bot):
    bot.add_cog(service_commands(bot))