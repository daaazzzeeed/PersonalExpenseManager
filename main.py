import constants 
import banking
import datetime


dataset = 'dataset.txt'
messages = banking.read_data(dataset)

while 1:
    banking.show_menu()
    try:
        selection = input('Choose: ')

        if selection == '1':
            card1 = banking.get_current_funds(messages, '480')
            card2 = banking.get_current_funds(messages, '720')
            card_numbers = banking.get_my_cards(messages)
            GorgeousBank = card_numbers.pop()
            SuperBank = card_numbers.pop()
            print('1. *' + SuperBank + ' (SuperBank): {money} EUR'.format(money=card1))
            print('2. *' + GorgeousBank + ' (GorgeousBank) {money} EUR'.format(money=card2))

        elif selection == '2':
    
            my_cards = banking.get_my_cards(messages)
            GorgeousBank = my_cards.pop()
            SuperBank = my_cards.pop()
            print('1. *' + SuperBank + ' (SuperBank)')
            print('2. *' + GorgeousBank + ' (GorgeousBank)')
            print('3. Total')
            print('4. Exit to main menu')

            choice = input('Choose: ')

            if choice == '1' or choice == '2':
                message = 'Input Month-Day: '
                date = banking.input_datetime(message)
                date_list = date.split('-')
                results = banking.get_expenses_per_month(messages, date_list)
                if results != 0:
                    index = int(choice) - 1
                    print('Report for {month} {year}, card {card}(SuperBank)'.format(month=datetime.datetime(int(date_list[1]), int(date_list[0]), 1).strftime('%B'), year=date_list[1], card=results[0][index]))
                    print('Received {amount} EUR'.format(amount=results[2][index]))
                    print('Spent {amount} EUR'.format(amount=results[1][index]))
                    print('Delta {amount} EUR'.format(amount=int(results[2][index])-int(results[1][index])))
                else:
                    print('No transactions in specified period')

            elif choice == '3':
                message = 'Input Month-Day: '
                date = banking.input_datetime(message)
                date_list = date.split('-')
                results = banking.get_expenses_per_month(messages, date_list)
                if results != 0:
                    total_expenses = results[1][0] + results[1][1]
                    total_incomes = results[2][0] + results[2][1]
                    index = int(choice) - 1
                    print('Report for {month} {year}: '
                        .format(month=datetime.datetime(int(date_list[1]), int(date_list[0]), 1).strftime('%B'),
                        year=date_list[1]))
                    print('Received {amount} EUR'.format(amount=total_incomes))
                    print('Spent {amount} EUR'.format(amount=total_expenses))
                    print('Delta {amount} EUR'.format(amount=total_incomes - total_expenses))
                else:
                    print('No transactions in specified period')

            elif choice == '4':
                continue
            else:
                print('Choose between 1, 2 or 3')

        elif selection == '3':
            break
        else:
            print('Choose between 1, 2 or 3')
    except KeyboardInterrupt:
        print('Input interrupted')
    


    