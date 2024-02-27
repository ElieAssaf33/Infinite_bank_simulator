import PySimpleGUI as sg
from infinite_db import connection,cursor
from datetime import date, timedelta, datetime

def pay_monthly():
    pass

def pay_upfront():
    pass

def calculate_loan(loan_ammount, years, interest):
    monthyly_payment = (int(loan_ammount) * (int(interest)/100/12)) / (1-(1 + (0.05/12))**-abs(12 * int(years)))
    return monthyly_payment

def create_loan(loan, ammount, monthly, period, interest, created_at, ):
    with connection:
        cursor.execute(('INSERT INTO Loans(Loan, Ammount, Monthly, Period, Interest, Created_at)'
    'VALUES(?,?,?,?,?,?);'),(loan, ammount, monthly, period,  interest, created_at))
def show_loans():
    with connection:
        cursor.execute(('UPDATE Loans SET Period_left = Created_at + ?'),(datetime.now() + timedelta(days = 4),))

show_loans()

def make_loan(main_window:sg.Window):
    main_window.hide()

    layout = [
    [
    sg.Text('Loan calculator')
    ],
    [
    sg.Text('Loan ammount:', size=(17,1)), 
    sg.Input('', key= '-AMMOUNT-', size=(17,1))
    ],
    [
    sg.Text('Period in years:', size=(17,1)),
    sg.Input('', key='-PERIOD-', size=(17,1))
    ],
    [
    sg.Text('Interest rate:', size=(17,1)),
    sg.Input('', key='-INTEREST-', size=(17,1))
    ],
    [
    sg.Text('Loan name:', size=(17,1)),
    sg.Input('', key = '-LOAN-', size=(17,1))
    ],
    [
    sg.Button('Calculate', key= '-CALCULATE-')
    ],
    [
    sg.Text('Monthly payment:',size=(17,1)),
    sg.Text('', key='-MONTHLY-', size=(17,1)),
    sg.Button('Submit', key = '-SUBMIT-', visible=False)
    ],
    [
    sg.Button('Home', key = '-HOME-'),
    ]
]

    window = sg.Window('Loan', layout,size=(500,450), font = 'Arial 23', text_justification='left', element_justification='center', element_padding=10)

    while True:
        event, values = window.read()
        if event in [sg.WINDOW_CLOSED, '-HOME-']:
            break  
        if event == '-CALCULATE-':
            calculated = calculate_loan(values['-AMMOUNT-'], values['-PERIOD-'], values['-INTEREST-'])
            window['-MONTHLY-'].update(calculated)
            window['-SUBMIT-'](visible = True)
        if event == '-PAY_MONTHLY-':
            pay_monthly()
        if event == '-SUBMIT-':
            if sg.PopupYesNo('Are you sure?', font='Arial 23') == 'Yes':
                sg.popup('You have commited to a loan of', values["-AMMOUNT-"])
                create_loan(values['-LOAN-'],values['-AMMOUNT-'],calculated, values['-PERIOD-'], values['-INTEREST-'], datetime.now())
            else:
                continue
        if event == '-PAY_UPFRONT-':
            pay_upfront()
    window.close()
    main_window.un_hide()
