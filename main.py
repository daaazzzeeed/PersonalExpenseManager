import constants 
import banking


dataset = 'dataset.txt'
messages = banking.read_data(dataset)

while 1:
    banking.show_menu()
    try:
        selection = input('Choose: ')

        if selection == '1':

            my_cards = banking.get_my_cards(messages)

            print('1. *' + my_cards.pop() + ' (SuperBank)')
            print('2. *' + my_cards.pop() + ' (GorgeousBank)')

            card = input('Choose: ')

            if card == '1':
                message = 'Input Month-Day: '
                date = banking.input_datetime(message).split('-')
                results = banking.get_expenses_per_month(messages, date)
            elif card == '2':
                pass
            elif card == '3':
                pass
            else:
                print('Choose between 1, 2 or 3')

        elif selection == '2':
            pass
        elif selection == '3':
            break
        else:
            print('Choose between 1, 2 or 3')
    except KeyboardInterrupt:
        print('Input interrupted')
    


    