import banking
import datetime
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment


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
                message = 'Input Month-Year: '
                date = banking.input_datetime(message)
                date_list = date.split('-')
                results = banking.get_expenses_per_month(messages, date_list)
                if results != 0:
                    index = int(choice) - 1
                    print('Report for {month} {year}, card {card}(SuperBank)'.format(month=datetime.datetime(int(date_list[1]), int(date_list[0]), 1).strftime('%B'), year=date_list[1], card=results[0][index]))
                    print('Received {amount} EUR'.format(amount=results[2][index]))
                    print('Spent {amount} EUR'.format(amount=results[1][index]))
                    print('Delta {amount} EUR'.format(amount=int(results[2][index])-int(results[1][index])))
                    ans = input('Export a full report to Excel?')
                    if ans == 'y':
                        wb = Workbook()
                        ws = wb.active
                        ws['A1'] = 'Time'
                        ws['A1'].font = Font(b=True, color="ff0080")
                        ws['B1'] = 'Phone'
                        ws['B1'].font = Font(b=True, color="ff0080")
                        ws['C1'] = 'Card Number'
                        ws['C1'].font = Font(b=True, color="ff0080")
                        ws['D1'] = 'Type of transaction'
                        ws['D1'].font = Font(b=True, color="ff0080")
                        ws['E1'] = 'Sum of transaction'
                        ws['E1'].font = Font(b=True, color="ff0080")
                        ws['F1'] = 'Balance'
                        ws['F1'].font = Font(b=True, color="ff0080")

                        i = 1
                        for r in results[3]:
                            ws['A' + str(i+1)] = r['time']
                            ws['B' + str(i+1)] = r['phone']
                            if r['phone'] == '480':
                                ws['C' + str(i+1)] = r['text'][1]
                                ws['D' + str(i+1)] = r['text'][0]
                                ws['E' + str(i + 1)] = r['text'][2]
                                ws['F' + str(i + 1)] = r['text'][3]
                            else:
                                ws['C' + str(i + 1)] = r['text'][0]
                                sum_of_transaction = r['text'][1]
                                sum_of_transaction = int(sum_of_transaction[1:])
                                ws['E' + str(i + 1)] = sum_of_transaction
                                if sum_of_transaction > 0:
                                    ws['D' + str(i + 1)] = 'Transfer'
                                else:
                                    ws['D' + str(i + 1)] = 'Withdrawal'
                                ws['F' + str(i + 1)] = r['text'][2]
                            i += 1
                        ws.column_dimensions['A'].width = 20
                        ws.column_dimensions['B'].width = 20
                        ws.column_dimensions['C'].width = 20
                        ws.column_dimensions['D'].width = 20
                        ws.column_dimensions['E'].width = 20
                        ws.column_dimensions['F'].width = 20
                        r1 = int(results[2][0])
                        r2 = int(results[2][1])
                        s1 = int(results[1][0])
                        s2 = int(results[1][1])
                        ws['A' + str(i + 2)] = 'Received: {0} EUR'.format(r1 + r2)
                        ws['A' + str(i + 2)].font = Font(b=True, color="007f00")
                        ws['B' + str(i + 2)] = 'Spent: {0} EUR'.format(s1 + s2)
                        ws['B' + str(i + 2)].font = Font(b=True, color="FF0000")
                        ws['C' + str(i + 2)] = 'Delta: {0} EUR'.format(r1 + r2 - s1 - s2)
                        ws['C' + str(i + 2)].font = Font(b=True, color="0000FF")

                        for row in ws.rows:
                            for cell in row:
                                cell.alignment = Alignment(horizontal='left')
                        wb.save('FullMonthReport.xlsx')
                else:
                    print('No transactions in specified period')

            elif choice == '3':
                message = 'Input Month-Year: '
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
    


    