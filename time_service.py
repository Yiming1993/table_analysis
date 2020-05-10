import datetime
import re

'''
提供时间类服务
'''

month_dict = {'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6, 'July': 7,
		                   'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12,
						   'JANUARY': 1, 'FEBUARY': 2, 'MARCH': 3, 'APRIL': 4, 'JUNE': 6, 'JULY': 7,
						   'AUGUST': 8, 'SEPTEMBER': 9, 'OCTOBER': 10, 'NOVEMBER': 11, 'DECEMBER': 12,
		                   'JAN': 1, 'FEB': 2, 'MAR': 3, 'APR': 4, 'MAY': 5, 'JUN': 6, 'JUL': 7,
		                   'AUG': 8, 'SEP': 9, 'OCT': 10, 'NOV': 11, 'DEC': 12,
						   'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'Jun': 6, 'Jul': 7,
						   'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12 }

def get_today():
    return str(datetime.datetime.now())[:10]

def date_transfer(date, transfer_tag, with_digit_check=True, reverse = False):
    if reverse == False:
        if with_digit_check == True:
            date = date.split(transfer_tag)
            year = date[0]
            if len(date) == 2:
                month = date[1]
                if len(month) < 2:
                    month = '0' + month
                return year + '-' + month

            if len(date) == 3:
                month = date[1]
                day = date[2]
                if len(month) < 2:
                    month = '0' + month
                if len(day) < 2:
                    day = '0' + day
                return year + '-' + month + '-' + day
        else:
            return '-'.join(date.split(transfer_tag))
    else:
        if with_digit_check == True:
            date = date.split(transfer_tag)
            year = date[2]
            if len(date) == 2:
                month = date[1]
                if len(month) < 2:
                    month = '0' + month
                return year + '-' + month

            if len(date) == 3:
                month = date[0]
                day = date[1]
                year = date[2]
                if len(month) < 2:
                    month = '0' + month
                if len(day) < 2:
                    day = '0' + day
                return year + '-' + month + '-' + day
        else:
            return '-'.join(date.split(transfer_tag))

def date_calculate(rank = 3, direction = 'forward'):
    if direction == 'forward':
        date = datetime.datetime.now() + datetime.timedelta(days=rank)
        return str(date)[:10]
    else:
        date = datetime.datetime.now() - datetime.timedelta(days=rank)
        return str(date)[:10]

def language2time(sentence, direction = 'forward'):
    if direction == 'forward':
        rank = re.findall(r'[0-9]{0,4}',sentence)[0]
        if 'day' in sentence:
            date = datetime.datetime.now() + datetime.timedelta(days=rank)
            return str(date)[:10]
        if 'hour' in sentence:
            date = datetime.datetime.now() + datetime.timedelta(hours=rank)
            return str(date)[:10]
        if 'week' in sentence:
            date = datetime.datetime.now() + datetime.timedelta(weeks=rank)
            return str(date)[:10]
        if 'minute' in sentence:
            date = datetime.datetime.now() + datetime.timedelta(minutes=rank)
            return str(date)[:10]
        if 'month' in sentence:
            date = datetime.datetime.now() + datetime.timedelta(days=rank*30)
            return str(date)[:10]
        if 'year' in sentence:
            date = datetime.datetime.now() + datetime.timedelta(days=rank * 365)
            return str(date)[:10]

    else:
        rank = re.findall(r'[0-9]{0,4}',sentence)[0]
        rank = int(rank)
        if 'day' in sentence:
            date = datetime.datetime.now() - datetime.timedelta(days=rank)
            return str(date)[:10]
        if 'hour' in sentence:
            date = datetime.datetime.now() - datetime.timedelta(hours=rank)
            return str(date)[:10]
        if 'week' in sentence:
            date = datetime.datetime.now() - datetime.timedelta(weeks=rank)
            return str(date)[:10]
        if 'minute' in sentence:
            date = datetime.datetime.now() - datetime.timedelta(minutes=rank)
            return str(date)[:10]
        if 'month' in sentence:
            date = datetime.datetime.now() - datetime.timedelta(days=rank*30)
            return str(date)[:10]
        if 'year' in sentence:
            date = datetime.datetime.now() - datetime.timedelta(days=rank * 365)
            return str(date)[:10]

def timestamp2time(time_stamp):
    time_stamp = time_stamp
    date_array = datetime.datetime.utcfromtimestamp(time_stamp)
    date = date_array.strftime("%Y-%m-%d")
    return date
