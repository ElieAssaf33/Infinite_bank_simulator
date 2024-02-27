import sqlite3
import PySimpleGUI as sg
import requests
from datetime import datetime
from crypto_prices import *
connection = sqlite3.connect('infinite.db')
cursor = connection.cursor()

prices = {"Bitcoin":btc, "Ethereum": eth, "Dogecoin": doge, "Solana":sol, "Avalanche": avax, "Cardano": ada,"XRP": xrp }

print(prices['Bitcoin'])



def get_balance():

    with connection:
        
        cursor.execute('SELECT Balance FROM Balance WHERE id = 1')
        balance = cursor.fetchall()
        balance = balance[0][0]

    return balance

def invest(investment, ammount):
    price = prices[investment]
    with connection:
        try:
            cursor.execute(('INSERT INTO Transactions(Investment,Action,Ammount, Cash, Date, Current)' 
            'VALUES(?,?,?,?,?,?);'),
            (investment,"Bought",float(ammount)/float(price) ,ammount,datetime.now(), float(price)))
            cursor.execute(('INSERT INTO Investments(Investment, Ammount, Current)'
            'VALUES(?,?,?);'),(investment, float(ammount)/float(price), float(price)))
        except Exception:
            cursor.execute(('UPDATE Investments SET Ammount = Ammount + ? WHERE Investment = ?'),
            (float(ammount)/float(price), investment))

def sell(investment, ammount):
    price = prices[investment]
    with connection:
        try:
            cursor.execute(('INSERT INTO Transactions(Investment,Action ,Ammount, Cash,Date)'
            'VALUES(?,?,?,?,?);'), (investment,"Sold",float(ammount)/float(price), ammount, datetime.now()))
            cursor.execute(('UPDATE Investments SET Ammount = Ammount - ? WHERE Investment = ?'),(float(ammount)/float(price), investment))
        except Exception:
            sg.popup('You dont have that much to sell', font='Arial 23')
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
    'Ammount','Cash', 'Current Price'), key = '-table-',
    expand_x=True, expand_y=True, justification='left')
    ],
    [
    sg.Text('Enter Ammount: '), 
    sg.Input('', key= '-Ammount-', size=(10,8)),
    sg.Text('Pick Investment'),
    sg.DropDown(investment, size=(10,8), key='-Investment-', default_value= investment[0]),
    sg.Button('Add Investment', key = '-ADD-'),sg.Button('Sell', key = '-SELL-')
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
        if event == '-ADD-' and int(values['-Ammount-']) <= int(get_balance()):
            invest(values['-Investment-'], values['-Ammount-'])
            window['-table-'].update(values=content())
            with connection:
                cursor.execute(('UPDATE Balance SET Balance = Balance - ? WHERE id = 1'),(int(values['-Ammount-']),))
        if event == '-ADD-' and int(values['-Ammount-']) > int(get_balance()):
            window['-MESSAGE-'].update(message)
        if event == '-SELL-':
            sell(values['-Investment-'], values['-Ammount-'])
            window['-table-'].update(values=content())
            with connection:
                cursor.execute(('UPDATE Balance SET Balance = Balance + ? WHERE id = 1'),(int(values['-Ammount-']),))
            
    window.close()
    main_window.un_hide()


