from random import randint
from datetime import datetime, timedelta

def get_response(user_message, channel, events_dict): #function to select appropriate (instant) response

    lowercase_message = user_message.lower()

    if lowercase_message == '!surprise':
        if channel == 'reminder-bot':
            return 'https://www.youtube.com/watch?v=GJ0mO8P37Eg&list=WL&index=13 ( ͡° ͜ʖ ͡°)'
        else:
            return 'Wrong channel! Rem can help you in #reminder-bot.'

    if lowercase_message == '!cursedmike':
        if channel == 'reminder-bot':
            return 'https://media.giphy.com/media/pVuABKLhxv5hk0bAHQ/giphy.gif'
        else:
            return 'Wrong channel! Rem can help you in #reminder-bot.'

    if lowercase_message == '!eventedit':
        if channel == 'reminder-bot':
            return ':pencil: To edit an event, submit a new event under the **same** event name with the updated information. _(Note: This means that you cannot have two events with the same exact name.)_'
        else:
            return 'Wrong channel! Rem can help you in #reminder-bot.'

    elif lowercase_message == '!help':
        if channel == 'reminder-bot':
            return "**All bot commands:** \n \n :blue_heart: `!surprise`: A surprise... \n :blue_heart: `!mood`: Rem's curent mood. \n :blue_heart: `!eventsubmit`: Submit a event to be reminded for! \n :blue_heart: `!eventlist`: List all events. \n :blue_heart: `!eventdelete`: Delete an event. \n :blue_heart: `!eventedit`: Edit an existing event. \n \n _**Note:** All event times should be given in PST, and you will recieve your event reminders in PST._ \n _**Note:** If you submit an event with the same name as a previously existing one, the existing event will be overwritten._"
        else:
            return 'Wrong channel! Rem can help you in #reminder-bot.'

    elif lowercase_message == '!eventlist':
        if channel == 'reminder-bot':
            event_name_list = list(events_dict.keys())

            if len(event_name_list) == 0:
                return 'There are no scheduled events to list! Try !eventsubmit to submit one.'

            event_print = '**All events:** \n \n'

            for x in range(len(event_name_list)):
                this_value = events_dict[event_name_list[x]]
                event_hour = this_value[1][0] + this_value[1][1]
                event_minute = this_value[1][3] + this_value[1][4]
                am_or_pm = 'AM'

                if int(event_hour) > 12:
                    event_hour = str(int(event_hour) - 12)
                    am_or_pm = 'PM'
                if event_hour == '00':
                    event_hour = '12'

                event_print = event_print + '`' + event_name_list[x] + '` on `' + this_value[0] + '`, `' + event_hour + ':' + event_minute + ' ' + am_or_pm + '`'

                if this_value[2].lower() == 'yearly' or this_value[2].lower() == 'monthly' or this_value[2].lower() == 'weekly':
                    event_print = event_print + ', repeating `' + this_value[2].lower() + '`'

                event_print = event_print + ' (reminder `' + this_value[4].lower() + '` before)' + '\n'

            return event_print
        else:
            return 'Wrong channel! Rem can help you in #reminder-bot.'

    elif lowercase_message == '!eventdelete':
        if channel == 'reminder-bot':
            return '**To delete an event, return relevant information in the square brackets on one line.** \n \n :clipboard:  >eventdelete \n :label:  > [Name of Event] \n \n **Ex:**  `>eventdelete >Math Assignment #4`'
        else:
            return 'Wrong channel! Rem can help you in #reminder-bot.'

    elif lowercase_message == 'k':
        return 'k'

    elif lowercase_message[0] == '>' and len(lowercase_message) >= 15:
        if channel == 'reminder-bot':
            event_data_list = user_message.split(">")

            if len(event_data_list) == 3: #eventdelete
                if event_data_list[1].strip() == 'eventdelete':
                    event_name = event_data_list[2].strip()
                    event_name_list = list(events_dict.keys())
                    counter = 0

                    for x in range(len(event_name_list)):
                        if event_name_list[x] == event_name:
                            counter += 1

                    if counter == 1:
                        del events_dict[event_name]
                        return 'Event deleted successfully!'
                    else:
                        return 'This event name does not exist, try again! Maybe you spelled something wrong, or missed a capital letter...'
                else:
                    return 'Sorry, something went wrong in your event deletion! Please correct the issue and try again.'

            elif len(event_data_list) == 6: #eventsubmit
                time = event_data_list[3]
                colons = 0

                for k in range(len(time)):
                    if time[k] == ':':
                        colons += 1

                if colons == 1 and len(event_data_list[2]) == 11 and len(event_data_list[3]) == 6:
                    if event_data_list[4].lower() == "yearly " or event_data_list[4].lower() == "monthly " or event_data_list[4].lower() == "weekly " or event_data_list[4].lower() == "none ":
                        if event_data_list[5].lower() == '30m' or event_data_list[5].lower() == '3h' or event_data_list[5].lower() == '1d':
                            utc_datetime = datetime.now()
                            vancouver_datetime = utc_datetime - timedelta(hours=8)
                            vancouver_datetime = vancouver_datetime.replace(second=0,microsecond=0)
                            mod_vancouver_datetime = vancouver_datetime + timedelta(minutes=30)

                            datetime_string = event_data_list[2] + event_data_list[3]
                            datetime_object = datetime.strptime(datetime_string, '%m-%d-%Y %H:%M ')

                            if datetime_object > mod_vancouver_datetime:
                                thirty_min = False
                                three_hr = False
                                one_day = False

                                if event_data_list[5].lower() == '30m':
                                    thirty_min = True
                                elif event_data_list[5].lower() == '3h':
                                    three_hr = True
                                elif event_data_list[5].lower() == '1d':
                                    one_day = True

                                when_to_remind_list = [thirty_min, three_hr, one_day]
                                event_data_list.extend(when_to_remind_list)
                                print(event_data_list) #TODO remove
                                return event_data_list
                            else:
                                return 'Sorry, your event date is either within 30 minutes of the current time or is in the past. Try again with a valid event date!'
                        else:
                            return 'Sorry, something went wrong in your event submission! Please correct the issue and try again.'
                    else:
                        return 'Sorry, something went wrong in your event submission! Please correct the issue and try again.'
                else:
                    return 'Sorry, something went wrong in your event submission! Please correct the issue and try again.'
            else:
                return 'Sorry, something went wrong in your event submission! Please correct the issue and try again.'

    elif lowercase_message == '!eventsubmit':
        if channel == 'reminder-bot':
            return "**To submit an event, return relevant information in the square brackets on one line.** \n \n :label:  > [Name of Event] \n :calendar:  > [Date of Event as MM-DD-YYYY] \n :alarm_clock:  > [Time of Event as 00:00 in 24h time, PST] \n :repeat:  > [Reapeating Weekly/Monthly/Yearly/None] \n :grey_question:  > [Remind 30m/3h/1d Before] \n \n **Ex:**  `>Christmas Day! >12-25-2023 >00:00 >yearly >30m`"
        else:
            return 'Wrong channel! Rem can help you in #reminder-bot.'

    elif lowercase_message == '!mood':
        if channel == 'reminder-bot':
            mood = randint(0, 6)
            if mood == 0:
                return 'Rem is feeling excited! ৻( •̀ ᗜ •́  ৻)'
            if mood == 1:
                return 'Rem is feeling grumpy... (♯｀∧´)'
            if mood == 2:
                return 'Rem is feeling upset... °՞(ᗒᗣᗕ)՞°'
            if mood == 3:
                return 'Rem is feeling sleepy. (- o - ) zzZ ☽'
            if mood == 4:
                return 'Rem is feeling shy. (ó﹏ò｡ )'
            if mood == 5:
                return 'Rem is feeling relaxed. (✿◡‿◡)'
            if mood == 6:
                return 'Rem is feeling mischievous... ( ＾◡＾)っ✂╰⋃╯'
        else:
            return 'Wrong channel! Rem can help you in #reminder-bot.'

    elif channel == 'reminder-bot':
        return "Sorry, Rem doesn't quite understand! Try !help for a list of commands."

    return

def get_reminder(event_name, event_info): #function to select appropriate (scheduled) response: aka a reminder
    event_date = event_info[0]
    event_month = event_date[0] + event_date[1]
    event_day = event_date[3] + event_date[4]
    event_year = '20' + event_date[8] + event_date[9]
    event_time = event_info[1]
    event_hour = event_time[0] + event_time[1]
    event_minute = event_time[3] + event_time[4]
    am_or_pm = 'AM'

    if int(event_hour) > 12:
        event_hour = int(event_hour) - 12
        am_or_pm = 'PM'
    if event_hour == '00':
        event_hour = '12'

    return f"@here :warning: Don't forget! `{event_name}` is on `{event_month}-{event_day}-{event_year}` at `{event_hour}:{event_minute} {am_or_pm}`! :warning:"