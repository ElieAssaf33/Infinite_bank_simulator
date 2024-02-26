import PySimpleGUI as sg
import sqlite3

connection = sqlite3.connect('infinite.db')

cursor = connection.cursor()
def get_balance():
     
    with connection:
            
        cursor.execute('CREATE TABLE IF NOT EXISTS Balance(id INTEGER PRIMARY KEY, Balance INTEGER)')
        cursor.execute('SELECT Balance FROM Balance WHERE id = 1')
        balance = cursor.fetchall()
        balance = balance[0][0]

    return(balance)



def check_balance(main_window:sg.Window):
    main_window.hide()
    layout = [
    [
    sg.Text('Balance:'), sg.Text(get_balance(), key = '-BALANCE-')
    ],
    [
    sg.Button('Home', key = '-HOME-')
    ]
]
    window = sg.Window('Balance', layout, size= (400,400), font= 'Arial 23')
   
    while True:

        event, values = window.read()
     
        if event in [sg.WINDOW_CLOSED, '-HOME-']:
            break

    window.close()
    main_window.un_hide()

