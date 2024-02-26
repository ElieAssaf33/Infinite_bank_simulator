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
    sg.Text('Loan ammount'), 
    sg.Input('', key= '-AMMOUNT-')
    ],
    [
    sg.Text('Period in years'),
    sg.Input('', key='-PERIOD-')
    ],
    [
    sg.Text('Interest rate'),
    sg.Input('', key='-INTEREST-')
    ],
    [
    sg.Button('Calculate', key= '-CALCULATE-'),
    sg.Text('Monthly payment:'),
    sg.Text('', key='-MONTHLY-')
    ],
    [
    sg.Text('Make loan'),
    sg.Button('Submit', key = '-SUBMIT-', visible=False),
    sg.Text('Input name'),
    sg.Input('', key = '-LOAN-')
    ],
    [
    sg.Button('Home', key = '-HOME-'),
    ]
]

    window = sg.Window('Loan', layout,size=(1000,700), font = 'Arial 23')

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
