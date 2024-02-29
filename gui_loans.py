import PySimpleGUI as sg
from infinite_db import connection,cursor
from datetime import date, timedelta, datetime
import sqlite3

def pay_monthly(loan):

    with connection:
        try:
            cursor.execute(('UPDATE Loans SET Amount_left = Amount_left - Monthly WHERE Loan = ?'), (loan))
            cursor.execute(('UPDATE Loans SET Period_left = Period_left - 1 WHERE Loan = ?'), (loan))
            cursor.execute(('SELECT Monthly FROM Loans WHERE Loan = ? '), (loan))
            monthly = cursor.fetchall()
            cursor.execute(('UPDATE Balance SET Balance = Balance - ?'),(monthly[0][0],))
        except sqlite3.IntegrityError:
            cursor.execute(('DELETE FROM Loans WHERE Loan = ?'),(loan))
            sg.PopupOK('You have successfully paid of your loan', title='Loan paid', font='Arial 20')
        except sqlite3.ProgrammingError:
            sg.PopupOK('Please pick a loan', font='Arial 20')
        

def calculate_loan(loan_ammount, years, interest):

    with connection:
        try:
            if int(years) < 0 or int(loan_ammount) < 0 or int(interest) < 0:
                sg.PopupOK("Invalid input: Enter a positive number", title="Invalid input", font='Arial 17')
            else:
                monthly_payment = (int(loan_ammount) * (int(interest)/100/12)) / (1-(1 + (0.05/12))**-abs(12 * int(years)))
                rounded_monthly_payment = round(monthly_payment, 2)
                return rounded_monthly_payment
        except ValueError:
                sg.PopupOK('Invalid input: Enter a number',title='Invalid input' ,font='Arial 20')

def get_loans():
    
    with connection:
        cursor.execute("SELECT Loan, Amount, ROUND(Monthly,2), Period, Interest, Period_left, ROUND(Amount_left,2), Created_at FROM Loans")
        loans = cursor.fetchall()
    return loans

def create_loan(loan, amount, monthly, period, interest, created_at):

    with connection: 
        try:
            cursor.execute(('INSERT INTO Loans(Loan, Amount, Monthly,Period,Interest ,Period_left,Amount_left, Created_at)'
            'VALUES(?,?,?,?,?,?,?,?);'),(loan, amount, monthly,period, interest,int(period) * 12,monthly * (int(period)*12), created_at))
            cursor.execute(('UPDATE Balance SET Balance = Balance + ?'), (amount,))
            cursor.execute(('INSERT INTO Transactions(Name, Action, Amount, Date) VALUES(?,?,?,?)'), (loan, "Loan Received",amount, created_at))
        except sqlite3.IntegrityError:
                sg.PopupOK('Existing name: You already have a loan with this name',title='Existing name' ,font = 'Arial 20')
                return False
        
    return True
def get_loan_names():

    with connection:
        cursor.execute('SELECT Loan FROM Loans')
        loan_names = cursor.fetchall()
    return loan_names

def show_loans(create_loan_window:sg.Window):

    create_loan_window.hide()
     
    layout = [
        [
            sg.Table(values = get_loans(), headings= (
            "Loan", "Ammount($)", "Monthly($)", "Years","Interest(%)","Months left", "Amount left($)", "Created at"), 
            expand_x=True, expand_y=True, justification='left', key = '-TABLE-')
        ],
        [
            sg.Button('Back', key = '-BACK-') ,
            sg.DropDown(get_loan_names(), key = '-LOAN-', size=(10,1)),
            sg.Button('Pay for month', key = '-PAYMENT-'),
        ],
    ]
    window = sg.Window('Loans', layout, size= (1300,700), font='Arial 23', element_justification='center')

    while True:
        event, values = window.read()
        if event in ['-BACK-', sg.WINDOW_CLOSED]:
                break
        if event == '-PAYMENT-':
            pay_monthly(values['-LOAN-'])
            window['-TABLE-'].update(get_loans())
            
    window.close()
    create_loan_window.un_hide()

def make_loan(main_window:sg.Window):
    
    main_window.hide()
    layout = [
    [
    sg.Text('Loan calculator')
    ],
    [
    sg.Text('Loan amount:', size=(17,1)), 
    sg.Input('', key= '-AMOUNT-', size=(17,1))
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
    sg.Button('Submit', key = '-SUBMIT-', visible=False),
    sg.Button('Show loans', key = '-LOANS-'),
    sg.Button('Home', key = '-HOME-'),
    ]
]
    window = sg.Window('Loan', layout,size=(500,450), font = 'Arial 23', element_justification='left', element_padding=10)

    while True:
        event, values = window.read()
        if event in [sg.WINDOW_CLOSED, '-HOME-']:
            break  
        if event == '-CALCULATE-': 
            calculated_monthly = calculate_loan(values['-AMOUNT-'], values['-PERIOD-'], values['-INTEREST-'])
            if calculated_monthly:
                window['-MONTHLY-'].update(calculated_monthly)
                window['-SUBMIT-'](visible = True)    
        if event == '-SUBMIT-':
            if create_loan(values['-LOAN-'],values['-AMOUNT-'],calculated_monthly, values['-PERIOD-'], values['-INTEREST-'], datetime.now().replace(microsecond=0)):
                if sg.PopupYesNo('Are you sure you?', title='Confirm',font='Arial 20') == 'Yes':
                    sg.PopupOK('You have commited to a loan of', values["-AMOUNT-"], title='Loan created successfully',font='Arial 20')
                else:
                    continue
            else:
                continue
        if event == '-LOANS-':
            show_loans(window)

    window.close()
    main_window.un_hide()
