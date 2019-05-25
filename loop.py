import methods
import config
import datetime

data_set = 'records.txt'
records_list = methods.get_data(data_set)

while True:
    methods.message()
    try:
        s = input('Choose action: ')

        if s == '1':
            phone_list = methods.get_bank_list(records_list)
            cards = methods.get_my_cards_list(records_list)

            k = 1
            for p in phone_list:
                current_funds = methods.get_account_states(records_list, p)
                try:
                    print(str(k) + '. *' + cards[k - 1] + ' (' + config.banks[p] + ') : {money} USD'
                          .format(money=methods.get_account_states(records_list, p)))
                    k = k + 1
                except KeyError as ke:
                    print(str(k) + '. *' + cards[k - 1] + ' (Bank' + str(k) + ') : {money} USD'
                          .format(money=methods.get_account_states(records_list, p)))
                    k = k + 1

        elif s == '2':
    
            my_cards = methods.get_my_cards_list(records_list)
            SUPERBANK = str(my_cards[0])
            GORGEOUSBANK = str(my_cards[1])
            print('1. *' + SUPERBANK + ' (SuperBank)')
            print('2. *' + GORGEOUSBANK + ' (GorgeousBank)')

            k = 3
            for j in range(2, len(my_cards), 1):
                print(str(k) + '. *' + str(my_cards[j]) + '(bank' + str(k) + ')')
                k = k + 1
            print(str(k) + '. Total')
            k = k + 1
            print(str(k) + '. Exit to main menu')

            c = input('\nChoose card/action: ')
            if c != str(k) and c != str(k - 1):
                message = 'Input Month-Year: '
                date = methods.get_datetime(message)
                date_list = date.split('-')
                my_banks = methods.get_bank_list(records_list)
                resulting_expenses = methods.get_card_expenses(records_list, date_list, my_banks)
                if sum(resulting_expenses[0]) != 0 or sum():
                    choice = int(c) - 1
                    my_cards = methods.get_my_cards_list(records_list)
                    print('Report for {month} {year}, card {card}'
                          .format(month=datetime.datetime(int(date_list[1]), int(date_list[0]), 1)
                                  .strftime('%B'), year=date_list[1], card=my_cards[len(my_cards) - 1 - choice]))

                    print('Received {amount} USD'.format(amount=resulting_expenses[1][choice]))
                    print('Spent {amount} USD'.format(amount=resulting_expenses[0][choice]))
                    print('Delta {amount} USD'.format(amount=int(resulting_expenses[1][choice]) - int(resulting_expenses[0][choice])))
                    ans = input('Export a full report to Excel? ')
                    if ans == 'y':
                        methods.write_card_expenses_to_xl(records_list, resulting_expenses, choice)
                        print('Report export completed')
                else:
                    print('Nothing found')

            elif c == str(k - 1):
                message = 'Input Date in format: Month-Year: '
                date = methods.get_datetime(message)
                date_to_list = date.split('-')
                resulting_expenses = methods.get_card_expenses(records_list, date_to_list, methods.get_bank_list(records_list))
                if sum(resulting_expenses[0]) != 0 or sum(resulting_expenses[1]) != 0:
                    total_resulting_expenses = sum(resulting_expenses[0])
                    total_resulting_incomes = sum(resulting_expenses[1])
                    choice = int(c) - 1
                    print('Report for {month} {year}: '
                          .format(month=datetime.datetime(int(date_to_list[1]), int(date_to_list[0]), 1).strftime('%B'),
                                  year=date_to_list[1]))
                    print('Received {amount} EUR'.format(amount=total_resulting_incomes))
                    print('Spent {amount} EUR'.format(amount=total_resulting_expenses))
                    print('Delta {amount} EUR'.format(amount=total_resulting_incomes - total_resulting_expenses))
                    if input('Export a full report to Excel?') == 'y':
                        methods.write_all_expenses_to_xl(records_list, resulting_expenses)
                        print('Report export completed')
                else:
                    print('Nothing found')

            elif c == str(k):
                continue
            else:
                print('Input Error')

        elif s == '3':
            break
        else:
            print('Input Error')
    except KeyboardInterrupt:
        print('Program stopped')
    except ValueError:
        print('Value Error')
