import PySimpleGUI as sg
import sqlite3
import requests

connection = sqlite3.connect('infinite.db')
cursor = connection.cursor()

btc = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
data = requests.get(btc) 
data = data.json() 
btc = data['price']

eth = "https://api.binance.com/api/v3/ticker/price?symbol=ETHUSDT"
data = requests.get(eth) 
data = data.json() 
eth = data['price']

doge = "https://api.binance.com/api/v3/ticker/price?symbol=DOGEUSDT"
data = requests.get(doge) 
data = data.json() 
doge = data['price']

def get_transaction_list():

    with connection:
        cursor.execute(('UPDATE Transactions SET Current = ? * Ammount WHERE Investment = "Bitcoin"'), (float(btc),))
        cursor.execute(('UPDATE Transactions SET Current = ? * Ammount WHERE Investment = "Ethereum"'), (float(eth),))
        cursor.execute(('UPDATE Transactions SET Current = ? * Ammount WHERE Investment = "Dogecoin"'), (float(doge),))
        cursor.execute('SELECT Investment,Action,Ammount, Cash, Current, Date FROM Transactions')
        transaction_list = cursor.fetchall()
    return transaction_list

def get_balance():
    with connection:
        
        cursor.execute('SELECT Balance FROM Balance WHERE id = 1')
        balance = cursor.fetchall()
        balance = balance[0][0]

    return(balance)

def get_invested_balance():

    with connection:
        cursor.execute('SELECT SUM(Cash) from Investments')
        invested = cursor.fetchall()
        invested = invested[0][0]

    return(invested)

def transaction_list(balance_window: sg.Window):
    balance_window.hide()
    layout = [
        [
        sg.Table(values = get_transaction_list(), 
        headings=('Investment','Action' ,'Ammount', 'Cash','Current','Date'), 
        expand_x=True, expand_y=True, justification='left')
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
    window = sg.Window('Balance', layout, size= (400,250), font= 'Arial 23', element_padding=5)
   
    while True:

        event, values = window.read()
     
        if event in [sg.WINDOW_CLOSED, '-HOME-']:
            break
        if event == '-TRANSACTIONS-':
            transaction_list(window)

    window.close()
    main_window.un_hide()

