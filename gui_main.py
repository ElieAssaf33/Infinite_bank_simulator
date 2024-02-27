import PySimpleGUI as sg
import sqlite3
from gui_balance import check_balance
from gui_investments import make_investment
from gui_loans import make_loan

sg.theme('DarkTeal9')

main_layout = [[sg.Text('''Welcome to Infinite, Infinite is a company
that provides infinite solutions
to finanicial stability, growth and support. 
Our main goal is to make as much people 
reach financial freedom as possible.''')],
    [
    sg.Button('Invest', key = '-INVEST-',font= 'Arial 30'), 
    sg.Button('Loan', key = '-LOAN-',font= 'Arial 30'), 
    sg.Button('Balance', key = '-BALANCE-',font= 'Arial 30'), 
    sg.Button('Exit', key='-EXIT-',font= 'Arial 30')
    ],
]

main_window = sg.Window(
    'Infinite', 
    main_layout, 
    size=(500,270), 
    element_justification='center', 
    element_padding=15, 
    font = 'Arial 23',
    finalize=True,
    text_justification='center',
)

while True:
    event, values = main_window.read(timeout=0.1)
    if event in [sg.WINDOW_CLOSED, "-EXIT-"]:
        break
    if event == '-INVEST-':
        make_investment(main_window)
    if event == '-LOAN-':
        make_loan(main_window)
    if event == '-BALANCE-':
        check_balance(main_window)
 