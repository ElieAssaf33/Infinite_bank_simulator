import sqlite3
import PySimpleGUI as sg
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

def get_balance():

    with connection:
        
        cursor.execute('SELECT Balance FROM Balance WHERE id = 1')
        balance = cursor.fetchall()
        balance = balance[0][0]

    return balance

def invest(investment, ammount):
    if investment == "Bitcoin":
        with connection:
            try:
                cursor.execute(('INSERT INTO Investments(Investment, Ammount, Current)'
                'VALUES(?,?,?);'),(investment, float(ammount)/float(btc), float(btc)))
            except Exception:
                cursor.execute(('UPDATE Investments SET Ammount = Ammount + ? WHERE Investment = ?'),
                (float(ammount)/float(btc), investment))
    elif investment == "Ethereum":
        with connection:
            try:
                cursor.execute(('INSERT INTO Investments(Investment, Ammount, Current)'
                'VALUES(?,?,?);'),(investment, float(ammount)/float(eth), float(eth)))
            except Exception:
                cursor.execute(('UPDATE Investments SET Ammount = Ammount + ? WHERE Investment = ?'),
                (float(ammount)/float(eth), investment))
    elif investment == "Dogecoin":
        with connection:
            try:
                cursor.execute(('INSERT INTO Investments(Investment, Ammount, Current)'
                'VALUES(?,?,?);'),(investment, float(ammount)/float(doge), float(doge)))
            except Exception:
                cursor.execute(('UPDATE Investments SET Ammount = Ammount + ? WHERE Investment = ?'),
                (float(ammount)/float(doge), investment))

def sell(investment, ammount):
    if investment == "Bitcoin":
        with connection:
            cursor.execute(('UPDATE Investments SET Ammount = Ammount - ? WHERE Investment = ?'),(float(ammount)/float(btc), investment))
    elif investment == "Ethereum":
        with connection:
            cursor.execute(('UPDATE Investments SET Ammount = Ammount - ? WHERE Investment = ?'),(float(ammount)/float(eth), investment))
    elif investment == "Dogecoin":
        with connection:
            cursor.execute(('UPDATE Investments SET Ammount = Ammount - ? WHERE Investment = ?'),(float(ammount)/float(doge), investment))

def content():
    with connection:
        cursor.execute(('UPDATE Investments SET Cash = Ammount * Current, Current = ? WHERE Investment = "Bitcoin"'),(float(btc),))
        cursor.execute(('UPDATE Investments SET Cash = Ammount * Current, Current = ? WHERE Investment = "Ethereum"'),(float(eth),))
        cursor.execute(('UPDATE Investments SET Cash = Ammount * Current, Current = ? WHERE Investment = "Dogecoin"'),(float(doge),))
        cursor.execute(('SELECT Investment, Ammount, Cash, Current  FROM Investments'))
        investments = cursor.fetchall()
    return investments

def make_investment(main_window:sg.Window):
    main_window.hide()

    investment = ['Bitcoin', 'Ethereum', 'Dogecoin']

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


