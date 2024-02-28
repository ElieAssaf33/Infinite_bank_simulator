import PySimpleGUI as sg
import sqlite3
from crypto_prices import *
from infinite_db import connection, cursor

def get_transaction_list():

    with connection:
        cursor.execute(('UPDATE Transactions SET Current = ? * Ammount WHERE Investment = "Bitcoin"'), (float(btc),))
        cursor.execute(('UPDATE Transactions SET Current = ? * Ammount WHERE Investment = "Ethereum"'), (float(eth),))
        cursor.execute(('UPDATE Transactions SET Current = ? * Ammount WHERE Investment = "Dogecoin"'), (float(doge),))
        cursor.execute(('UPDATE Transactions SET Current = ? * Ammount WHERE Investment = "Solana"'), (float(sol),))
        cursor.execute(('UPDATE Transactions SET Current = ? * Ammount WHERE Investment = "Avalanche"'), (float(avax),))
        cursor.execute(('UPDATE Transactions SET Current = ? * Ammount WHERE Investment = "Cardano"'), (float(ada),))
        cursor.execute(('UPDATE Transactions SET Current = ? * Ammount WHERE Investment = "XRP"'), (float(xrp),))
        cursor.execute('SELECT Investment,Action,Ammount, Cash, Current, Date FROM Transactions')
        transaction_list = cursor.fetchall()
    return transaction_list

def get_balance():

    with connection:
        cursor.execute('SELECT Balance FROM Balance')
        balance = cursor.fetchone()
    return balance[0]

def get_invested_balance():

    with connection:
        cursor.execute('SELECT SUM(Cash) from Investments')
        invested = cursor.fetchone()
    return invested[0]

def transaction_list(balance_window: sg.Window):

    balance_window.hide()
    layout = [
        [
        sg.Table(values = get_transaction_list(), 
        headings=('Investment','Action' ,'Ammount', 'Bought for','Currently for','Date'), 
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

