import datetime
import calendar


def get_banks(data):
    bank_list = ['480', '720']
    j = 3
    for i in range(len(data)):
        if data[i]['phone'] not in bank_list:
            bank_list.append(data[i]['phone'])
            j += 1
    return bank_list


def menu():
    message = """\nChoose an option
1 - Show current funds
2 - Expenses per month
3 - Exit from the program\n"""
    print(message)


def input_datetime(message):
    while True:
        user_input = input(message)
        try:
            datetime.datetime.strptime(user_input, "%m-%Y")
            return user_input
        except ValueError:
            print("Incorrect format. Use MM-YYYY")


def get_dataset(dataset):
    data = []
    with open(dataset, 'r') as f:
        for line in f:
            t = dict()
            line = line.replace('\n', '').split(';')
            line[2] = line[2].split(' ')
            t['phone'] = line[0]
            t['time'] = line[1]
            t['text'] = line[2]
            data.append(t)
    return data


def get_expenses(data, day, banks):
    expenses = [0 for i in range(len(banks))]
    incomes = [0 for i in range(len(banks))]
    phone_numbers = []
    year = int(day[1])
    month = int(day[0])
    monthrange = calendar.monthrange(year, month)[1]
    day = datetime.datetime(year, month, 1)
    first_day = day.replace(day=1, hour=00, minute=00, second=00, microsecond=0)
    last_day = day.replace(day=monthrange, hour=23, minute=59, second=59, microsecond=0)

    for i in range(len(banks)):
        for item in data:
            day = item['time'].split(' ')[0].split('-')
            year = int(day[2])
            month = int(day[1])
            day = datetime.datetime(year, month, 1)
            phone = item['phone']
            if phone not in phone_numbers:
                phone_numbers.append(phone)

            if first_day <= day <= last_day:

                if banks[i] == '480':
                    if phone == '480':
                        if item['text'][0] == 'Withdrawal':
                            expenses[i] += int(item['text'][2])
                        else:
                            incomes[i] += int(item['text'][2])

                else:
                    if phone == banks[i]:
                        sum_of_transaction = int(item['text'][1])
                        if sum_of_transaction < 0:
                            expenses[i] += abs(int(item['text'][1]))
                        else:
                            incomes[i] += int(item['text'][1])
    return [expenses, incomes, phone_numbers]


def get_cards(data):
    cards_list = []
    for record in data:
        if record['phone'] == '480':
            if record['text'][1] not in cards_list:
                cards_list.append(record['text'][1])
        else:
            if record['text'][0] not in cards_list:
                cards_list.append(record['text'][0])
    return cards_list


def get_current_funds(data, bank_phone):
    latest_date = datetime.datetime(1, 1, 1, 00, 00, 00)
    message = 0
    for record in data:
        if record['phone'] == bank_phone:
            time = record['time']
            time = time.split(' ')
            time[0] = time[0].split('-')
            time[1] = time[1].split(':')
            date = datetime.datetime(int(time[0][2]), int(time[0][1]), int(time[0][0]), int(time[1][0]), int(time[1][1]), int(time[1][2]))
            if date > latest_date:
                latest_date = date
                message = record
    if bank_phone == '480':
        return message['text'][3]
    else:
        return message['text'][2]


