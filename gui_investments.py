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

def invest(investment, ammount):
    price = prices[investment]
    with connection:
        try:
            if int(ammount) < 0:
                sg.PopupOK("Invalid input: Enter a positive number", title="Invalid input", font='Arial 17')
            else:
                cursor.execute(('INSERT INTO Transactions(Investment,Action,Ammount, Cash, Date, Current)' 
                'VALUES(?,?,?,?,?,?);'),(investment,"Bought",float(ammount)/float(price) ,ammount,datetime.now(), float(price)))
                cursor.execute(('UPDATE Investments SET Ammount = Ammount + ? WHERE Investment = ?'),(float(ammount)/float(price), investment))
                cursor.execute(('UPDATE Balance SET Balance = Balance - ? WHERE id = 1'),(ammount,))
        except ValueError:
            sg.PopupOK("Invalid input: Enter a number", title="Invalid input", font='Arial 17')
        except sqlite3.IntegrityError:
            sg.PopupOK("Non-Sufficient Funds: Please enter a valid ammount of funds", title="Non-Sufficient Funds", font='Arial 17')

def sell(investment, ammount):
    price = prices[investment]
    with connection:
        try:
            if int(ammount) < 0:
                sg.PopupOK("Invalid input: Enter a positive number", title="Invalid input", font='Arial 17')
            else:
                cursor.execute(('INSERT INTO Transactions(Investment,Action ,Ammount, Cash,Date)'
                'VALUES(?,?,?,?,?);'), (investment,"Sold",float(ammount)/float(price), ammount, datetime.now()))
                cursor.execute(('UPDATE Investments SET Ammount = Ammount - ? WHERE Investment = ?'),(float(ammount)/float(price), investment))
                cursor.execute(('UPDATE Balance SET Balance = Balance + ? WHERE id = 1'),(ammount,))
        except ValueError:
            sg.PopupOK("Invalid input: Enter a number", title="Invalid input", font='Arial 17')
        except sqlite3.IntegrityError:
            sg.PopupOK("Insufficient Holdings: Please enter a valid ammount of shares", title="Insufficient Holdings", font='Arial 17')

def content():
    with connection:
        cursor.execute(('UPDATE Investments SET Cash = Ammount * Current, Current = ? WHERE Investment = "Bitcoin"'),(float(btc),))
        cursor.execute(('UPDATE Investments SET Cash = Ammount * Current, Current = ? WHERE Investment = "Ethereum"'),(float(eth),))
        cursor.execute(('UPDATE Investments SET Cash = Ammount * Current, Current = ? WHERE Investment = "Dogecoin"'),(float(doge),))
        cursor.execute(('UPDATE Investments SET Cash = Ammount * Current, Current = ? WHERE Investment = "Solana"'),(float(sol),))
        cursor.execute(('UPDATE Investments SET Cash = Ammount * Current, Current = ? WHERE Investment = "Avalanche"'),(float(avax),))
        cursor.execute(('UPDATE Investments SET Cash = Ammount * Current, Current = ? WHERE Investment = "Cardano"'),(float(ada),))
        cursor.execute(('UPDATE Investments SET Cash = Ammount * Current, Current = ? WHERE Investment = "XRP"'),(float(xrp),))
        cursor.execute(('SELECT Investment, Ammount, Cash, Current  FROM Investments'))
        investments = cursor.fetchall()
    return investments

def make_investment(main_window:sg.Window):
    main_window.hide()

    investment = ['Bitcoin', 'Ethereum', 'Dogecoin', 'Solana', 'Avalanche', 'Cardano', 'XRP']
    layout = [
    [
    sg.Table(values = content(), headings = ('Investment',
    'Ammount','Cash', 'Current Price'), key = '-TABLE-',
    expand_x=True, expand_y=True, justification='left')
    ],
    [
    sg.Text('Enter Ammount: '), 
    sg.Input('', key= '-AMMOUNT-', size=(10,8)),
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

    message = 'Not enough money'
    while True:
        event, values = window.read()

        if event in [sg.WINDOW_CLOSED , '-HOME-']:
            break
        if event == '-BUY-':
            invest(values['-INVESTMENT-'], values['-AMMOUNT-'])
            window['-TABLE-'].update(values=content())
        if event == '-SELL-':
            sell(values['-INVESTMENT-'], values['-AMMOUNT-'])
            window['-TABLE-'].update(values=content())

    window.close()
    main_window.un_hide()
