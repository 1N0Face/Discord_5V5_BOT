import discord
import random
import time
from discord_webhook import DiscordWebhook, DiscordEmbed

TOKEN = 'ODY2Njk1Mjk4NTA3MDc5Njgx.YPWS5Q.WmETM9ECCAQOz825DTboAF_w60Y'
client = discord.Client()


def helpMsg():
    webhook = DiscordWebhook(url = "https://discord.com/api/webhooks/866824157873963009/kI9DfyfdHWooysAxrLND_FC1lVN9n1E5Ujhwlm5HgAdvcx6OwbulyvmQ1nvs47s35NcO")
    embed = DiscordEmbed(title="**Commands:**", color=242424)
    embed.add_embed_field(name = "**$list**", value = "```cs\n#View the playing players and teams```", inline=False)
    embed.add_embed_field(name = "**$join1**", value = "```cs\n#Join team 1```", inline=False)
    embed.add_embed_field(name = "**$join2**", value = "```cs\n#Join team 2```", inline=False)
    embed.add_embed_field(name = "**$leave**", value = "```cs\n#Leave from the chosen team```", inline=False)
    embed.add_embed_field(name = "**$timeset**", value = "```diff\n-Set time for the match (ꜱᴛaꜰꜰ only)\n!Example: $timeset-XX:XX```", inline=False)
    embed.add_embed_field(name = "**$wipe**", value = "```diff\n-Delete all the player from the list (ꜱᴛaꜰꜰ only)```", inline=False)
    embed.set_thumbnail(url="https://i.ibb.co/3YtVnWG/thumbs.png")
    webhook.add_embed(embed)
    response = webhook.execute()


info = {'time': '**Unset**', 'team1': [], 'team2': []}


def tableMsg():
    webhook = DiscordWebhook(url = "https://discord.com/api/webhooks/866824157873963009/kI9DfyfdHWooysAxrLND_FC1lVN9n1E5Ujhwlm5HgAdvcx6OwbulyvmQ1nvs47s35NcO")
    embed = DiscordEmbed(title="Table for the 5V5:", color=242424)
    printer = "```fix\nTeam1: {0}\nTeam2: {1}```".format(' '.join(info['team1']), ' '.join(info['team2']))
    embed.add_embed_field(name="Time: {0}".format(info['time']), value=printer, inline=False)
    embed.set_thumbnail(url="https://i.gifer.com/5t6T.gif")
    webhook.add_embed(embed)
    response = webhook.execute()


@client.event
async def on_ready():
    print("Logged in as {0.user}".format(client))


def changeStartTime(newTime):
    info['time'] = newTime


def checkTime(newTime):
    try:
        time.strptime(newTime, '%H:%M')
        return True
    except ValueError:
        return False


@client.event
async def on_message(message):
    username = str(message.author).split('#')[0]
    msg = str(message.content)
    channel = str(message.channel.name)


    if message.content.startswith('$help'):
        helpMsg()



    if message.content.startswith('$list'):
        tableMsg()

        
    if message.content.startswith('$join1'):
        if username in info['team1'] or username in info['team2']:
            await message.channel.send('**Error: you are already in the table!**')
        else:
            if len(info['team1']) < 5:
                info['team1'].append(username)
                await message.channel.send('**User: {0} successfully added to team1!**'.format(username))
            else:
                await message.channel.send('**Team1 is full**'.format(username))


    if message.content.startswith('$join2'):
        if username in info['team1'] or username in info['team2']:
            await message.channel.send('**Error: you are already in the table!**')
        else:
            if len(info['team1']) < 5:
                info['team2'].append(username)
                await message.channel.send('**User: {0} successfully added to team2!**'.format(username))
            else:
                await message.channel.send('**Team2 is full**'.format(username))



    if message.content.startswith('$leave'):
        if username not in info['team1'] and username not in info['team2']:
            await message.channel.send('**Error: you are not in any team!**')
        else:
            if username in info['team1']:
                info['team1'].remove(username)
                await message.channel.send('**User: {0} successfully left from team1!**'.format(username))
            if username in info['team2']:
                info['team2'].remove(username)
                await message.channel.send('**User: {0} successfully left from team2!**'.format(username))



    if message.content.startswith('$timeset'):
        if "name='Staff'" in str(message.author.roles) and 'id=868839975712595989' in str(message.author.roles):
            newTime = message.content[message.content.find('-')+1:message.content.find('-')+6]
            if(checkTime(newTime) and message.content.find('-') != -1):
                info['time'] = message.content[message.content.find('-')+1:message.content.find('-')+6]
                await message.channel.send('**Match time successfully set to: {0}**'.format(info['time']))
            else:
                await message.channel.send('**Error: unknown time, try again!**')
        else:
            await message.channel.send('**Error: you are not ꜱᴛaꜰꜰ!**')



    if message.content.startswith('$wipe'):
        if "name='Staff'" in str(message.author.roles[0]) and 'id=868839975712595989' in str(message.author.roles[0]):
            info['team1'] = []
            info['team2'] = []
            await message.channel.send('**Table successfully wiped!**')
        else:
            await message.channel.send('**Error: you are not ꜱᴛaꜰꜰ!**')


    
    if message.author == client.user:
        return
    

client.run(TOKEN)
