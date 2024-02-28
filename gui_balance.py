import PySimpleGUI as sg
import sqlite3
from crypto_prices import *
from infinite_db import connection, cursor

def get_transaction_list():

    with connection:
        cursor.execute(('UPDATE Transactions SET Current = ? * Amount WHERE Name = "Bitcoin"'), (float(btc),))
        cursor.execute(('UPDATE Transactions SET Current = ? * Amount WHERE Name = "Ethereum"'), (float(eth),))
        cursor.execute(('UPDATE Transactions SET Current = ? * Amount WHERE Name = "Dogecoin"'), (float(doge),))
        cursor.execute(('UPDATE Transactions SET Current = ? * Amount WHERE Name = "Solana"'), (float(sol),))
        cursor.execute(('UPDATE Transactions SET Current = ? * Amount WHERE Name = "Avalanche"'), (float(avax),))
        cursor.execute(('UPDATE Transactions SET Current = ? * Amount WHERE Name = "Cardano"'), (float(ada),))
        cursor.execute(('UPDATE Transactions SET Current = ? * Amount WHERE Name = "XRP"'), (float(xrp),))
        cursor.execute('SELECT Name,Action,ROUND(Amount,3), ROUND(Cash,3), ROUND(Current,3), strftime("%Y-%m-%d %H:%M:00", datetime(Date,"unixepoch")) FROM Transactions')
        transaction_list = cursor.fetchall()

    return transaction_list

def get_balance():

    with connection:
        cursor.execute('SELECT Balance FROM Balance')
        balance = cursor.fetchone()
        rounded = round(balance[0], 2)
    return rounded

def get_invested_balance():

    with connection:
        cursor.execute('SELECT SUM(Cash) from Investments')
        invested = cursor.fetchone()
        rounded  = round(invested[0],2)
    return rounded

def transaction_list(balance_window: sg.Window):

    balance_window.hide()
    layout = [
        [
        sg.Table(values = get_transaction_list(), 
        headings=('Transaction','Action' ,'Amount', 'Bought for','Currently for','Date'), 
        expand_x=True, expand_y=True, justification='left', col_widths=(20))
        ],
        [
        sg.Button('Balance', key = '-BALANCE-')
        ]
        ]
    window = sg.Window('Transactions', layout, size = (1300,700), font= 'Arial 23', element_justification='center', text_justification='center')

    while True:
        event, values = window.read()

        if event in [sg.WIN_CLOSED, '-BALANCE-']:
            break
    
    window.close()
    balance_window.un_hide()

def check_balance(main_window:sg.Window):

    main_window.hide()
    layout = [
    [
    sg.Text('Portfolio:'), sg.Text(get_balance() + get_invested_balance()),
    ],
    [
    sg.Text('Cash balance:'), sg.Text(get_balance())
    ],
    [
    sg.Text('Invested balance:'), sg.Text(get_invested_balance()),
    ],
    [
    sg.Button('Home', key = '-HOME-'), sg.Button('Transactions', key = '-TRANSACTIONS-')
    ]
]
    window = sg.Window('Balance', layout, size= (400,200), font= 'Arial 23', element_padding=7)
   
    while True:

        event, values = window.read()
     
        if event in [sg.WINDOW_CLOSED, '-HOME-']:
            break
        if event == '-TRANSACTIONS-':
            transaction_list(window)

    window.close()
    main_window.un_hide()

