import functions
import constants
import datetime
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment


dataset = 'messages.txt'
records_list = functions.get_dataset(dataset)

while 1:
    functions.menu()
    try:
        user_choice = input('Choose: ')

        if user_choice == '1':
            phone_list = functions.get_banks(records_list)
            cards = functions.get_cards(records_list)

            k = 1
            for p in phone_list:
                current_funds = functions.get_current_funds(records_list, p)
                try:
                    print(str(k) + '. *' + cards[k - 1] + ' (' + constants.banks[p] + ') : {money} EUR'
                          .format(money=functions.get_current_funds(records_list, p)))
                    k = k + 1
                except KeyError:
                    print(str(k) + '. *' + cards[k - 1] + ' (Bank' + str(k) + ') : {money} EUR'
                          .format(money=functions.get_current_funds(records_list, p)))
                    k = k + 1

        elif user_choice == '2':
    
            cards_list = functions.get_cards(records_list)
            SuperBank = str(cards_list[0])
            GorgeousBank = str(cards_list[1])
            print('1. *' + SuperBank + ' (SuperBank)')
            print('2. *' + GorgeousBank + ' (GorgeousBank)')

            k = 3
            for j in range(2, len(cards_list), 1):
                print(str(k) + '. *' + str(cards_list[j]) + '(bank' + str(k) + ')')
                k = k + 1
            print(str(k) + '. Total')
            k = k + 1
            print(str(k) + '. Exit to main menu')

            selection = input('Choose: ')
            if selection != str(k) and selection != str(k - 1):
                message = 'Input Month-Year: '
                date = functions.input_datetime(message)
                date_to_list = date.split('-')
                banks = functions.get_banks(records_list)
                resulting_expenses = functions.get_expenses(records_list, date_to_list, banks)
                if resulting_expenses != 0:
                    index = int(selection) - 1
                    cards_list = functions.get_cards(records_list)
                    print('Report for {month} {year}, card {card}'
                          .format(month=datetime.datetime(int(date_to_list[1]), int(date_to_list[0]), 1)
                                  .strftime('%B'), year=date_to_list[1], card=cards_list[len(cards_list) - 1 - index]))

                    print('Received {amount} EUR'.format(amount=resulting_expenses[1][index]))
                    print('Spent {amount} EUR'.format(amount=resulting_expenses[0][index]))
                    print('Delta {amount} EUR'.format(amount=int(resulting_expenses[1][index]) - int(resulting_expenses[0][index])))
                    ans = input('Export a full report to Excel? ')
                    if ans == 'y':
                        workbook = Workbook()
                        worksheet = workbook.active
                        worksheet['A1'] = 'Date'
                        worksheet['A1'].font = Font(b=True, color="D705F3")
                        worksheet['B1'] = 'Telephone'
                        worksheet['B1'].font = Font(b=True, color="D705F3")
                        worksheet['C1'] = 'Card No'
                        worksheet['C1'].font = Font(b=True, color="D705F3")
                        worksheet['D1'] = 'Type'
                        worksheet['D1'].font = Font(b=True, color="D705F3")
                        worksheet['E1'] = 'Sum'
                        worksheet['E1'].font = Font(b=True, color="D705F3")
                        worksheet['F1'] = 'Balance'
                        worksheet['F1'].font = Font(b=True, color="D705F3")

                        k = 1

                        for received in records_list:
                            if received['phone'] == resulting_expenses[2][index]:
                                worksheet['A' + str(k + 1)] = received['time']
                                worksheet['B' + str(k + 1)] = received['phone']
                                if received['phone'] == '480':
                                    worksheet['C' + str(k + 1)] = received['text'][1]
                                    worksheet['D' + str(k + 1)] = received['text'][0]
                                    worksheet['E' + str(k + 1)] = received['text'][2]
                                    worksheet['F' + str(k + 1)] = received['text'][3]
                                else:
                                    worksheet['C' + str(k + 1)] = received['text'][0]
                                    quantity = received['text'][1]
                                    quantity = int(quantity[1:])
                                    worksheet['E' + str(k + 1)] = quantity
                                    if quantity > 0:
                                        worksheet['D' + str(k + 1)] = 'Transfer'
                                    else:
                                        worksheet['D' + str(k + 1)] = 'Withdrawal'
                                    worksheet['F' + str(k + 1)] = received['text'][2]
                                k = k + 1
                        worksheet.column_dimensions['A'].width = 20
                        worksheet.column_dimensions['B'].width = 20
                        worksheet.column_dimensions['C'].width = 20
                        worksheet.column_dimensions['D'].width = 20
                        worksheet.column_dimensions['E'].width = 20
                        worksheet.column_dimensions['F'].width = 20
                        received = resulting_expenses[1][index]
                        spent = resulting_expenses[0][index]
                        worksheet['A' + str(k + 2)] = 'Received: {0} EUR'.format(received)
                        worksheet['A' + str(k + 2)].font = Font(b=True, color="007f00")
                        worksheet['B' + str(k + 2)] = 'Spent: {0} EUR'.format(spent)
                        worksheet['B' + str(k + 2)].font = Font(b=True, color="FF0000")
                        worksheet['C' + str(k + 2)] = 'Delta: {0} EUR'.format(received - spent)
                        worksheet['C' + str(k + 2)].font = Font(b=True, color="0000FF")

                        for row in worksheet.rows:
                            for cell in row:
                                cell.alignment = Alignment(horizontal='left')
                        workbook.save('Report.xlsx')
                else:
                    print('No transactions in this period')

            elif selection == str(k - 1):
                message = 'Input Month-Year: '
                date = functions.input_datetime(message)
                date_to_list = date.split('-')
                resulting_expenses = functions.get_expenses(records_list, date_to_list, functions.get_banks(records_list))
                if resulting_expenses != 0:
                    total_resulting_expenses = sum(resulting_expenses[0])
                    total_resulting_incomes = sum(resulting_expenses[1])
                    index = int(selection) - 1
                    print('Report for {month} {year}: '
                          .format(month=datetime.datetime(int(date_to_list[1]), int(date_to_list[0]), 1).strftime('%B'),
                                  year=date_to_list[1]))
                    print('Received {amount} EUR'.format(amount=total_resulting_incomes))
                    print('Spent {amount} EUR'.format(amount=total_resulting_expenses))
                    print('Delta {amount} EUR'.format(amount=total_resulting_incomes - total_resulting_expenses))
                else:
                    print('No transactions in specified period')

            elif selection == str(k):
                continue
            else:
                print('Wrong choice')

        elif user_choice == '3':
            break
        else:
            print('Wrong choice')
    except KeyboardInterrupt:
        print('Input Error')
