import discord
import responses
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import asyncio

#A channel called reminder-bot needs to exist in the server.

async def run_discord_bot():
    TOKEN = #put token here
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)

    events_dict = {}

    @client.event
    async def on_ready(): #function that is called every time the bot comes online
        bot_name = str(client.user).split('#')[0]
        print(f'{bot_name} is online!')

    @client.event
    async def on_message(message): #function that is called every time a message is sent
        user = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel.name)
        bot = str(client.user)

        print(f'{user}: {user_message} ({channel})')

        if user == bot:
            return #the bot processes all messages, this makes sure it can't reply to itself and create a loop

        await send_message(message)

    async def send_message(message): #function to get bot's instant responses from responses.py
        bot_response = responses.get_response(message.content, message.channel.name, events_dict)

        if type(bot_response) == list:
            await add_event(bot_response, message.channel.id)
            if bot_response[5].lower() == '30m':
                when_remind = '30 minutes'
            elif bot_response[5].lower() == '3h':
                when_remind = '3 hours'
            elif bot_response[5].lower() == '1d':
                when_remind = '1 day'
            success = f'Event successfully added! You will be REMinded {when_remind} before the event time.'
            await message.channel.send(success)
        elif bot_response == None:
            return
        else:
            await message.channel.send(bot_response)

    async def add_event(event_data_list, channel_id): #function to add the new event to the event dictionary
        mod_event_list = [event_data_list[2].strip(), event_data_list[3].strip(), event_data_list[4].strip(), channel_id, event_data_list[5].strip(), event_data_list[6], event_data_list[7], event_data_list[8]]
        event_name = event_data_list[1].strip()
        events_dict[event_name] = mod_event_list

    async def check_for_events(events_dict): #function called every minute to check if the current date & time match a scheduled one
        utc_datetime = datetime.now()
        vancouver_datetime = utc_datetime - timedelta(hours=8)
        vancouver_datetime = vancouver_datetime.replace(second=0,microsecond=0)
        event_name_list = list(events_dict.keys())

        for x in range(len(event_name_list)):
            this_key = event_name_list[x]
            this_value = events_dict[this_key]

            if this_value[5] == True:
                x = 30
            elif this_value[6] == True:
                x = 180
            elif this_value[7] == True:
                x = 1440

            mod_vancouver_datetime = vancouver_datetime + timedelta(minutes=x)
            datetime_string = this_value[0] + this_value[1]
            datetime_object = datetime.strptime(datetime_string, '%m-%d-%Y%H:%M')

            if mod_vancouver_datetime == datetime_object:
                await send_reminder(this_key, events_dict)
                await update_event_dictionary(this_key, datetime_object)

    async def send_reminder(event_name, events_dict): #function to get bot reminder from responses.py
        event_info = events_dict[event_name]
        bot_response = responses.get_reminder(event_name, event_info)
        channel = client.get_channel(event_info[3])
        await channel.send(bot_response)

    async def update_event_dictionary(event_name, datetime_object): #function that updates the next reminder date if repreating, or deletes it if not repeating
        event_info = events_dict[event_name]
        repeating = event_info[2].lower()
        if repeating == 'none':
            del events_dict[event_name]
        else:
            if repeating == 'yearly':
                x = 366 #366 days because 2024 is a leap year
                        #if the event is before Feb. 28 2023 and it is repeating yearly it will repeat one day too late
            elif repeating == 'weekly':
                x = 7
            event_date = event_info[0]
            datetime_object = datetime.strptime(event_date, '%m-%d-%Y')

            if repeating == 'yearly' or repeating == 'weekly':
                datetime_object = datetime_object + timedelta(days=x)
            elif repeating == 'monthly':
                datetime_object = datetime_object + relativedelta(months=1)

            datetime_object_str = datetime_object.strftime('%m-%d-%Y')
            events_dict[event_name][0] = datetime_object_str

    asyncio.create_task(client.start(TOKEN))

    while True:
        await asyncio.sleep(60)
        await check_for_events(events_dict)