import discord
import constants
import message_maker
import commendation_handler
import join_timer

intents = discord.Intents.default()
intents.members = True
bot = discord.Client(intents=intents)

join_log = {}
ban_log = {}
commends_log = {}
banned = []

@bot.event
async def on_ready():
    print(f"{bot.user} has connected succesfully!")

@bot.event
async def on_member_join(member):
    timer = join_timer.Timer(constants.AFK_TIME_LIMIT, kick_user(member))
    join_log[str(member.id)] = timer

    bantimer = join_timer.Timer(60, remove_from_ban(member))
    ban_log[str(member.id)] = (bantimer, member)

    channel = bot.get_channel(constants.WELCOME_CHANNEL)
    rules = message_maker.get_rules()
    await channel.send(f"Ave, Warrior! Welcome to the Impera Discord, <@{member.id}>!{constants.WELCOME_MESSAGE}{rules}")

    if len(ban_log) >= 5:
        await ban_all()

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # Help command handler
    elif message.content.startswith("i!help"):
        msg = f"i!commend: This command will shoutout a member. It can be used in <#{constants.COMMEND_CHANNEL}> once every 24 hours but only on the same person every 48 hours."
        if message.channel.id == constants.ADMINISTRATOR_BOT_COMMANDS_CHANNEL:
            msg += "\ni!undo: This command will unban all members banned from most recent raid."
            msg += "\ni!scoreboard: This command will list how many times each member has been commended."
        await message.channel.send(msg)

    # Message handling for introductions
    elif message.channel.id == constants.INTRODUTION_CHANNEL:
        print(message.content)
        if str(message.author.id) in join_log:
            join_log[str(message.author.id)].cancel()
            join_log.pop(str(message.author.id), None)
        botmessage = message_maker.make_message(message.content, message.author)
        channel = message.channel
        await channel.send(botmessage)
        role = discord.utils.get(message.guild.roles, name = "member")
        #await message.author.add_roles(role)

    # Message handling for shout outs and praise channel
    elif message.channel.id == constants.COMMEND_CHANNEL:
        channel = message.channel
        if message.content.startswith('i!commend'):
            if len(message.mentions) > 1:
                await channel.send(f"Sorry <@{message.author.id}>, you can only commend one person at a time!")
            elif len(message.mentions) == 0:
                await channel.send(f"<@{message.author.id}>, please mention someone to commend")
            else:
                if str(message.author.id) in commends_log:
                    if str(message.mentions[0].id) in commends_log[str(message.author.id)]:
                        await channel.send(f"Sorry <@{message.author.id}>, you have already commended that user in the past 48 hours!")
                    elif commends_log[str(message.author.id)]["capable"] == False:
                        await channel.send(f"Sorry <@{message.author.id}>, you have already commended someone in the past 24 hours!")
                    else:
                        await commendation_handler.mod_json(message.mentions[0].id, message.mentions[0].name, message.mentions[0].discriminator)
                        await commend(channel, message.author, message.mentions[0])
                else:
                    await commendation_handler.mod_json(message.mentions[0].id, message.mentions[0].name, message.mentions[0].discriminator)
                    await commend(channel, message.author, message.mentions[0], present=False)
        else:
            await channel.send(f"<@{message.author.id}>, please only use this channel to commend someone using: !commend @user, or see scoreboard: !scoreboard")

    # Message handler for administrator-bot-commands channel
    elif message.channel.id == constants.ADMINISTRATOR_BOT_COMMANDS_CHANNEL or message.channel.id == constants.ADMIN_BOT_CHANNEL2:
        channel = message.channel
        if message.content.startswith("i!scoreboard"):
            await channel.send(commendation_handler.get_commends())
        elif message.content.startswith("!unban"):
            await unban_all()

async def kick_user(user):
    msg = constants.KICK_MESSAGE
    await user.send(msg)
    await user.kick()

async def remove_from_ban(user):
    ban_log.pop(str(user.id), None)

async def ban_all():
    while len(banned) > 0:
        banned.pop()
    msg = constants.BAN_MESSAGE
    admin_msg = f"I have banned {len(ban_log)} people for a suspected bot raid. Use !unban to unban them. Their names are as followed:"
    for id in ban_log:
        user = ban_log[id][1]
        await user.send(msg)
        await user.ban()
        banned.append(user)
        admin_msg += "\n" + str(user.name) + "#" + str(user.discriminator)

    channel = bot.get_channel(constants.ADMINISTRATOR_BOT_COMMANDS_CHANNEL)
    await channel.send(admin_msg)

async def commends_log_handler(user, mention):
    if str(user.id) in commends_log:
        commends_log[str(user.id)].pop(str(mention), None)

async def commends_log_daily_handler(user):
    if str(user.id) in commends_log:
        commends_log[str(user.id)]["capable"] = True

async def commend(channel, author, mention, present=True):
    await channel.send(f"Congratulations <@{mention.id}>! You have been commended!")
    commend_user_timer = join_timer.Timer(constants.COMMEND_SAME_USER_TIME, commends_log_handler(author, mention.id))
    if present:
        commends_log[str(author.id)]["capable"] = False
        commends_log[str(author.id)][str(mention.id)] = commend_user_timer
    else:
        commends_log[str(author.id)]= {
            str(mention.id): commend_user_timer,
            "capable": False
        }
    join_timer.Timer(constants.COMMEND_USER_TIME, commends_log_daily_handler(author))

async def unban_all():
    for user in banned:
        await user.unban()
    while len(banned) > 0:
        banned.pop()

bot.run(constants.TOKEN)
