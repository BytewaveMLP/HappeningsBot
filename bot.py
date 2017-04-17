import discord
import asyncio
import configparser
import os.path
import sys
import traceback

config = configparser.ConfigParser()

if os.path.isfile('./config.ini'):
	config.read('./config.ini')
else:
	config['Command'] = {'Prefix': '+hb',
						 'Subscribe': 'sub',
						 'Unsubscribe': 'unsub',
						 'Help': 'help'}
	config['API Keys'] = {'Discord': ''}

	with open('./config.ini', 'w') as cfgfile:
		config.write(cfgfile)

	print('[HB]: Config file generated.')
	print('[HB]: Edit config.ini before restarting.')
	sys.exit(1)

DISCORD_API_TOKEN = config.get('API Keys', 'Discord')
COMMAND_PREFIX    = config.get('Command', 'Prefix')
COMMAND_SUBSCRIBE = config.get('Command', 'Subscribe')
COMMAND_SUBSCRIBE = config.get('Command', 'Unsubscribe')
COMMAND_HELP      = config.get('Command', 'Help')
SUBSCRIBE         = COMMAND_PREFIX + COMMAND_SUBSCRIBE
UNSUBSCRIBE       = COMMAND_PREFIX + COMMAND_UNSUBSCRIBE
HELP              = COMMAND_PREFIX + COMMAND_HELP
GAME_STATUS       = HELP + ' for help'

client = discord.Client()
helpgame = discord.Game(name = GAME_STATUS, url = '', type = 0)

@client.event
async def on_ready():
	username = client.user.name
	idnum    = client.user.id
	print('[HB]: Logged in.')
	print('[HB]: USER: ' + username)
	print('[HB]: ID:   ' + idnum)
	await client.change_presence(game = helpgame, afk = False)

@client.event
async def on_message(message):
	user = message.author
	channel = message.channel
	server = message.server
	content = message.content

	if not user.bot and content in (SUBSCRIBE, UNSUBSCRIBE, HELP):
		await client.send_typing(channel)
		news_role = None

		for role in server.roles:
			if role.name == 'News':
				news_role = role

		if news_role == None:
			await client.send_message(channel, '**ERROR:** No @News role found. Please create an @News role!')
			return

		if content == SUBSCRIBE:
			for role in user.roles:
				if role == news_role:
					await client.send_message(channel, user.mention + ' - You\'re already subscribed!')
					return

			await client.add_roles(user, news_role)
			await clent.send_message(channel, user.mention + ' - Successfully subscribed to News!')
		elif content == UNSUBSCRIBE:
			for role in user.roles:
				if role == news_role:
					await client.remove_roles(user, news_role)
					await clent.send_message(channel, user.mention + ' - Successfully unsubscribed from News!')
					return

			await client.send_message(channel, user.mention + ' - You aren\'t subscribed!')
		elif content == HELP:
			await client.send_message(channel, user.mention + ' - Hi, I\'m ' + client.user.name + '! Here\'s what I\'m programmed to do:\n'
				+ ' - **' + SUBSCRIBE + '** - Subscribes you to the News channel\n'
				+ ' - **' + UNSUBSCRIBE + '** - Unsubscribes you from the News channel\n')

@client.event
async def on_error(event, *args, **kwargs):
	ex = sys.exc_info()
	print('!!!!!!')
	print('ERROR:     ' + ex[0].__name__ + ' occurred in ' + event + '!')
	print('           ' + str(ex[1]))
	print('Traceback:')
	print("".join(traceback.format_tb(ex[2])), end = '')
	print('!!!!!!')

@client.event
async def on_server_join(server):
	general = server.default_channel
	if server.me.permissions_in(general).send_messages:
		await client.send_message(general, "**Hey there!** I'm " + client.user.name + "! I help with subscribing to news and announcements.\n"
			+ "If you want to see what I do, type **" + HELP + "** in chat!\n"
			+ "*Made with <3 by Bytewave (https://github.com/BytewaveMLP/HappeningsBot)*\n")

client.run(DISCORD_API_TOKEN)
