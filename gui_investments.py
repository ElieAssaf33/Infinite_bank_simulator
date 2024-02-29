import sqlite3
import PySimpleGUI as sg
import requests
from datetime import datetime
from crypto_prices import *
from infinite_db import connection, cursor

def get_balance():

    with connection:
        
        cursor.execute('SELECT Balance FROM Balance')
        balance = cursor.fetchone()

    return balance

def invest(investment, amount):

    price = prices[investment]
    with connection:
        try:
            if int(amount) < 0:
                sg.PopupOK("Invalid input: Enter a positive number", title="Invalid input", font='Arial 17')
            else:
                cursor.execute(('INSERT INTO Transactions(Name,Action,Amount, Cash, Date, Current)' 
                'VALUES(?,?,?,?,?,?);'),(investment,"Investment made",float(amount)/float(price) ,amount,datetime.now().replace(microsecond=0), float(price)))
                cursor.execute(('UPDATE Investments SET Amount = Amount + ? WHERE Investment = ?'),(float(amount)/float(price), investment))
                cursor.execute(('UPDATE Balance SET Balance = Balance - ? WHERE id = 1'),(amount,))
        except ValueError:
            sg.PopupOK("Invalid input: Enter a number", title="Invalid input", font='Arial 17')
        except sqlite3.IntegrityError:
            sg.PopupOK("Non-Sufficient Funds: Please enter a valid ammount of funds", title="Non-Sufficient Funds", font='Arial 17')

def sell(investment, amount):

    price = prices[investment]
    with connection:
        try:
            if int(amount) < 0:
                sg.PopupOK("Invalid input: Enter a positive number", title="Invalid input", font='Arial 17')
            else:
                cursor.execute(('INSERT INTO Transactions(Name,Action ,Amount, Cash,Date)'
                'VALUES(?,?,?,?,?);'), (investment,"Investment sold",float(amount)/float(price), amount, datetime.now().replace(microsecond=0)))
                cursor.execute(('UPDATE Investments SET Amount = Amount - ? WHERE Investment = ?'),(float(amount)/float(price), investment))
                cursor.execute(('UPDATE Balance SET Balance = Balance + ? WHERE id = 1'),(amount,))
        except ValueError:
            sg.PopupOK("Invalid input: Enter a number", title="Invalid input", font='Arial 17')
        except sqlite3.IntegrityError:
            sg.PopupOK("Insufficient Holdings: Please enter a valid amount", title="Insufficient Holdings", font='Arial 17')

def content():

    with connection:
        for price in prices:
            cursor.execute(('UPDATE Investments SET Cash = Amount * Current, Current = ? WHERE Investment = ?'),(float(prices[price]), price))
        cursor.execute(('SELECT Investment, ROUND(Amount,4), ROUND(Cash,4), ROUND(Current,4)  FROM Investments'))
        investments = cursor.fetchall()
    return investments

def make_investment(main_window:sg.Window):

    main_window.hide()
    investment = ['Bitcoin', 'Ethereum', 'Dogecoin', 'Solana', 'Avalanche', 'Cardano', 'XRP', "Litecoin", "Polygon"]
    layout = [
    [
    sg.Table(values = content(), headings = ('Investment',
    'Amount','Cash($)', 'Current Price($)'), key = '-TABLE-',
    expand_x=True, expand_y=True, justification='left')
    ],
    [
    sg.Text('Enter Amount: '), 
    sg.Input('', key= '-AMOUNT-', size=(10,8)),
    sg.Text('Pick Investment'),
    sg.DropDown(investment, size=(10,8), key='-INVESTMENT-', default_value= investment[0]),
    sg.Button('Buy', key = '-BUY-'),sg.Button('Sell', key = '-SELL-')
    ],
    [
    sg.Button('Home', key = '-HOME-'), sg.Text('', key='-MESSAGE-')
    ]
    ]
    window = sg.Window('Invest', layout, size = (1000,700), element_padding = 10,
    text_justification='center',element_justification='center', font = 'Arial 23')
    
    while True:
        event, values = window.read()

        if event in [sg.WINDOW_CLOSED , '-HOME-']:
            break
        if event == '-BUY-':
            invest(values['-INVESTMENT-'], values['-AMOUNT-'])
            window['-TABLE-'].update(values=content())
        if event == '-SELL-':
            sell(values['-INVESTMENT-'], values['-AMOUNT-'])
            window['-TABLE-'].update(values=content())

    window.close()
    main_window.un_hide()
