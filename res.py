@bot.listen()
async def on_message(message):

    if message.author.bot or (message.content[0] in symbols):
        return

    if log_flag and setup_flag:
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




