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

def get_loans():
    with connection:
        cursor.execute("SELECT Loan, Ammount, Monthly, Period, Interest, Period_left, Ammount_left, Created_at FROM Loans")
        loans = cursor.fetchall()
    return loans

def create_loan(loan, ammount, monthly, period, interest, created_at, ):
    with connection:
        try:
            if int(period) > 0 or int(ammount) > 0 or int(interest) > 0:
                sg.PopupOK("Invalid input: Enter a positive number", title="Invalid input", font='Arial 17')
            else:
                cursor.execute(('INSERT INTO Loans(Loan, Ammount, Monthly, Period, Interest, Created_at)'
                'VALUES(?,?,?,?,?,?);'),(loan, ammount, monthly, period,  interest, created_at))
        except ValueError:
                sg.PopupOK('Invalid input: Enter a number', font='Arial 20')
def show_loans(create_loan_window:sg.Window):
    create_loan_window.hide()

    layout = [
    [
    sg.Table(values = get_loans(), headings= ("Loan", "Ammount", "Monthly", "Period","Period left", "Ammount left", "Created at"), expand_x=True, expand_y=True)
    ]
    ]
    window = sg.Window('Loans', layout, size= (1000,700), font='Arial 23')

    while True:
        event, values = window.read()

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
    ],
    [
    sg.Button('Submit', key = '-SUBMIT-', visible=False)
    ],
    [
    sg.Button('Show loans', key = '-LOANS-'),
    sg.Button('Home', key = '-HOME-'),
    ]
]
    window = sg.Window('Loan', layout,size=(500,500), font = 'Arial 23', text_justification='left', element_justification='center', element_padding=10)

    while True:
        event, values = window.read()
        if event in [sg.WINDOW_CLOSED, '-HOME-']:
            break  
        if event == '-CALCULATE-': 
            calculated_monthly = calculate_loan(values['-AMMOUNT-'], values['-PERIOD-'], values['-INTEREST-'])
            window['-MONTHLY-'].update(calculated_monthly)
            window['-SUBMIT-'](visible = True)    
        if event == '-PAY_MONTHLY-':
            pay_monthly()
        if event == '-SUBMIT-':
            if sg.PopupYesNo('Are you sure?', font='Arial 23') == 'Yes':
                sg.PopupOK('You have commited to a loan of', values["-AMMOUNT-"])
                create_loan(values['-LOAN-'],values['-AMMOUNT-'],calculated_monthly, values['-PERIOD-'], values['-INTEREST-'], datetime.now())
            else:
                continue
        if event == '-LOANS-':
            show_loans(window)
    window.close()
    main_window.un_hide()
